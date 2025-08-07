import streamlit as st
st.set_page_config(layout="wide")
from streamlit import column_config
from streamlit_pdf_viewer import pdf_viewer
import pandas as pd
import numpy as np
from PIL import Image
from utils.scraping import *
from utils.pdf_generator import *
from utils.auth import *
from utils.db import *
from utils.initialization import initialize_session_state_angebot_erstellen
import time

# --- Authentication ---
require_login()

# --- Session State Initialization ---
initialize_session_state_angebot_erstellen()

# --- Helper functions ---
def reset():
    st.session_state.update({
        'customer_information_1': {
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
        "product_df_1": st.session_state["product_df_1"].iloc[0:0],
        "images_1": {}
        })
    
def pdf_preview(file_path):
    st.subheader("PDF-Vorschau")
    pdf_viewer(
        file_path,
        height=1000,
        viewer_align="center",
        show_page_separator=True
    )

# ----------------
# --- Frontend ---
# ----------------
st.header("Angebot erstellen")

# -----------------
# --- Main Page ---
# -----------------

# --- Kundeninformationen ---
with st.expander("👨‍💼👩‍💼 **Kunden-Informationen**"):
    with st.form("Speichern"):
        anrede_optionen = ["Herr", "Frau"]
        anrede = st.radio("Anrede", anrede_optionen, index=anrede_optionen.index(st.session_state["customer_information_1"]["Anrede"]))
        vorname = st.text_input("Vorname", value=st.session_state["customer_information_1"]["Vorname"])
        nachname = st.text_input("Nachname", value=st.session_state["customer_information_1"]["Nachname"])
        firma = st.text_input("Firma", value=st.session_state["customer_information_1"]["Firma"])
        adresse = st.text_input("Adresse", value=st.session_state["customer_information_1"]["Adresse"])
        plz = st.text_input("PLZ", value=st.session_state["customer_information_1"]["PLZ"])
        ort = st.text_input("Ort", value=st.session_state["customer_information_1"]["Ort"])
        telefonnummer = st.text_input("Telefonnummer", value=st.session_state["customer_information_1"]["Telefonnummer"])
        email = st.text_input("E-Mail", value=st.session_state["customer_information_1"]["E_Mail"])
        angebots_id = st.text_input("Angebots-ID", value=st.session_state["customer_information_1"]["Angebots_ID"])
        kunden_button = st.form_submit_button("Kunden-Informationen Speichern")

        if kunden_button:
            if all([anrede, vorname, nachname, firma, adresse, plz, ort, angebots_id]):
                st.session_state["customer_information_1"]["Anrede"] = anrede
                st.session_state["customer_information_1"]["Vorname"] = vorname
                st.session_state["customer_information_1"]["Nachname"] = nachname
                st.session_state["customer_information_1"]["Firma"] = firma
                st.session_state["customer_information_1"]["Adresse"] = adresse
                st.session_state["customer_information_1"]["PLZ"] = plz
                st.session_state["customer_information_1"]["Ort"] = ort
                st.session_state["customer_information_1"]["Telefonnummer"] = telefonnummer
                st.session_state["customer_information_1"]["E_Mail"] = email
                st.session_state["customer_information_1"]["Angebots_ID"] = angebots_id

                with st.spinner():
                    st.success("Kunden-Informationen gespeichert!")
        else:
            st.warning("Bitte fülle alle Informationen aus.")

# --- Produkt-URL Eingabe + Scraping ---
with st.expander("➕📦 **GGM/GH/NC/SG Produkte hinzufügen**"):
    with st.form("url_form_1"):
        urls = st.text_area("Alle Produkt-Links hier einfügen.", height=150, key="url_input_1")
        submitted = st.form_submit_button("Produkte hinzufügen")

    if submitted:
        extracted_urls = extract_urls(urls)
        if extracted_urls:
            start_pos = len(st.session_state["product_df_1"]) + 1

            progress_text = f"🔄 0 / {len(extracted_urls)} Produkte wurden verarbeitet..."
            my_bar = st.progress(0, text=progress_text)

            total = len(extracted_urls)
            for i, url in enumerate(extracted_urls, start=1):
                idx = start_pos + i - 1

                if "gastro-hero" in url:
                    find_gh_information(url, idx, 1, 1, 1)
                elif "ggmgastro" in url:
                    find_ggm_information(url, idx, 1, 1, 1)
                elif "nordcap" in url:
                    find_nc_information(url, idx, 1, 1, 1)
                elif "stalgast" in url:
                    find_sg_information(url, idx, 1, 1, 1)

                # Update progress
                progress_text = f"🔄 {i} / {len(extracted_urls)} Produkte wurden verarbeitet..."
                my_bar.progress(int(i / total * 100), text=progress_text)

            time.sleep(0.3)
            my_bar.empty()

            st.session_state.clear_url_input_1 = True
            st.rerun()

# --- Produkt Selection from DB ---
with st.expander("➕📦 **Andere Produkte hinzufügen**"):
    db_product_col1, db_product_col2 = st.columns([5, 3])
    
    # Multi-Select to select items from the database
    with db_product_col1: 
        selected_db_products = st.multiselect("Produkte auswählen", st.session_state["all_products_1"]["label"])
        
    # Button to update the available products from the database
    with db_product_col2:
        st.write(
                """<style>
                [data-testid="stHorizontalBlock"] {
                    align-items: flex-end;
                }
                </style>
                """,
                unsafe_allow_html=True
                )
        
        st.button("🔄 Produkte aktualisieren")
        st.session_state["all_products_1"] = pd.DataFrame(get_all_products())
        st.session_state["all_products_1"] = st.session_state["all_products_1"][st.session_state["all_products_1"]["Alternative"]]
        st.session_state["all_products_1"]["label"] = st.session_state["all_products_1"].apply(lambda row: f"{row['Art_Nr']} | {row['Titel']} | {row['Hersteller']}", axis=1)
    
    
    # Button to add the products to the editing dataframe
    if st.button("Produkte hinzufügen", key="save_product_db_1"):
                for product_label in selected_db_products:
                    # Retrieve the product from the DB
                    doc_id = st.session_state["all_products_1"][st.session_state["all_products_1"]["label"] == product_label]["id"].iloc[0]
                    db_product = get_product(doc_id)
                    db_product['Alternative'] = False
                    #if db_product["Art_Nr"] not in st.session_state["product_df_1"]["Art_Nr"].values:

                    # Add the product to the product_df_1
                    st.session_state["product_df_1"] = pd.concat([st.session_state["product_df_1"], pd.DataFrame([db_product])], ignore_index=True)
                    db_image = get_image(db_product['Art_Nr'])

                    if db_image:
                        image = Image.open(BytesIO(db_image))
                        st.session_state[f"images_1"][db_product['Art_Nr']] = image

# --- Produkt-Tabelle Bearbeiten ---
with st.expander("✏️📦 **Produkte bearbeiten**"):
    editable_columns = ["Position", "2. Position", "Art_Nr", "Titel", "Beschreibung", "Menge", "Preis", "Gesamtpreis", "Hersteller", "Breite", "Tiefe", "Höhe", "Alternative"]
    edited_df = st.data_editor(
        st.session_state["product_df_1"].reset_index(drop=True),
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
            "2. Position": column_config.NumberColumn("2. Position"),
            "Breite": column_config.NumberColumn("Breite"),
            "Tiefe": column_config.NumberColumn("Tiefe"),
            "Höhe": column_config.NumberColumn("Höhe")
        },
        key="editable_products_1"
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

                if art_nr not in st.session_state['images_1']:
                    st.session_state['images_1'][art_nr] = Image.open("assets/logo.png")

            st.session_state["product_df_1"] = edited_df
            st.rerun()

    with col2:
        if st.button("🔀 Tabelle sortieren"):
            sorted_df = st.session_state["product_df_1"].sort_values(
                by=["Position", "2. Position"], na_position="last"
            ).reset_index(drop=True)
            st.session_state["product_df_1"] = sorted_df
            st.rerun()

# --- Produktbilder Anzeigen / Hochladen ---
with st.expander("✏️📸 **Produktbilder anzeigen / ändern**", expanded=False):
    for i, row in st.session_state["product_df_1"].iterrows():
        art_nr = row.get("Art_Nr")
        st.write("---")
        cols = st.columns([3, 5])
        with cols[0]:
            if art_nr in st.session_state["images_1"]:
                st.image(st.session_state["images_1"][art_nr], width=250)

        with cols[1]:
            st.markdown(f"""
            <div style='font-size:22px'>
            <strong>Position:</strong> {row['Position']},&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<strong>Art_Nr:</strong> {row['Art_Nr']}<br>
            <strong>Titel:</strong> {row['Titel']}
            </div>
            """, unsafe_allow_html=True)
            uploaded_file = st.file_uploader("Bild ersetzen", type=["png", "jpg", "jpeg"], key=f"ae_file_{art_nr}{i}")
            if uploaded_file:
                if st.button("💾 Bild speichern", key=f"save_img_{art_nr}"):
                    image = Image.open(uploaded_file)

                    # Handle transparency by compositing onto white background
                    if image.mode == "RGBA":
                        background = Image.new("RGB", image.size, (255, 255, 255))  # white background
                        background.paste(image, mask=image.split()[3])  # use alpha channel as mask
                        image = background
                    else:
                        image = image.convert("RGB")

                    buffer = BytesIO()
                    image.save(buffer, format="JPEG")
                    buffer.seek(0)

                    st.session_state["images_1"][art_nr] = Image.open(buffer)
                    st.rerun()

# ---------------
# --- Sidebar ---
# ---------------

# --- Datenbank Speicherung ---
st.sidebar.write("Datenbank")
if st.sidebar.button("💾 In Datenbank speichern"):

    # Make all Alternative values False by default
    st.session_state["product_df_1"]['Alternative'] = st.session_state["product_df_1"]['Alternative'].fillna(False).astype(bool)

    post_offer(
        customer=st.session_state["customer_information_1"],
        products=st.session_state["product_df_1"],
        images=st.session_state["images_1"]
        )
    reset() # Resets it, so the user has to use the second tab to further work on the offer
    st.rerun()
    st.success("✅ Angebot wurde erfolgreich gespeichert.")

# Button to log out

st.sidebar.markdown("<hr style='margin: 2px 0;'>", unsafe_allow_html=True)
if st.sidebar.button("Logout"):
    logout()
