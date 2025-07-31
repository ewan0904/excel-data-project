import streamlit as st
from utils.auth import require_login, logout
import pandas as pd
from utils.db import *
from utils.initialization import initialize_session_state_produkt_hinzufügen
from utils.scraping import *
import time
from streamlit import column_config
import numpy as np

# --- Authentication ---
require_login()
if st.sidebar.button("Logout"):
    logout()

# --- Initialize Session State ---
initialize_session_state_produkt_hinzufügen()

# --- Reset product table ---
def reset_product_table():
    st.session_state.update({
        "product_df_3": st.session_state["product_df_3"].iloc[0:0],
        "images_3": {}
        })
    
def reset_product_edit():
    st.session_state.update({
        "product_in_edit": st.session_state["product_in_edit"].iloc[0:0],
        "image_in_edit": {}
    })

# --- Frontend ---
st.header("Neue GGM/GH Produkte hinzufügen")

# --- Produkt-URL Eingabe + Scraping ---
with st.expander("➕📦 **GGM/GH/NC Produkte hinzufügen**"):
    with st.form("url_form_3"):
        urls = st.text_area("Alle Produkt-Links hier einfügen.", height=150, key="url_input_3")
        submitted = st.form_submit_button("Produkte hinzufügen")

    if submitted:
        extracted_urls = extract_urls(urls)
        if extracted_urls:
            start_pos = len(st.session_state["product_df_3"]) + 1

            progress_text = f"🔄 0 / {len(extracted_urls)} Produkte wurden verarbeitet..."
            my_bar = st.progress(0, text=progress_text)

            total = len(extracted_urls)
            for i, url in enumerate(extracted_urls, start=1):
                idx = start_pos + i - 1

                if "gastro-hero" in url:
                    find_gh_information(url, idx, 3, 3, 0)
                elif "ggmgastro" in url:
                    find_ggm_information(url, idx, 3, 3, 0)
                elif "nordcap" in url:
                    find_nc_information(url, idx, 3, 3, 0)

                # Update progress
                progress_text = f"🔄 {i} / {len(extracted_urls)} Produkte wurden verarbeitet..."
                my_bar.progress(int(i / total * 100), text=progress_text)

            time.sleep(0.3)
            my_bar.empty()
            st.session_state.clear_url_input_3 = True
            st.rerun()

# --- Produkt-Tabelle Bearbeiten ---
with st.expander("✏️📦 **Produkte bearbeiten**"):
    editable_columns = ["Art_Nr", "Titel", "Beschreibung", "Preis", "Hersteller"]
    edited_df = st.data_editor(
        st.session_state["product_df_3"].reset_index(drop=True),
        use_container_width=True,
        num_rows="dynamic",
        column_order=editable_columns,
        column_config={
            "Titel": column_config.TextColumn("Titel", width="large"),
            "Beschreibung": column_config.TextColumn("Beschreibung", width="large"),
            "Preis": column_config.NumberColumn("Preis")
        },
        key="editable_products_3"
    )
    col1, col2, col3 = st.columns([3, 3, 3])
    with col1:
        if st.button("💾 Änderungen speichern"):
            # Check if there are any missing or empty values in the required columns
            required_columns = ["Art_Nr", "Titel"]

            # Strip whitespace and check for empty strings
            stripped = edited_df[required_columns].astype(str).apply(lambda col: col.str.strip())

            # Identify rows with missing or empty values
            missing_rows = edited_df[
                edited_df[required_columns].isnull().any(axis=1) |
                (stripped == "").any(axis=1)]

            if not missing_rows.empty:
                st.error("❌ Einige Pflichtfelder (Art_Nr, Titel) sind leer. Bitte ausfüllen.")
                st.stop()
            
            # Calculate Gesamtpreis conditionally
            for i, row in edited_df.iterrows():
                art_nr = row.get("Art_Nr")

                if art_nr not in st.session_state['images_3']:
                    st.session_state['images_3'][art_nr] = Image.open("assets/logo.png")

            st.session_state["product_df_3"] = edited_df
            st.rerun()
    with col2:
        if st.button("💾 In Datenbank speichern"):
            put_product(st.session_state["product_df_3"])
            post_image(st.session_state["product_df_3"], st.session_state["images_3"])

    with col3:
        if st.button("Tabelle leeren"):
            reset_product_table()
            st.rerun()

