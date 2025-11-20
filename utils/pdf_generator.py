from jinja2 import Environment, BaseLoader
from weasyprint import HTML
import base64
import pandas as pd
import os
import tempfile
from datetime import datetime
from PIL.Image import Image 
from io import BytesIO

# ------------------------
# --- Helper functions ---
# ------------------------
def format_german_currency(value):
    """
    Formats a numeric value into German currency format.

    Args:
        value (float or int): The number to format.

    Returns:
        str: The number formatted with comma as decimal and period as thousands separator,
             e.g., 1.234,56. If formatting fails, the original value is returned.
    """
    try:
        return f"{value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except:
        return value  # fallback for non-numeric cases

def encode_file_to_base64(file_or_image):
    """
    Encodes an image or file into a base64 PNG data URI.

    Args:
        file_or_image (Image | BytesIO | str | os.PathLike): The input image or file.
            - PIL.Image.Image: will be saved as PNG to memory.
            - BytesIO: binary stream will be encoded directly.
            - str / os.PathLike: path to a file on disk.

    Returns:
        str: Base64-encoded image data URI for PNG format.

    Raises:
        TypeError: If the input type is unsupported.
    """
    if isinstance(file_or_image, Image):  # PIL image
        buffered = BytesIO()
        file_or_image.convert("RGB").save(buffered, format="JPEG")
        img_bytes = buffered.getvalue()

    elif isinstance(file_or_image, BytesIO):  # already a BytesIO object
        img_bytes = file_or_image.getvalue()

    else:
        raise TypeError(f"Unsupported image type: {type(file_or_image)}")

    return f"data:image/jpeg;base64,{base64.b64encode(img_bytes).decode()}"

def encode_logo_as_base64_png(path="assets/logo.png"):
    """
    Loads the PNG logo from disk and returns a base64-encoded PNG data URI.
    """
    with open(path, "rb") as f:
        img_bytes = f.read()
    return f"data:image/png;base64,{base64.b64encode(img_bytes).decode()}"

# -----------------
# --- Build PDF ---
# ----------------- 
def build_pdf(product_df, customer_df, custom_images, template_type, rabatt, payment_details, if_mwst, atu):
    """
    Builds a PDF document from product and customer data using an HTML template.

    Args:
        product_df (pd.DataFrame): DataFrame containing product rows with fields such as
            'Position', '2. Position', 'Titel', 'Beschreibung', 'Menge', 'Preis', 'Gesamtpreis', etc.
        customer_df (pd.DataFrame): DataFrame with a single row of customer data, including 'Angebots_ID'.
        custom_images (dict): Dictionary of images keyed by article number. Each value can be
            a PIL Image, BytesIO, or file path.

    Returns:
        str: File path to the generated PDF saved in a temporary directory.

    Raises:
        ValueError: If product or customer data is empty.
    """
    if product_df.empty or customer_df.empty:
        raise ValueError("Produkt- oder Kundendaten fehlen.")

    rows = []

    for i, row in product_df.iterrows():
        pos = str(int(row.get("Position", 0)))

        # Get and sanitize "2. Position"
        pos2_raw = row.get("2. Position")

        if pos2_raw is None or str(pos2_raw).strip() == "":
            pos2 = 0
        else:
            try:
                pos2 = int(pos2_raw)
            except ValueError:
                pos2 = 0  # fallback if the value is not convertible

        # Generate pos_label
        pos_label = f"{pos},{pos2}" if pos2 != 0 else pos

        article_number = row.get("Art_Nr")
        image_data = None

        if article_number in custom_images:
            image_data = encode_file_to_base64(custom_images[article_number])

        is_alternative = row.get("Alternative", False)

        # Abmessungen
        abmessungen = ""
        if pd.notna(row.get('Breite')):
            abmessungen += f"Breite: {float(row.get('Breite'))} mm\n"
        if pd.notna(row.get('Tiefe')):
            abmessungen += f"Tiefe: {float(row.get('Tiefe'))} mm\n"
        if pd.notna(row.get('Höhe')):
            abmessungen += f"Höhe: {float(row.get('Höhe'))} mm"

        rows.append({
            "Positionsbezeichnung": pos_label,
            "Titel": row.get("Titel", ""),
            "Beschreibung": row.get("Beschreibung", ""),
            "Menge": "" if is_alternative else row.get("Menge", ""),
            "Preis": row.get("Preis", 0.0),
            "Gesamtpreis": None if is_alternative else row.get("Gesamtpreis", 0.0),
            "image": image_data,
            "Alternative": is_alternative,
            "Abmessungen": abmessungen
        })

    df_render = pd.DataFrame(rows)
    df_render["Alternative"] = df_render["Alternative"].fillna(False).astype(bool)
    filtered_df = df_render[~df_render["Alternative"]]  # exclude alternatives
    netto = filtered_df["Gesamtpreis"].sum()
    rabatt_num = (netto * rabatt) / 100
    mwst = netto * 0.19 if if_mwst else 0
    brutto = netto - rabatt_num + mwst
    customer = customer_df.drop(columns=["Angebots_ID"])
    env = Environment(loader=BaseLoader())
    env.filters['german_currency'] = format_german_currency
    template = env.from_string(template_type)

    html = template.render(
        angebot_id=customer_df.iloc[0]["Angebots_ID"],
        kunde=customer.iloc[0],
        products=rows,
        netto=netto,
        mwst=mwst,
        brutto=brutto,
        rabatt=rabatt,
        rabatt_num=rabatt_num,
        payment_details=payment_details,
        logo_base64=encode_logo_as_base64_png(),
        aktuelles_datum=datetime.today().strftime("%d.%m.%y"),
        if_mwst=if_mwst,
        atu=atu
    )

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf", dir="/tmp") as tmp_file:
        HTML(string=html).write_pdf(tmp_file.name)
        return tmp_file.name