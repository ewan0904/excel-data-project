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
from utils.excel_generator import generate_excel_file
from concurrent.futures import ThreadPoolExecutor, as_completed
from assets.html_structure import get_angebot_template, get_auftrag_template, get_short_angebot_template, get_angebot_wo_price_template

# Authentication
require_login()

# --- Session State Initialization ---
initialize_session_state_angebot_suchen()

# ------------------------
# --- Helper Functions ---
# ------------------------
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
        "images_2": {},
        "rabatt": 0,
        "payment_details": "",
        "mwst": True,
        "atu": ""
        })

def pdf_preview(file_path):
    st.subheader("PDF-Vorschau")
    pdf_viewer(
        file_path,
        height=1000,
        viewer_align="center",
        show_page_separator=True
    )

 # Parallel image fetching

def fetch_image(art_nr):
    try:
        image_bytes = get_image(art_nr)
        image = Image.open(BytesIO(image_bytes))
        return art_nr, image
    except Exception:
        return art_nr, None  # Optional: log error

# -----------------
# --- Main Page ---
# -----------------
st.header("Wähle einen Eintrag aus:")

col1, col2 = st.columns([5, 3])
with col1:
    # Add a label column for display
    st.session_state["all_invoices_df"]["label"] = st.session_state["all_invoices_df"].apply(lambda row: f'{row["offer_id"]} | {row["company"]} | {row["first_name"]} {row["surname"]}', axis=1)

    # Create options to choose from, the first one does not represent an offer
    options = ["-- Bitte auswählen --"] + st.session_state["all_invoices_df"]["label"].tolist()

    # Only reset if selected_label isn't initialized at all
    if "selected_label" not in st.session_state:
        st.session_state["selected_label"] = "-- Bitte auswählen --"
    elif st.session_state["selected_label"] not in options:
        st.warning("Das ausgewählte Angebot existiert nicht mehr. Auswahl wurde zurückgesetzt.")
        st.session_state["selected_label"] = "-- Bitte auswählen --"

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
        payment_info, st.session_state["product_df_2"] = get_invoice(selected_invoice_row.iloc[0]['invoice_id'])
        st.session_state["rabatt"] = payment_info.get("rabatt", 0)
        st.session_state["bei_auftrag"] = payment_info.get("bei_auftrag", "")
        st.session_state["bei_lieferung"] = payment_info.get("bei_lieferung", "")
        st.session_state["mwst"] = payment_info.get("mwst", True)
        st.session_state["atu"] = payment_info.get("atu", "")

        # Fetch images and store them in session_state
        art_nrs = st.session_state["product_df_2"]["Art_Nr"].tolist()
        st.session_state["images_2"] = {}
        with ThreadPoolExecutor(max_workers=20) as executor:
            results = executor.map(fetch_image, art_nrs)

        for art_nr, image in results:
            st.session_state["images_2"][art_nr] = image

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
            kunden_button = st.form_submit_button("Kunden-Informationen speichern")

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
    with st.expander("➕📦 **Produkte hinzufügen**"):
        with st.form("url_form_2"):
            urls = st.text_area("Alle Produkt-Links hier einfügen.", height=150, key="url_input_2")
            submitted = st.form_submit_button("Produkte hinzufügen")

        if submitted:
            extracted_urls = extract_urls(urls)
            if extracted_urls:
                if "product_df_2" not in st.session_state:
                    st.session_state["product_df_2"] = pd.DataFrame()

                start_pos = len(st.session_state["product_df_2"]) + 1
                total = len(extracted_urls)
                product_bar = st.progress(0, text=f"🔄 0 / {total} Produkte wurden verarbeitet...")

                futures = []
                with ThreadPoolExecutor(max_workers=10) as ex:
                    for i, url in enumerate(extracted_urls, start=1):
                        idx = start_pos + i - 1
                        futures.append(ex.submit(process_url, url, idx))  # df_id = 1
                    
                    results, failed = [], []
                    for done, fut in enumerate(as_completed(futures), start=1):
                        res = fut.result()
                        results.append(res)
                        if not res["ok"]:
                            failed.append((res["url"], res.get("err")))
                        product_bar.progress(int(done / total * 100),
                                    text=f"🔄 {done} / {total} Produkte wurden verarbeitet...")

                time.sleep(0.2)
                product_bar.empty()

                # write rows in order of idx
                rows = [r for r in results if r["ok"] and r["row"] is not None]
                if rows:
                    new_df = pd.DataFrame([r["row"] for r in rows])
                    st.session_state["product_df_2"] = (
                        pd.concat([st.session_state["product_df_2"], new_df])
                        .sort_values("Position").reset_index(drop=True)
                    )
                
                # Image processing
                todo = [
                        (r["row"].get("Art_Nr"), r["image_url"])
                        for r in results
                        if r["ok"] and r["row"] and r["image_url"]
                        and r["row"].get("Art_Nr") not in st.session_state["images_2"]
                    ]
                image_bar = st.progress(0, text=f"🔄 0 / {total} Produktbilder wurden verarbeitet...")
                with ThreadPoolExecutor(max_workers=10) as ex:
                    futures = [ex.submit(process_image, art, url) for art, url in todo]

                    for done, fut in enumerate(as_completed(futures), start=1):
                        art_nr, img = fut.result()
                        if img is not None:
                            # ✅ safe: update session only in main thread
                            st.session_state["images_2"][art_nr] = img
                        else:
                            st.session_state["images_2"][art_nr] = Image.open("assets/logo.png")
                        image_bar.progress(int(done / total * 100), text=f"🔄 {done} / {total} Produktbilder wurden verarbeitet...")


                if failed:
                    st.warning("Einige Links konnten nicht verarbeitet werden:")

                st.session_state.clear_url_input_2 = True
                st.rerun()

    # --- Produkt-Tabelle Bearbeiten ---
    with st.expander("✏️📦 **Produkte bearbeiten**"):
        editable_columns = ["Position", "2. Position", "Art_Nr", "Titel", "Beschreibung", "Menge", "Preis", "Gesamtpreis", "Hersteller", "Breite", "Tiefe", "Höhe", "Alternative"]

        # Ensure Menge is float
        if "Menge" in st.session_state["product_df_2"].columns:
            st.session_state["product_df_2"]["Menge"] = (pd.to_numeric(st.session_state["product_df_2"]["Menge"], errors="coerce").astype(float))

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
                "2. Position": column_config.NumberColumn("2. Position"),
                "Breite": column_config.NumberColumn("Breite"),
                "Tiefe": column_config.NumberColumn("Tiefe"),
                "Höhe": column_config.NumberColumn("Höhe")
            },
            key="editable_products_2"
        )

        col1, col2, col3 = st.columns([3, 2, 7])
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
                        db_image = get_image(art_nr)
                        if db_image:
                            try:
                                st.session_state['images_2'][art_nr] = Image.open(BytesIO(db_image))
                            except Exception:
                                st.session_state['images_2'][art_nr] = Image.open("assets/logo.png")
                        else:
                            st.session_state['images_2'][art_nr] = Image.open("assets/logo.png")

                st.session_state["product_df_2"] = edited_df

                # Delete the images that are not being used anymore
                valid_artnrs = set(st.session_state["product_df_2"]["Art_Nr"])
                for image in list(st.session_state['images_2'].keys()):
                    if image not in valid_artnrs:
                        del st.session_state['images_2'][image]
                st.rerun()

        with col2:
            if st.button("🔀 Tabelle sortieren"):
                sorted_df = st.session_state["product_df_2"].sort_values(
                    by=["Position", "2. Position"], na_position="last"
                ).reset_index(drop=True)
                st.session_state["product_df_2"] = sorted_df
                st.rerun()

        with col3:
            if st.button("➕ IP/TK/MK hinzufügen"):
                pos_id = st.session_state["product_df_2"]["Position"].max()
                ip_tk_mk_df = pd.DataFrame([
                    {
                        "Position": pos_id + 1,
                        "2. Position": None,
                        "Art_Nr": "IP",
                        "Titel": "Installationsplan",
                        "Beschreibung": "Erstellung eines Installationsplans für die\nPositionierung der erforderlichen Anschlüsse\nAnfahrten durch unseren Außendienst zum Objekt\nwerden nach Absprache und Aufwand berechnet.",
                        "Menge": 1,
                        "Preis": 0.0,
                        "Gesamtpreis": 0.0,
                        "Hersteller": "",
                        "Alternative": False,
                        "Breite": None,
                        "Tiefe": None,
                        "Höhe": None
                    },
                    {
                        "Position": pos_id + 2,
                        "2. Position": None,
                        "Art_Nr": "TK",
                        "Titel": "Lieferkosten",
                        "Beschreibung": "Lieferanschrift in DE",
                        "Menge": 1,
                        "Preis": 0.0,
                        "Gesamtpreis": 0.0,
                        "Hersteller": "",
                        "Alternative": False,
                        "Breite": None,
                        "Tiefe": None,
                        "Höhe": None
                    },
                    {
                        "Position": pos_id + 3,
                        "2. Position": None,
                        "Art_Nr": "MK",
                        "Titel": "Montagekosten",
                        "Beschreibung": "Anfahrt & Montage\nÜbernachtungskosten werden gesondert abgerechnet",
                        "Menge": 1,
                        "Preis": 0.0,
                        "Gesamtpreis": 0.0,
                        "Hersteller": "",
                        "Alternative": False,
                        "Breite": None,
                        "Tiefe": None,
                        "Höhe": None
                    }
                ])
                st.session_state["product_df_2"] = pd.concat([st.session_state["product_df_2"], ip_tk_mk_df], ignore_index=True)
                st.rerun()

    # --- Produktbilder Anzeigen / Hochladen ---
    with st.expander("✏️📸 **Produktbilder bearbeiten**", expanded=False):
        for i, row in st.session_state["product_df_2"].iterrows():
            art_nr = row.get("Art_Nr")
            st.write("---")
            cols = st.columns([3, 5])
            with cols[0]:
                if art_nr in st.session_state["images_2"]:
                    st.image(st.session_state["images_2"][art_nr], width=250)

            with cols[1]:
                st.markdown(f"""
            <div style='font-size:22px'>
            <strong>Position:</strong> {row['Position']},&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<strong>Art_Nr:</strong> {row['Art_Nr']}<br>
            <strong>Titel:</strong> {row['Titel']}
            </div>
            """, unsafe_allow_html=True)
                uploaded_file = st.file_uploader("Bild ersetzen", type=["png", "jpg", "jpeg"], key=f"as_file_{art_nr}{i}")
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

    with st.expander("🏷️ **Zahlungs-Einstellungen**"):
        with st.form("Zahlungen speichern"):
            rabatt = st.number_input("Rabatt (z.B. 10 für 10%)", value=float(st.session_state["rabatt"]), step=0.1, format="%0.1f")
            mwst_included = st.checkbox("Mwst. mit berechnen?", value=st.session_state["mwst"])
            atu_nummer = st.text_input("ATU-Nummer", value=st.session_state["atu"])
            payment_details = st.text_area("Wie viel bei Lieferung und Zahlung? (Falls nichts angegeben, steht bei den Zahlungsbedingungen: Vorkasse)", value=st.session_state["payment_details"])
            zahlungs_button = st.form_submit_button("Zahlungen-Einstellungen speichern")

            if zahlungs_button:
                st.session_state["rabatt"] = rabatt
                st.session_state["payment_details"] = payment_details
                st.session_state["mwst"] = mwst_included
                st.session_state["atu"] = atu_nummer
            
                with st.spinner():
                    st.success("Zahlungs-Einstellungen gespeichert!")


    # ---------------
    # --- Sidebar ---
    # ---------------

    # --- Angebot-PDF Erstellung ---
    st.sidebar.subheader("Angebot-Erstellung")
    if st.sidebar.button("📄 Angebot anzeigen"):
        try:
            pdf_path = build_pdf(
                product_df=st.session_state["product_df_2"],
                customer_df=pd.DataFrame([st.session_state["customer_information_2"]]),
                custom_images=st.session_state["images_2"],
                template_type=get_angebot_template(),
                rabatt=st.session_state["rabatt"],
                payment_details = st.session_state["payment_details"],
                if_mwst=st.session_state["mwst"],
                atu=st.session_state["atu"]
            )
            st.session_state["pdf_angebot"] = pdf_path
            st.success("✅ PDF wurde erfolgreich erstellt.")
            pdf_preview(pdf_path)
        except ValueError as e:
            st.error(f"❌ {e}")
    
    # --- Angebot-PDF Download
    if st.session_state.get("pdf_angebot"):
        file_name = f"angebot_{st.session_state['customer_information_2']['Firma']}_{st.session_state['customer_information_2']['Angebots_ID']}.pdf"
        with open(st.session_state["pdf_angebot"], "rb") as f:
            st.sidebar.download_button(
                label="⬇️ Angebot herunterladen",
                data=f,
                file_name=file_name,
                mime="application/pdf"
            )

    st.sidebar.markdown("<hr style='margin: 2px 0;'>", unsafe_allow_html=True)
    
    # --- Angebot ohne Preise-PDF Erstellung ---
    st.sidebar.subheader("Angebot ohne Preise")
    if st.sidebar.button("📄 Angebot ohne Preise anzeigen"):
        try:
            pdf_path = build_pdf(
                product_df=st.session_state["product_df_2"],
                customer_df=pd.DataFrame([st.session_state["customer_information_2"]]),
                custom_images=st.session_state["images_2"],
                template_type=get_angebot_wo_price_template(),
                rabatt=st.session_state["rabatt"],
                payment_details = st.session_state["payment_details"],
                if_mwst=st.session_state["mwst"],
                atu=st.session_state["atu"]
            )
            st.session_state["pdf_angebot_wo_price"] = pdf_path
            st.success("✅ PDF wurde erfolgreich erstellt.")
            pdf_preview(pdf_path)
        except ValueError as e:
            st.error(f"❌ {e}")

    # --- Angebot ohne Preise-PDF Download
    if st.session_state.get("pdf_angebot_wo_price"):
        file_name = f"angebot_ohne_preise_{st.session_state['customer_information_2']['Firma']}_{st.session_state['customer_information_2']['Angebots_ID']}.pdf"
        with open(st.session_state["pdf_angebot_wo_price"], "rb") as f:
            st.sidebar.download_button(
                label="⬇️ Angebot herunterladen",
                data=f,
                file_name=file_name,
                mime="application/pdf"
            )

    st.sidebar.markdown("<hr style='margin: 2px 0;'>", unsafe_allow_html=True)
    

    # --- Auftrag-PDF Erstellung ---
    st.sidebar.subheader("Auftrag-Erstellung")
    if st.sidebar.button("📄 Auftrag anzeigen"):
        try:
            payment_details = st.session_state["payment_details"].replace('\n', '<br>')
            pdf_path = build_pdf(
                product_df=st.session_state["product_df_2"],
                customer_df=pd.DataFrame([st.session_state["customer_information_2"]]),
                custom_images=st.session_state["images_2"],
                template_type=get_auftrag_template(),
                rabatt=st.session_state["rabatt"],
                payment_details=payment_details,
                if_mwst=st.session_state["mwst"],
                atu=st.session_state["atu"]
            )
            st.session_state["pdf_auftrag"] = pdf_path
            st.success("✅ PDF wurde erfolgreich erstellt.")
            pdf_preview(pdf_path)
        except ValueError as e:
            st.error(f"❌ {e}")
    # --- Auftrag-PDF Download ---
    if st.session_state.get("pdf_auftrag"):
        file_name = f"auftrag_{st.session_state['customer_information_2']['Firma']}_{st.session_state['customer_information_2']['Angebots_ID']}.pdf"
        with open(st.session_state["pdf_auftrag"], "rb") as f:
            st.sidebar.download_button(
                label="⬇️ Auftrag herunterladen",
                data=f,
                file_name=file_name,
                mime="application/pdf"
            )
    
    st.sidebar.markdown("<hr style='margin: 2px 0;'>", unsafe_allow_html=True)

    # --- Kurzes Angebot Erstellung ---
    st.sidebar.subheader("Kurzes Angebot")
    if st.sidebar.button("📄 Kurzes Angebot anzeigen"):
        try:
            pdf_path = build_pdf(
                product_df=st.session_state["product_df_2"],
                customer_df=pd.DataFrame([st.session_state["customer_information_2"]]),
                custom_images=st.session_state["images_2"],
                template_type=get_short_angebot_template(),
                rabatt=st.session_state["rabatt"],
                payment_details = st.session_state["payment_details"],
                if_mwst=st.session_state["mwst"],
                atu=st.session_state["atu"]
            )
            st.session_state["pdf_short"] = pdf_path
            st.success("✅ PDF wurde erfolgreich erstellt.")
            pdf_preview(pdf_path)
        except ValueError as e:
            st.error(f"❌ {e}")

    # --- Kurzes-PDF Download
    if st.session_state.get("pdf_short"):
        file_name = f"angebot_kurz_{st.session_state['customer_information_2']['Firma']}_{st.session_state['customer_information_2']['Angebots_ID']}.pdf"
        with open(st.session_state["pdf_short"], "rb") as f:
            st.sidebar.download_button(
                label="⬇️ Kurzes Angebot herunterladen",
                data=f,
                file_name=file_name,
                mime="application/pdf"
            )
    st.sidebar.markdown("<hr style='margin: 2px 0;'>", unsafe_allow_html=True)

    # --- Excel Download ---
    st.sidebar.subheader("Excel")
    if st.sidebar.button("📊 Excel-Datei erstellen"):
        buffer = generate_excel_file(st.session_state["product_df_2"])

        st.sidebar.download_button(
            label="📥 Excel-Datei herunterladen",
            data=buffer,
            file_name=f"excel_liste.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    st.sidebar.markdown("<hr style='margin: 2px 0;'>", unsafe_allow_html=True)

    # --- Datenbank Speicherung ---
    st.sidebar.subheader("Datenbank")
    if st.sidebar.button("💾 In Datenbank speichern"):
        # Make all Alternative values False by default
        st.session_state["product_df_2"]['Alternative'] = st.session_state["product_df_2"]['Alternative'].fillna(False).astype(bool)

        put_offer(
            customer=st.session_state["customer_information_2"],
            products=st.session_state["product_df_2"],
            images=st.session_state["images_2"],
            angebots_id=selected_invoice_row.iloc[0]['invoice_id'],
            customer_id=selected_invoice_row.iloc[0]["customer_id"],
            )
        st.success("✅ Angebot wurde erfolgreich gespeichert.")

    if st.sidebar.button("📄 Angebot duplizieren"):
        post_duplicate_offer(
            customer=st.session_state["customer_information_2"],
            products=st.session_state["product_df_2"]
            )
        reset() # Resets it, so the user has to use the second tab to further work on the offer
        st.session_state["selected_label"] = "-- Bitte auswählen --"

        # 🔄 Reload updated invoice list
        st.session_state["all_invoices_df"] = pd.DataFrame(get_all_invoices())
        st.session_state["all_invoices_df"]["label"] = st.session_state["all_invoices_df"].apply(
            lambda row: f'{row["offer_id"]} | {row["company"]} | {row["first_name"]} {row["surname"]}', axis=1)

        st.rerun()
        st.success("✅ Angebot wurde erfolgreich dupliziert.")

    with st.sidebar.popover("❌ Eintrag löschen"):
            st.markdown("""
                Die Löschung eines Angebots ist permanent,<br>
                <b>willst du fortfahren?</b>
                """, unsafe_allow_html=True
            )

            if st.button("❌ Löschen"):
                delete_offer(st.session_state["all_invoices_df"][st.session_state["all_invoices_df"]["label"] == st.session_state["selected_label"]].iloc[0]['invoice_id'])

                # Clear and reset session state
                reset()
                st.session_state["selected_label"] = "-- Bitte auswählen --"

                # 🔄 Reload updated invoice list
                st.session_state["all_invoices_df"] = pd.DataFrame(get_all_invoices())
                st.session_state["all_invoices_df"]["label"] = st.session_state["all_invoices_df"].apply(
                    lambda row: f'{row["offer_id"]} | {row["company"]} | {row["first_name"]} {row["surname"]}', axis=1)

                st.rerun()

    st.sidebar.markdown("<hr style='margin: 2px 0;'>", unsafe_allow_html=True)
    if st.sidebar.button("Logout"):
        logout()
