import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore, storage
from io import BytesIO
from PIL import Image
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
import datetime

# ----------------------------
# --- Initialize Firestore ---
# ----------------------------
if not firebase_admin._apps:
    cred = credentials.Certificate(dict(st.secrets['FIREBASE_CREDENTIALS']))
    app = firebase_admin.initialize_app(cred,{
        'storageBucket': st.secrets['FIREBASE_BUCKET']
        })
    db = firestore.client()
else:
    db = firestore.client()

# ------------------------
# --- Helper Functions ---
# ------------------------
def to_jpeg_rgb(image: Image.Image) -> BytesIO:
    """
    Converts a PIL image to RGB JPEG with white background if transparency exists.

    Args:
        image (PIL.Image): The image to convert.

    Returns:
        BytesIO: A JPEG image in memory.
    """
    buffer = BytesIO()
    
    if image.mode in ("RGBA", "LA"):
        # Ensure image is in RGBA mode
        image = image.convert("RGBA")
        # Create white background image
        background = Image.new("RGBA", image.size, (255, 255, 255, 255))
        # Composite transparent image onto white background
        image = Image.alpha_composite(background, image)
    
    # Convert to RGB and save as JPEG
    image.convert("RGB").save(buffer, format="JPEG", quality=75)
    buffer.seek(0)
    return buffer

# ---------------------
# --- GET Firestore ---
# ---------------------
def get_customer(customer_id: str) -> dict:
    """
    Retrieves customer data from Firestore by customer ID.

    Args:
        customer_id (str): The ID of the customer.

    Returns:
        dict: Customer data.
    """
    customer_ref = db.collection("customers").document(customer_id)
    customer = customer_ref.get().to_dict()

    return customer

def get_invoice(angebots_id: str) -> pd.DataFrame:
    """
    Retrieves the products from a specific invoice in Firestore and returns them as a sorted DataFrame.

    Args:
        angebots_id (str): The ID of the invoice.

    Returns:
        pd.DataFrame: DataFrame containing sorted product details.
    """
    
    # Get all documents in the 'products' subcollection under this invoice
    invoice_ref = db.collection("invoices").document(angebots_id)
    products_ref = invoice_ref.collection("products")
    products_docs = products_ref.stream()

    # Parse product documents into a list of dictionaries
    product_list = []
    for doc in products_docs:
        product_data = doc.to_dict()
        product_list.append(product_data)

    # Convert to DataFrame
    products_df = pd.DataFrame(product_list)

    # Reorder columns
    ordered_columns = ["Position", "2. Position", "Art_Nr", "Titel", "Beschreibung", "Menge", "Preis", "Gesamtpreis", "Hersteller", "Alternative", "Breite", "Tiefe", "Höhe", "Url"]
    for col in ordered_columns:
        if col not in products_df.columns:
            products_df[col] = None  # or "", or 0, depending on your case
    
    products_df = products_df[ordered_columns]

    # Sort by Position and 2. Position
    products_df.sort_values(
        by=["Position", "2. Position"],
        ascending=[True, True],
        na_position="last",
        inplace=True
    )

    # Get payment details
    payment_info = invoice_ref.get().to_dict()

    return payment_info, products_df

def get_all_invoices():
    """
    Retrieves all invoices from Firestore and merges them with customer data.

    Returns:
        list[dict]: List of invoice entries with customer and invoice details.
    """
    invoices = list(db.collection("invoices").stream())
    data = []

    for invoice in invoices:
        invoice_data = invoice.to_dict()
        customer_id = invoice_data.get("Kunden_ID")
        offer_id = invoice_data.get("Angebots_ID")
        created_at = invoice_data.get("created_at")

        # Fetch corresponding customer
        customer_doc = db.collection("customers").document(customer_id).get()
        customer_data = customer_doc.to_dict() if customer_doc.exists else {}

        row = {
            "invoice_id": invoice.id,
            "offer_id": offer_id,
            "company": customer_data.get("Firma"),
            "first_name": customer_data.get("Vorname"),
            "surname": customer_data.get("Nachname"),
            "customer_id": customer_id,
            "created_at": created_at
        }
        data.append(row)

    # 🆕 Sort by created_at (newest first), fall back to None if missing
    data.sort(key=lambda x: x.get("created_at") or datetime.datetime.min, reverse=True)

    return data

