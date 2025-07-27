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

    if "product_df_1" not in st.session_state:
        st.session_state["product_df_1"] = pd.DataFrame(columns=[
            'Position', '2. Position', 'Art_Nr', 'Titel', 'Beschreibung', 'Menge',
            'Preis', 'Gesamtpreis', 'Hersteller', 'Alternative'
        ])

    if "images_1" not in st.session_state:
        st.session_state["images_1"] = {}
    
    if "pdf_preview_1" not in st.session_state:
        st.session_state["pdf_preview_1"] = ""

    if "clear_url_input_1" not in st.session_state:
        st.session_state['clear_url_input_1'] = False

    if st.session_state['clear_url_input_1']:
        st.session_state['url_input_1'] = ""
        st.session_state['clear_url_input_1'] = False

    if "all_products_1" not in st.session_state:
        st.session_state["all_products_1"] = pd.DataFrame(get_all_products())
        st.session_state["all_products_1"] = st.session_state["all_products_1"][st.session_state["all_products_1"]["Alternative"]]
        st.session_state["all_products_1"]["label"] = st.session_state["all_products_1"].apply(lambda row: f"{row['Art_Nr']} | {row['Titel']} | {row['Hersteller']}", axis=1)

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
            'Position', '2. Position', 'Art_Nr', 'Titel', 'Beschreibung', 'Menge',
            'Preis', 'Gesamtpreis', 'Hersteller', 'Alternative'
        ])

    if "pdf_preview_2" not in st.session_state:
        st.session_state["pdf_preview_2"] = ""
    
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

    if "all_products_2" not in st.session_state:
        st.session_state["all_products_2"] = pd.DataFrame(get_all_products())
        st.session_state["all_products_2"] = st.session_state["all_products_2"][st.session_state["all_products_2"]["Alternative"]]
        st.session_state["all_products_2"]["label"] = st.session_state["all_products_2"].apply(lambda row: f"{row['Art_Nr']} | {row['Titel']} | {row['Hersteller']}", axis=1)


# --- Session_state for page 3: Produkt hinzufügen ---
def initialize_session_state_produkt_hinzufügen():
    """
    Initializes the session state for the third page: Produkt hinzufügen.
    """
    if "product_df_3" not in st.session_state:
        st.session_state["product_df_3"] = pd.DataFrame(columns=[
            'Art_Nr', 
            'Titel', 
            'Beschreibung',
            'Hersteller',
            'Preis',
            'Alternative'
        ])

    if "images_3" not in st.session_state:
        st.session_state["images_3"] = {}

    if "clear_url_input_3" not in st.session_state:
        st.session_state['clear_url_input_3'] = False

    if st.session_state['clear_url_input_3']:
        st.session_state['url_input_3'] = ""
        st.session_state['clear_url_input_3'] = False

    if "all_products_df" not in st.session_state:
        st.session_state["all_products_df"] = pd.DataFrame(get_all_products())

    if "product_label" not in st.session_state:
        st.session_state["product_label"] = "-- Bitte auswählen --"

    if "product_in_edit" not in st.session_state:
        st.session_state["product_in_edit"] = pd.DataFrame(columns=[
            "Art_Nr",
            "Titel",
            "Beschreibung",
            "Preis",
            "Hersteller",
            "Alternative"
        ])

    if "image_in_edit" not in st.session_state:
        st.session_state["image_in_edit"] = {}