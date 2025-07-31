import streamlit as st
from utils.auth import *
from utils.db import *
from utils.initialization import initialize_session_state_angebot_suchen
import pandas as pd
import numpy as np
from streamlit import column_config
from utils.scraping import *
import time
from utils.pdf_generator import *
from streamlit_pdf_viewer import pdf_viewer
import re
from PIL import Image

# Authentication
require_login()
if st.sidebar.button("Logout"):
    logout()

# --- Session State Initialization ---
initialize_session_state_angebot_suchen()

# ------------------------
# --- Helper Functions ---
# ------------------------

# --- Reset session_state ---
def reset():
    st.session_state.update({
        'customer_information_2': {
            "Anrede": "Herr",
            "Vorname": "",
            "Nachname": "",
            "Firma": "",
            "Adresse": "",
            "PLZ": "",
            "Ort": "",
            "Telefonnummer": "",
            "E_Mail": "",
            "Angebots_ID": ""
        },
        "product_df_2": st.session_state["product_df_2"].iloc[0:0],
        "images_2": {}
        })
    
# --- Preview PDF ---
def pdf_preview(file_path):
    st.subheader("PDF-Vorschau")
    pdf_viewer(
        file_path,
        height=1000,
        viewer_align="center",
        show_page_separator=True
    )

# Title of the page
st.header("Wähle ein Angebot aus:")

col1, col2 = st.columns([5, 3])
with col1:
    # Add a label column for display
    st.session_state["all_invoices_df"]["label"] = st.session_state["all_invoices_df"].apply(lambda row: f'{row["offer_id"]} | {row["company"]} | {row["first_name"]} {row["surname"]}', axis=1)

    # Create options to choose from, the first one does not represent an offer
    options = ["-- Bitte auswählen --"] + st.session_state["all_invoices_df"]["label"].tolist()

    # Selectbox for user to pick an invoice
    selected_label = st.selectbox("Angebot", options, index=options.index(st.session_state["selected_label"]))

with col2:
    st.write(
    """<style>
    [data-testid="stHorizontalBlock"] {
        align-items: flex-end;
    }
    </style>
    """,
    unsafe_allow_html=True
    )
    if st.button("🔄 Angebote aktualisieren"):
        st.session_state["all_invoices_df"] = pd.DataFrame(get_all_invoices())
        st.session_state["all_invoices_df"]["label"] = st.session_state["all_invoices_df"].apply(lambda row: f'{row["offer_id"]} | {row["company"]} | {row["first_name"]} {row["surname"]}', axis=1)



# Reset data if no data is selected
if selected_label == "-- Bitte auswählen --":
    st.session_state["selected_label"] = selected_label
    reset()