def get_product(article_number):
    """
    Retrieves a specific product document from Firestore based on article number.

    Args:
        art_nr (str): Article number identifying the document.

    Returns:
        dict or None: Product data if found; otherwise, None.
    """
    doc = db.collection("products").where("Art_Nr", "==", article_number).limit(1).get()

    return doc[0].to_dict() if doc else None

def get_all_products():
    """
    Fetches all products from the 'products' collection in Firestore.

    Returns:
        list[dict]: List of product dictionaries with 'id', 'Art-Nr', 'Titel', and 'Hersteller'.
    """
    products = db.collection("products").stream()
    return [
        {
         "id": product.id, 
         "Art_Nr": product.to_dict().get("Art_Nr"), 
         "Titel": product.to_dict().get("Titel"),
         "Hersteller": product.to_dict().get("Hersteller"),
         "Alternative": product.to_dict().get("Alternative")
         }
        for product in products
    ]

def get_image(art_nr: str) -> bytes | None:
    """
    Retrieves an image from Firebase Storage based on the provided article number.

    Args:
        art_nr (str): Article number used to locate the image.

    Returns:
        bytes or None: Image data in bytes if found; otherwise, None.
    """
    bucket = storage.bucket()
    extensions = ["jpg", "png", "jpeg"]

    for ext in extensions:
        file_path = f"product_images/{art_nr}.{ext}"
        blob = bucket.blob(file_path)
        if blob.exists():
            return blob.download_as_bytes()
    return None

# ----------------------
# --- POST Firestore ---
# ----------------------
def post_image(products, images, max_threads=20):
    """
    Uploads images to Firebase Storage for each product in the given DataFrame using threading.

    Args:
        products (pd.DataFrame): DataFrame of products.
        images (dict): Dictionary of images keyed by article number.
        max_threads (int): Number of threads to use for parallel upload.
    """
    bucket = storage.bucket()

    def upload_image(product):
        art_nr = product['Art_Nr']
        image_data = images.get(art_nr)

        if image_data is None:
            return f"⚠️ Kein Bild für {art_nr} gefunden."

        blob = bucket.blob(f"product_images/{art_nr}.jpg")

        try:
            if isinstance(image_data, st.runtime.uploaded_file_manager.UploadedFile) or hasattr(image_data, "read"):
                image_data.seek(0)
                pil_image = Image.open(image_data)

            elif isinstance(image_data, Image.Image):
                pil_image = image_data

            elif isinstance(image_data, BytesIO):
                image_data.seek(0)
                pil_image = Image.open(image_data)

            else:
                return f"❌ {art_nr}: Bildtyp nicht unterstützt ({type(image_data)})."

            buffer = to_jpeg_rgb(pil_image)
            blob.upload_from_file(buffer, content_type="image/jpeg")
            return f"✅ {art_nr} hochgeladen"
        
        except Exception as e:
            return f"❌ Fehler beim Hochladen von {art_nr}: {e}"

    # Use ThreadPoolExecutor to upload images in parallel
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        executor.map(upload_image, products.to_dict(orient="records"))

def post_customer_offer(customer):
    """
    Uploads customer data to Firestore and returns the generated document ID.

    Args:
        customer (dict): Customer data.
    """
    # Store the information of customer and retrieve the auto-generated ID
    filtered_state = {k: v for k, v in customer.items()}
    _, customer_doc_ref = db.collection("customers").add(filtered_state)
    customer_doc_id = customer_doc_ref.id

    # Store the offer in the database
    angebot_Kunden_ID = {
        "Angebots_ID": customer["Angebots_ID"],
        "Kunden_ID": customer_doc_id,
        "rabatt": 0,
        "payment_details": "",
        "mwst": True,
        "atu": "",
        "created_at": firestore.SERVER_TIMESTAMP
    }

    db.collection("invoices").add(angebot_Kunden_ID)

