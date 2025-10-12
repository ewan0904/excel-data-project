import streamlit as st
st.set_page_config(layout="wide")
from utils.scraping import *
from utils.pdf_generator import *
from utils.auth import *
from utils.db import *
from utils.initialization import initialize_session_state_angebot_erstellen

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
        })

# ----------------
# --- Frontend ---
# ----------------
st.header("Angebot erstellen")

# -----------------
# --- Main Page ---
# -----------------

# --- Kundeninformationen ---
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

# ---------------
# --- Sidebar ---
# ---------------

# --- Datenbank Speicherung ---
st.sidebar.write("**Datenbank**")
if st.sidebar.button("💾 In Datenbank speichern"):

    # Make all Alternative values False by default
    #st.session_state["product_df_1"]['Alternative'] = st.session_state["product_df_1"]['Alternative'].fillna(False).astype(bool)

    post_customer_offer(
        customer=st.session_state["customer_information_1"],
        )
    reset() # Resets it, so the user has to use the second tab to further work on the offer
    st.rerun()
    st.success("✅ Angebot wurde erfolgreich gespeichert.")

# Button to log out

st.sidebar.markdown("<hr style='margin: 2px 0;'>", unsafe_allow_html=True)
if st.sidebar.button("Logout"):
    logout()