# If an invoice is selected
if selected_label != "-- Bitte auswählen --":
    # Load (new) invoice
    selected_invoice_row = st.session_state["all_invoices_df"][st.session_state["all_invoices_df"]["label"] == selected_label]
    if st.session_state["selected_label"] != selected_label:
        customer_db_information = get_customer(selected_invoice_row.iloc[0]["customer_id"])
        customer_db_information["Angebots_ID"] = selected_invoice_row.iloc[0]['offer_id']
        st.session_state["customer_information_2"] = customer_db_information
        st.session_state["product_df_2"] = get_invoice(selected_invoice_row.iloc[0]['invoice_id'])
        
        # Fetch images and store them in session_state
        for art_nr in st.session_state["product_df_2"]["Art_Nr"]:
            st.session_state["images_2"][art_nr] = Image.open(BytesIO(get_image(art_nr)))
        st.session_state["selected_label"] = selected_label

    st.write("---")

    # --- Main Page ---
    # --- Kundeninformationen ---
    with st.expander("👨‍💼👩‍💼 **Kunden-Informationen**"):
        with st.form("Speichern"):
            anrede_optionen = ["Herr", "Frau"]
            anrede = st.radio("Anrede", anrede_optionen, index=anrede_optionen.index(st.session_state["customer_information_2"]["Anrede"]))
            vorname = st.text_input("Vorname", value=st.session_state["customer_information_2"]["Vorname"])
            nachname = st.text_input("Nachname", value=st.session_state["customer_information_2"]["Nachname"])
            firma = st.text_input("Firma", value=st.session_state["customer_information_2"]["Firma"])
            adresse = st.text_input("Adresse", value=st.session_state["customer_information_2"]["Adresse"])
            plz = st.text_input("PLZ", value=st.session_state["customer_information_2"]["PLZ"])
            ort = st.text_input("Ort", value=st.session_state["customer_information_2"]["Ort"])
            telefonnummer = st.text_input("Telefonnummer", value=st.session_state["customer_information_2"]["Telefonnummer"])
            email = st.text_input("E-Mail", value=st.session_state["customer_information_2"]["E_Mail"])
            angebots_id = st.text_input("Angebots-ID", value=st.session_state["customer_information_2"]["Angebots_ID"])
            kunden_button = st.form_submit_button("Kunden-Informationen Speichern")

            if kunden_button:
                if all([anrede, vorname, nachname, firma, adresse, plz, ort, angebots_id]):
                    st.session_state["customer_information_2"]["Anrede"] = anrede
                    st.session_state["customer_information_2"]["Vorname"] = vorname
                    st.session_state["customer_information_2"]["Nachname"] = nachname
                    st.session_state["customer_information_2"]["Firma"] = firma
                    st.session_state["customer_information_2"]["Adresse"] = adresse
                    st.session_state["customer_information_2"]["PLZ"] = plz
                    st.session_state["customer_information_2"]["Ort"] = ort
                    st.session_state["customer_information_2"]["Telefonnummer"] = telefonnummer
                    st.session_state["customer_information_2"]["E_Mail"] = email
                    st.session_state["customer_information_2"]["Angebots_ID"] = angebots_id

                    with st.spinner():
                        st.success("Kunden-Informationen gespeichert!")
            else:
                st.warning("Bitte fülle alle Informationen aus.")

    # --- Produkt-URL Eingabe + Scraping ---  
    with st.expander("➕📦 **GGM/GH/NC Produkte hinzufügen**"):
        with st.form("url_form_2"):
            urls = st.text_area("Alle Produkt-Links hier einfügen.", height=150, key="url_input_2")
            submitted = st.form_submit_button("Produkte hinzufügen")

        if submitted:
            extracted_urls = extract_urls(urls)
            if extracted_urls:
                start_pos = len(st.session_state["product_df_2"]) + 1

                progress_text = f"🔄 0 / {len(extracted_urls)} Produkte wurden verarbeitet..."
                my_bar = st.progress(0, text=progress_text)

                total = len(extracted_urls)
                for i, url in enumerate(extracted_urls, start=1):
                    idx = start_pos + i - 1

                    if "gastro-hero" in url:
                        find_gh_information(url, idx, 2, 2, 1)
                    elif "ggmgastro" in url:
                        find_ggm_information(url, idx, 2, 2, 1)
                    elif "nordcap" in url:
                        find_nc_information(url, idx, 2, 2, 1)

                    # Update progress
                    progress_text = f"🔄 {i} / {len(extracted_urls)} Produkte wurden verarbeitet..."
                    my_bar.progress(int(i / total * 100), text=progress_text)

                time.sleep(0.3)
                my_bar.empty()

                st.session_state.clear_url_input_2 = True
                st.rerun()

    # --- Produkt Selection from DB ---
    with st.expander("➕📦 **Andere Produkte hinzufügen**"):
        db_product_col1, db_product_col2 = st.columns([5, 3])

        # Multi-Select to select the products from the DB
        with db_product_col1: 
            selected_db_products = st.multiselect("Produkte auswählen", st.session_state["all_products_2"]["label"])

        # Button to refresh the products fetched from the DB
        with db_product_col2:
            st.button("🔄 Produkte aktualisieren")
            st.session_state["all_products_2"] = pd.DataFrame(get_all_products())
            st.session_state["all_products_2"] = st.session_state["all_products_2"][st.session_state["all_products_2"]["Alternative"]]
            st.session_state["all_products_2"]["label"] = st.session_state["all_products_2"].apply(lambda row: f"{row['Art_Nr']} | {row['Titel']} | {row['Hersteller']}", axis=1)

        # Button to add products to the editing dataframe
        if st.button("Produkte hinzufügen", key="save_product_db_2"):
                    for product_label in selected_db_products:
                        # Retrieve the product from the DB
                        doc_id = st.session_state["all_products_2"][st.session_state["all_products_2"]["label"] == product_label]["id"].iloc[0]
                        db_product = get_product(doc_id)
                        if db_product["Art_Nr"] not in st.session_state["product_df_2"]["Art_Nr"].values:

                            # Add the product to the product_df_2
                            st.session_state["product_df_2"] = pd.concat([st.session_state["product_df_2"], pd.DataFrame([db_product])], ignore_index=True)
                            db_image = get_image(db_product['Art_Nr'])

                            if db_image:
                                image = Image.open(BytesIO(db_image))
                                st.session_state[f"images_2"][db_product['Art_Nr']] = image

    # --- Produkt-Tabelle Bearbeiten ---
    with st.expander("✏️📦 **Produkte bearbeiten**"):
        editable_columns = ["Position", "2. Position", "Art_Nr", "Titel", "Beschreibung", "Menge", "Preis", "Gesamtpreis", "Hersteller", "Alternative"]
        edited_df = st.data_editor(
            st.session_state["product_df_2"].reset_index(drop=True),
            use_container_width=True,
            num_rows="dynamic",
            column_order=editable_columns,
            column_config={
                "Titel": column_config.TextColumn("Titel", width="medium"),
                "Beschreibung": column_config.TextColumn("Beschreibung", width="large"),
                "Menge": column_config.NumberColumn("Menge"),
                "Preis": column_config.NumberColumn("Preis"),
                "Gesamtpreis": column_config.NumberColumn("Gesamtpreis", disabled=True),
                "Position": column_config.NumberColumn("Position"),
                "2. Position": column_config.NumberColumn("2. Position")
            },
            key="editable_products_2"
        )

        col1, col2, _ = st.columns([3, 2, 7])
        with col1:
            if st.button("💾 Änderungen speichern"):
                # Check if there are any missing or empty values in the required columns
                required_columns = ["Position", "Art_Nr", "Titel", "Preis"]

                # Strip whitespace and check for empty strings
                stripped = edited_df[required_columns].astype(str).apply(lambda col: col.str.strip())

                # Identify rows with missing or empty values
                missing_rows = edited_df[
                    edited_df[required_columns].isnull().any(axis=1) |
                    (stripped == "").any(axis=1)]

                if not missing_rows.empty:
                    st.error("❌ Einige Pflichtfelder (Position, Art_Nr, Titel, Menge) sind leer. Bitte ausfüllen.")
                    st.stop()
                
                # Calculate Gesamtpreis conditionally
                edited_df["Gesamtpreis"] = np.where(
                edited_df["Menge"].isna() | (edited_df["Menge"] == 0),
                edited_df["Preis"],                   # Use Preis if Menge is missing or zero
                edited_df["Menge"] * edited_df["Preis"]  # Otherwise calculate normally
                )
                for i, row in edited_df.iterrows():
                    art_nr = row.get("Art_Nr")

                    if art_nr not in st.session_state['images_2']:
                        st.session_state['images_2'][art_nr] = Image.open("assets/logo.png")

                st.session_state["product_df_2"] = edited_df
                st.rerun()

        with col2:
            if st.button("🔀 Tabelle sortieren"):
                sorted_df = st.session_state["product_df_2"].sort_values(
                    by=["Position", "2. Position"], na_position="last"
                ).reset_index(drop=True)
                st.session_state["product_df_2"] = sorted_df
                st.rerun()

    # --- Produktbilder Anzeigen / Hochladen ---
    with st.expander("✏️📸 **Produktbilder anzeigen / ändern**", expanded=False):
        for i, row in st.session_state["product_df_2"].iterrows():
            art_nr = row.get("Art_Nr")
            st.write("---")
            cols = st.columns([3, 5])
            with cols[0]:
                if art_nr in st.session_state["images_2"]:
                    st.image(st.session_state["images_2"][art_nr], width=250)

            with cols[1]:
                st.markdown(f"**{row['Titel']}**")
                uploaded_file = st.file_uploader("Bild ersetzen", type=["png", "jpg", "jpeg"], key=f"file_{art_nr}")
                if uploaded_file:
                    if st.button("💾 Bild speichern", key=f"save_img_{art_nr}"):
                        image = Image.open(uploaded_file)

                        # Handle transparency by compositing onto white background
                        if image.mode == "RGBA":
                            background = Image.new("RGB", image.size, (255, 255, 255))
                            background.paste(image, mask=image.split()[3])
                            image = background
                        else:
                            image = image.convert("RGB")

                        buffer = BytesIO()
                        image.save(buffer, format="JPEG")
                        buffer.seek(0)

                        st.session_state["images_2"][art_nr] = Image.open(buffer)
                        st.rerun()

    # --- Sidebar ---
    st.sidebar.subheader("Funktionen")
    # --- Neues Angebot Erstellen (Daten zurücksetzen) ---

    # --- PDF Erstellung ---
    if st.sidebar.button("📄 PDF anzeigen"):
        try:
            pdf_path = build_pdf(
                product_df=st.session_state["product_df_2"],
                customer_df=pd.DataFrame([st.session_state["customer_information_2"]]),
                custom_images=st.session_state["images_2"]
            )
            st.session_state["pdf_preview_2"] = pdf_path
            st.success("✅ PDF wurde erfolgreich erstellt.")
            pdf_preview(pdf_path)
        except ValueError as e:
            st.error(f"❌ {e}")

    # --- PDF Download
    if st.session_state.get("pdf_preview_2"):
        file_name = f"{st.session_state['customer_information_2']['Firma']}_{st.session_state['customer_information_2']['Angebots_ID']}.pdf"
        with open(st.session_state["pdf_preview_2"], "rb") as f:
            st.sidebar.download_button(
                label="⬇️ PDF herunterladen",
                data=f,
                file_name=file_name,
                mime="application/pdf"
            )


    # --- Datenbank Speicherung ---
    if st.sidebar.button("💾 In Datenbank speichern"):
        # Make all Alternative values False by default
        st.session_state["product_df_2"]['Alternative'] = st.session_state["product_df_2"]['Alternative'].fillna(False).astype(bool)

        put_offer(
            customer=st.session_state["customer_information_2"],
            products=st.session_state["product_df_2"],
            images=st.session_state["images_2"],
            angebots_id=selected_invoice_row.iloc[0]['invoice_id'],
            customer_id=selected_invoice_row.iloc[0]["customer_id"]
            )
        st.success("✅ Angebot wurde erfolgreich gespeichert.")