def post_offer(customer, products, images):
    """
    Uploads a new offer to Firestore including customer info, product list, and images.

    Args:
        customer (dict): Customer data including Angebots_ID.
        products (pd.DataFrame): DataFrame of products.
        images (dict): Dictionary of images keyed by article number.
    """
    # Store the information of customer and retrieve the auto-generated ID
    filtered_state = {k: v for k, v in customer.items()}
    _, customer_doc_ref = db.collection("customers").add(filtered_state)
    customer_doc_id = customer_doc_ref.id

    # Store the images in the database
    post_image(products, images)

    # Store the offer in the database
    angebot_Kunden_ID = {
        "Angebots_ID": customer["Angebots_ID"],
        "Kunden_ID": customer_doc_id,
        "rabatt": 0,
        "payment_details": "",
        "mwst": True,
        "atu": "",
        "created_at": firestore.SERVER_TIMESTAMP
    }
    _, angebot_doc_ref = db.collection("invoices").add(angebot_Kunden_ID)

    # Store the products of the offers as a subcollection
    for row in products.to_dict(orient="records"):
        # Ensure all values are Firestore-compatible
        clean_row = {k: (bool(v) if k == "Alternative" else v) for k, v in row.items()}
        
        # Add to subcollection "products" under the offer
        angebot_doc_ref.collection("products").add(clean_row)

def post_duplicate_offer(customer, products):
    """
    Makes a copy of an invoice and changes the Angebots_ID to a new one (.01).
    """
    # Determine the new Angebots_ID
    if "." in customer["Angebots_ID"]:
        base_id = customer["Angebots_ID"].split(".")[0]
    else:
        base_id = customer["Angebots_ID"]

    versions = [
        int(o["offer_id"].split(".")[1])
        for o in get_all_invoices()
        if o["offer_id"].startswith(base_id + ".") and o["offer_id"].split(".")[1].isdigit()
    ]

    next_version = max(versions, default=0) + 1
    new_angebot_id = f"{base_id}.{next_version:02d}"

    # Store the information of customer and retrieve the auto-generated ID
    customer["Angebots_ID"] = new_angebot_id
    filtered_state = {k: v for k, v in customer.items()}
    _, customer_doc_ref = db.collection("customers").add(filtered_state)
    customer_doc_id = customer_doc_ref.id


    # Store the offer in the database
    angebot_Kunden_ID = {
        "Angebots_ID": new_angebot_id,
        "Kunden_ID": customer_doc_id,
        "rabatt": 0,
        "payment_details": "",
        "mwst": True,
        "atu": "",
        "created_at": firestore.SERVER_TIMESTAMP
    }

    _, angebot_doc_ref = db.collection("invoices").add(angebot_Kunden_ID)

    # Store the products of the offers as a subcollection
    products_ref = angebot_doc_ref.collection("products")

    for row in products.to_dict(orient="records"):
        # Ensure all values are Firestore-compatible
        clean_row = {k: (bool(v) if k == "Alternative" else v) for k, v in row.items()}
        
        # Add updated subcollection "products" under the offer
        products_ref.add(clean_row)

# ---------------------
# --- PUT Firestore ---
# ---------------------
def put_product(product_df: pd.DataFrame):
    """
    Updates or inserts products in the Firestore 'products' collection based on a DataFrame.

    Args:
        product_df (pd.DataFrame): DataFrame containing product data to be synced with Firestore.
    """
    COLLECTION = "products"
    product_df['Alternative'] = product_df['Alternative'].fillna(True).astype(bool)

    for _, product in product_df.iterrows():
        art_nr = product['Art_Nr']
        data = {
            "Art_Nr": product['Art_Nr'],
            "Hersteller": product['Hersteller'],
            "Titel": product['Titel'],
            "Beschreibung": product['Beschreibung'],
            "Preis": product['Preis'],
            "Alternative": product['Alternative'],
            "Breite": product['Breite'],
            "Tiefe": product['Tiefe'],
            "Höhe": product['Höhe'],
            "Url": product['Url']
        }

         # Check if a product with the same Art-Nr exists
        query = db.collection(COLLECTION).where("Art_Nr", "==", art_nr).get()
        if query:
            # Document exists, update it
            doc_id = query[0].id
            db.collection(COLLECTION).document(doc_id).set(data)
        else:
            # Create a new document with auto-ID
            db.collection("products").add(data)