# --- Produktbilder Anzeigen / Hochladen ---
with st.expander("✏️📸 **Produktbilder anzeigen / ändern**", expanded=False):
    for i, row in st.session_state["product_df_3"].iterrows():
        art_nr = row.get("Art_Nr")
        st.write("---")
        cols = st.columns([3, 5])
        with cols[0]:
            if art_nr in st.session_state["images_3"]:
                st.image(st.session_state["images_3"][art_nr], width=250)

        with cols[1]:
            st.markdown(f"**{row['Titel']}**")
            uploaded_file = st.file_uploader("Bild ersetzen", type=["png", "jpg", "jpeg"], key=f"file_{art_nr}")
            if uploaded_file:
                if st.button("💾 Bild speichern", key=f"save_img_{art_nr}"):
                    st.session_state["images_3"][art_nr] = uploaded_file
                    st.rerun()


st.write("---")
# --- Bestehende Produkte Bearbeiten ---
st.header("Bestehende Produkte bearbeiten")

col1, col2 = st.columns([5, 3])
with col1:
    st.session_state["all_products_df"]["label"] = st.session_state["all_products_df"].apply(lambda row: f"{row['Art_Nr']} | {row['Titel']} | {row['Hersteller']}", axis=1)
    product_options = ["-- Bitte auswählen --"] + st.session_state["all_products_df"]["label"].tolist()
    product_label = st.selectbox("Alle Produkte", options=product_options, index=product_options.index(st.session_state["product_label"]))
 
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
    if st.button("🔄 Produkte aktualisieren"):
        st.session_state["all_products_df"] = pd.DataFrame(get_all_products())
        st.session_state["all_products_df"]["label"] = st.session_state["all_products_df"].apply(lambda row: f"{row['Art_Nr']} | {row['Titel']} | {row['Hersteller']}", axis=1)
        st.session_state["product_label"] = "-- Bitte auswählen --"

if product_label == "-- Bitte auswählen --":
    st.session_state["product_label"] = product_label
    reset_product_edit()

