import streamlit as st
import pandas as pd
from utils.db import *

# --- Session_state for the first page: Angebot erstellen ---
def initialize_session_state_angebot_erstellen():
    """
    Initializes the session state for the first page: Angebot erstellen.
    """
    if "customer_information_1" not in st.session_state:
        st.session_state["customer_information_1"] = {
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
        }

# --- Session_state for page 2: Angebot suchen ---
def initialize_session_state_angebot_suchen():
    """
    Initializes the session state for the second page: Angebot suchen.
    """
    if "customer_information_2" not in st.session_state:
        st.session_state["customer_information_2"] = {
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
        }

    if "product_df_2" not in st.session_state:
        st.session_state["product_df_2"] = pd.DataFrame(columns=[
            'Position', 
            '2. Position', 
            'Art_Nr', 
            'Titel', 
            'Beschreibung', 
            'Menge',
            'Preis', 
            'Gesamtpreis', 
            'Hersteller', 
            'Alternative',
            'Breite',
            'Tiefe',
            'Höhe',
            'Url'
        ])

    if "pdf_angebot" not in st.session_state:
        st.session_state["pdf_preview_2"] = ""
    
    if "pdf_auftrag" not in st.session_state:
        st.session_state["pdf_auftrag"] = ""

    if "pdf_short" not in st.session_state:
        st.session_state["pdf_short"] = ""

    if "pdf_angebot_wo_price" not in st.session_state:
        st.session_state["pdf_angebot_wo_price"] = ""

    if "images_2" not in st.session_state:
        st.session_state["images_2"] = {}
    
    if "all_invoices_df" not in st.session_state:
        st.session_state["all_invoices_df"] = pd.DataFrame(get_all_invoices())

    if "selected_label" not in st.session_state:
        st.session_state["selected_label"] = "-- Bitte auswählen --"

    if "clear_url_input_2" not in st.session_state:
        st.session_state['clear_url_input_2'] = False

    if st.session_state['clear_url_input_2']:
        st.session_state['url_input_2'] = ""
        st.session_state['clear_url_input_2'] = False

    if "rabatt" not in st.session_state:
        st.session_state["rabatt"] = 0

    if "payment_details" not in st.session_state:
        st.session_state["payment_details"] = ""
    
    if "mwst" not in st.session_state:
        st.session_state["mwst"] = True
    
    if "atu" not in st.session_state:
        st.session_state["atu"] = ""