def put_offer(customer, products, images, angebots_id, customer_id):
    """
    Updates an existing offer with new customer data, product list, and images.

    Args:
        customer (dict): Customer data.
        products (pd.DataFrame): DataFrame of products.
        images (dict): Dictionary of images keyed by article number.
        angebots_id (str): ID of the offer.
        customer_id (str): ID of the customer.
    """
    # Store the information of customer and retrieve the auto-generated ID
    db.collection("customers").document(customer_id).set(customer)

    # Store the images in the database
    post_image(products, images)

    # Update standard invoice information
    db.collection("invoices").document(angebots_id).update({
        "Angebots_ID": st.session_state["customer_information_2"]["Angebots_ID"],
        "rabatt": st.session_state["rabatt"],
        "payment_details": st.session_state["payment_details"],
        "mwst": st.session_state["mwst"],
        "atu": st.session_state["atu"]
    })

    # Delete existing products subcollection
    products_ref = db.collection("invoices").document(angebots_id).collection("products")
    for doc in products_ref.stream():
        doc.reference.delete()

    # Store the products of the offers as a subcollection
    for row in products.to_dict(orient="records"):
        # Ensure all values are Firestore-compatible
        clean_row = {k: (bool(v) if k == "Alternative" else v) for k, v in row.items()}
        
        # Add updated subcollection "products" under the offer
        products_ref.add(clean_row)

# ------------------------
# --- UPDATE Firestore ---
# ------------------------
def update_product(doc_id, product_df):
    for _, product in product_df.iterrows():
        if "Preis" in product_df.columns:
            data = {
                "Art_Nr": product['Art_Nr'],
                "Hersteller": product['Hersteller'],
                "Titel": product['Titel'],
                "Beschreibung": product['Beschreibung'],
                "Preis": product['Preis'],
                "Alternative": product['Alternative'],
                "Breite": product['Breite'],
                "Tiefe": product['Tiefe'],
                "Höhe": product['Höhe'],
                "Url": product['Url']
            }
        else: 
            data = {
                "Art_Nr": product['Art_Nr'],
                "Hersteller": product['Hersteller'],
                "Titel": product['Titel'],
                "Beschreibung": product['Beschreibung'],
                "Alternative": product['Alternative'],
                "Breite": product['Breite'],
                "Tiefe": product['Tiefe'],
                "Höhe": product['Höhe'],
                "Url": product['Url']
            }
        print(data)

        db.collection("products").document(doc_id).set(data)

# ------------------------
# --- DELETE Firestore ---
# ------------------------

def delete_collection(coll_ref, batch_size=20):
    """
    Recursively delete documents in a Firestore collection in batches.
    """
    docs = coll_ref.limit(batch_size).stream()
    deleted = 0

    for doc in docs:
        doc.reference.delete()
        deleted += 1

    if deleted >= batch_size:
        return delete_collection(coll_ref, batch_size)

def delete_offer(invoice_id):
    # Retrieve the information of the invoice_id
    invoice_ref = db.collection("invoices").document(invoice_id)
    invoice = invoice_ref.get()
    data = invoice.to_dict()

    # Store the customer_ref to delete the customer information
    kunden_id = data['Kunden_ID']


    # Delete the customer using Kunden_ID
    customer_ref = db.collection("customers").document(kunden_id)
    customer_ref.delete()

    # Delete subcollections under invoice
    try:
        delete_collection(invoice_ref.collection("products"))
    except Exception as e:
        print(f"Error deleting subcollection 'products': {e}")

    # Delete the invoice
    invoice_ref.delete()