if product_label != "-- Bitte auswählen --":

    if st.session_state["product_label"] != product_label:
        art_nr = st.session_state["all_products_df"][st.session_state["all_products_df"]["label"] == product_label]["Art_Nr"].iloc[0]
        doc_id = st.session_state["all_products_df"][st.session_state["all_products_df"]["label"] == product_label]["id"].iloc[0]
        product = get_product(doc_id)
        st.session_state["product_in_edit"] = pd.DataFrame([product])
        st.session_state["product_label"] = product_label
        if art_nr not in st.session_state["image_in_edit"]:
            st.session_state["image_in_edit"][art_nr] = Image.open(BytesIO(get_image(art_nr)))
        
    art_nr = st.session_state["product_in_edit"].iloc[0]["Art_Nr"]
    product = st.session_state["product_in_edit"].iloc[0]
    doc_id = st.session_state["all_products_df"][st.session_state["all_products_df"]["label"] == product_label]["id"].iloc[0]

    with st.expander("✏️📦 **Produkt bearbeiten**", expanded=True):
        # --- TRUE ---
        if product["Alternative"] == True:
            editable_columns = ["Art_Nr", "Titel", "Beschreibung", "Preis", "Hersteller"]
            edited_df = st.data_editor(
                st.session_state["product_in_edit"].reset_index(drop=True),
                use_container_width=True,
                num_rows="fixed",
                column_order=editable_columns,
                column_config={
                    "Titel": column_config.TextColumn("Titel", width="large"),
                    "Beschreibung": column_config.TextColumn("Beschreibung", width="large"),
                    "Preis": column_config.NumberColumn("Preis")
                },
                key="editable_product_in_edit"
            )
        
            col1_true, col2_true, _ = st.columns([3, 3, 3])
            with col1_true:
                if st.button("💾 Änderungen speichern", key="product_in_edit_save"):
                    old_art_nr = st.session_state["product_in_edit"].iloc[0]["Art_Nr"]
                    st.session_state["product_in_edit"] = edited_df
                    existing_image = st.session_state["image_in_edit"][old_art_nr]
                    st.session_state["image_in_edit"] = {edited_df.iloc[0]["Art_Nr"]: existing_image}
                    st.rerun()

            with col2_true:
                if st.button("💾 In Datenbank speichern", key="db_save_false"):
                    st.session_state["product_in_edit"]['Alternative'] = st.session_state["product_in_edit"]['Alternative'].fillna(True).astype(bool)
                    update_product(doc_id, st.session_state["product_in_edit"])
                    post_image(st.session_state["product_in_edit"], st.session_state["image_in_edit"])

                    # Refresh product list with new data
                    all_products = get_all_products()
                    st.session_state["all_products_df"] = pd.DataFrame(all_products)
                    st.session_state["all_products_df"]["label"] = st.session_state["all_products_df"].apply(
                        lambda row: f"{row['Art_Nr']} | {row['Titel']} | {row['Hersteller']}", axis=1)
                    
                    # Re-Select the updated product based on doc_id
                    updated_row = st.session_state["all_products_df"][st.session_state["all_products_df"]["id"] == doc_id].iloc[0]
                    st.session_state["product_label"] = updated_row["label"]
                    existing_image = st.session_state["image_in_edit"][updated_row["Art_Nr"]]
                    st.session_state["image_in_edit"] = {updated_row["Art_Nr"]: existing_image}
        
        
        # --- FALSE ---
        if product["Alternative"] == False:
            editable_columns = ["Art_Nr", "Titel", "Beschreibung", "Hersteller"]
            edited_df = st.data_editor(
                st.session_state["product_in_edit"].reset_index(drop=True),
                use_container_width=True,
                num_rows="fixed",
                column_order=editable_columns,
                column_config={
                    "Titel": column_config.TextColumn("Titel", width="large"),
                    "Beschreibung": column_config.TextColumn("Beschreibung", width="large")
                },
                key="editable_product_in_edit"
            )
            col1_false, col2_false, _ = st.columns([3, 3, 3])
            with col1_false:
                if st.button("💾 Änderungen speichern", key="product_in_edit_save_2"):
                    old_art_nr = st.session_state["product_in_edit"].iloc[0]["Art_Nr"]
                    st.session_state["product_in_edit"] = edited_df
                    existing_image = st.session_state["image_in_edit"][old_art_nr]
                    st.session_state["image_in_edit"] = {edited_df.iloc[0]["Art_Nr"]: existing_image}
                    st.rerun()
            with col2_false:
                if st.button("💾 In Datenbank speichern", key="db_save_false"):
                    st.session_state["product_in_edit"]['Alternative'] = st.session_state["product_in_edit"]['Alternative'].fillna(True).astype(bool)
                    update_product(doc_id, st.session_state["product_in_edit"])
                    post_image(st.session_state["product_in_edit"], st.session_state["image_in_edit"])

                    # Refresh product list with new data
                    all_products = get_all_products()
                    st.session_state["all_products_df"] = pd.DataFrame(all_products)
                    st.session_state["all_products_df"]["label"] = st.session_state["all_products_df"].apply(
                        lambda row: f"{row['Art_Nr']} | {row['Titel']} | {row['Hersteller']}", axis=1)
                    
                    # Re-Select the updated product based on doc_id
                    updated_row = st.session_state["all_products_df"][st.session_state["all_products_df"]["id"] == doc_id].iloc[0]
                    st.session_state["product_label"] = updated_row["label"]
                    existing_image = st.session_state["image_in_edit"][updated_row["Art_Nr"]]
                    st.session_state["image_in_edit"] = {updated_row["Art_Nr"]: existing_image}


    # --- Produktbilder Anzeigen / Hochladen ---
    with st.expander("✏️📸 **Produktbilder anzeigen / ändern**", expanded=True):
            cols = st.columns([3, 5])
            with cols[0]:
                if art_nr in st.session_state["image_in_edit"]:
                    st.image(st.session_state["image_in_edit"][art_nr], width=250)

            with cols[1]:
                st.markdown(f"**{st.session_state['product_in_edit'].iloc[0]['Titel']}**")
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

                        st.session_state["images_in_edit"][art_nr] = Image.open(buffer)
                        st.rerun()

