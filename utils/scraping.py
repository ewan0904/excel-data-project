import requests
from bs4 import BeautifulSoup, NavigableString
import streamlit as st
import re
import pandas as pd
from rembg import remove
from io import BytesIO
from PIL import Image
from utils.db import *
from utils.initialization import *

# --- Session State Initialization ---
initialize_session_state_angebot_erstellen()
initialize_session_state_angebot_suchen()
initialize_session_state_produkt_hinzufügen()

# ---------------
# API - Usage ---
# ---------------
def get_soup(url):
    """
    Retrieves the HTML content of a webpage using Zyte API with browser rendering.

    Args:
        url (str): The URL of the webpage to extract.

    Returns:
        str: The HTML content of the page.
    """
    api_response = requests.post(
        "https://api.zyte.com/v1/extract",
        auth=(st.secrets['ZYTE_API_KEY'], ""),
        json={
            "url": f"{url}",
            "browserHtml": True,
        },
    )
    return api_response.json()["browserHtml"]

# ------------------------
# --- Helper functions ---
# ------------------------
def auto_crop_image_with_rembg(image_url):
    """
    Downloads an image and removes its background using the rembg library.
    Automatically crops the result to remove transparent edges.

    Args:
        image_url (str): The URL of the image to process.

    Returns:
        BytesIO or None: A buffer containing the cropped image, or None if failed.
    """
    try:
        response = requests.get(image_url)
        img = Image.open(BytesIO(response.content)).convert("RGBA")

        result = remove(img)
        bbox = result.getbbox()
        if bbox:
            cropped = result.crop(bbox)

            # Create white background and paste cropped image
            bg = Image.new("RGB", cropped.size, (255, 255, 255))
            bg.paste(cropped.convert("RGB"), mask=cropped.split()[3])  # Use alpha as mask

            buffer = BytesIO()
            bg.save(buffer, format="JPEG")  # <-- Save as JPEG
            buffer.seek(0)
            return buffer
    except Exception as e:
        print(f"AI-Cropping failed: {e}")
    return None

def extract_urls(text):
    """
    Extracts all URLs from a block of text.

    Args:
        text (str): The input text that may contain URLs.

    Returns:
        list[str]: A list of extracted URLs.
    """
    text = text.replace('\r', '\n').replace('\u2028', '\n').replace('\u2029', '\n').replace('\xa0', '').strip()
    split_text = re.split(r'(https?://)', text)
    urls = []
    for i in range(1, len(split_text), 2):
        full_url = split_text[i] + split_text[i+1].split()[0]
        urls.append(full_url.strip())
    return urls

# -------------------------------------
# --- Helper Functions - Extraction ---
# -------------------------------------
def get_ggm_description(soup):
    """
    Parses structured text from the GGM product description HTML.

    Args:
        soup (BeautifulSoup): The BeautifulSoup object containing HTML content.

    Returns:
        str: A cleaned and formatted product description.
    """
    desc_div = soup.find('div', class_='ggmDescription')
    description = ''
    for element in desc_div.find_all(['p', 'ul']):
        if element.name == 'p':
            strong = element.find('strong')
            if strong:
                if description == '':
                    description += f"{strong.get_text(strip=True)}:\n"
                else:
                    description += f"\n{strong.get_text(strip=True)}:\n"
        elif element.name == 'ul':
            for li in element.find_all('li'):
                li_text = li.get_text(strip=True)
                description += f"  • {li_text}\n"

    abmessungen = {}
    technical_div = soup.find('div', {'class': 'ggmTechnical'})
    # Loop through table rows in the ggmTechnical div
    for row in technical_div.find_all('tr'):
        th = row.find('th')
        td = row.find('td')
        
        if th and td:
            label = th.get_text(strip=True)
            value = td.get_text(strip=True)
            value = value.replace(" mm", "").replace(".", "")
            
            if "Höhe" in label:
                abmessungen[label] = value
            elif "Breite" in label:
                abmessungen[label] = value
            elif "Tiefe" in label:
                abmessungen[label] = value

    return description.strip(), abmessungen

def get_gh_description(soup):
    """
    Extracts the product description from a GastroHero product page.

    Args:
        soup (BeautifulSoup): The BeautifulSoup object containing HTML content.

    Returns:
        str: A formatted string with the product description.
    """
    desc_container = soup.find("div", {"data-tracking": "product.tab-container.description"})
    if not desc_container:
        return "Description not found"

    tab_content = desc_container.select_one(".tab-content--have-gradient")
    if not tab_content:
        return ""

    description = ""
    skip_next_ul = False
    found_advantages = False

    for tag in tab_content.find_all(["p", "ul"]):
        text = tag.get_text(strip=True)
        text_lower = text.lower()

        # Check for "Produktvorteile im Überblick"
        if "produktvorteile im überblick" in text_lower:
            found_advantages = True
            skip_next_ul = True  # skip the list that follows
            continue

        # If we're skipping the <ul> that immediately follows the heading
        if skip_next_ul and tag.name == "ul":
            skip_next_ul = False  # skip this one and stop skipping
            continue

        # If it's before the "Produktvorteile" section, ignore
        if not found_advantages:
            continue

        # Otherwise, keep the content
        if tag.name == "p" and text:
            if description == "":
                description += f"{text}"
            else:
                description += f"\n{text}"
        elif tag.name == "ul":
            description += "\n" + "\n".join(f"• {li.get_text(strip=True)}" for li in tag.find_all("li"))
            description += "\n"

    # Abmessungen
    abmessungen = {}
    dimension_div = soup.find('div', {'data-tracking': 'product.tab-container.attributes'})

    # Loop through table rows to find the Maße label
    for row in dimension_div.find_all('tr', class_='product-attribute-table-row'):
        label = row.find('th')
        value = row.find('td')
        
        if label and value:
            label = label.get_text(strip=True)
            value = value.get_text(strip=True)

            if "maße" in label.lower():
                parts = [p.strip() for p in value.split('x')]
                abmessungen = {
                    "Breite": parts[0],
                    "Tiefe": parts[1],
                    "Höhe": parts[2]
                }
                break

    return description.strip(), abmessungen

def get_nc_description(soup):
    soup = soup.find('div', {'class': 'tab-menu--product js--tab-menu'})

    description = "Beschreibung\n"
    abmessungen = {}

    # 1 Beschreibung
    # product_description = soup.find('div', {'class': 'product--description'})
    product_description = soup.select_one('.product--description > ul')
    product_description_without_hinweis = product_description.find_all('li')
    for item in product_description_without_hinweis:
        description += f'• {item.get_text(strip=True)} \n'

    # 2 Produktdetails
    description += "\nProduktdetails\n"
    product_details = soup.find('div', {'class': 'nc-table-container is-full'})
    # Each detail seems to be structured in sub-divs
    details = product_details.find_all('div', recursive=False)

    # Extracting textual information clearly
    for detail in details:
        # Find key-value pairs
        label = detail.find('span', {'class': 'nc-table-title'})
        value = detail.find('span', {'class': 'nc-table-value'})
        if label and value:
            description += f"• {label.get_text(strip=True)} {value.get_text(strip=True)} \n"

    # 3 Abmessungen
    description += "\nAbmessungen\n"
    all_details = soup.find_all('div', {'class': 'nc-table-container is-full'})

    if len(all_details) >= 2:
        dimension_details = all_details[1].find_all('div', recursive=False)
        for dimension in dimension_details:
            label = dimension.find('span', {'class': 'nc-table-title'})
            value = dimension.find('span', {'class': 'nc-table-value'})
            if label and value:
                label_text = label.get_text(strip=True)
                value_text = value.get_text(strip=True)
                description += f"• {label_text} {value_text} \n"
                if "außen" in label_text.lower():
                    abmessungen[label_text] = value_text
    
    return description.strip(), abmessungen

def get_sg_information(soup):
    description = ""
    abmessungen = {}
    keywords = ['Breite', 'Tiefe', 'Höhe']

    # Get the table with the information
    table = soup.find('table', id='product-attribute-specs-table')

    # Loop through each row
    for row in table.find_all('tr'):
        label = row.find('th', class_='col label')
        value = row.find('td', class_='col data')

        if label and value:
            label_text = label.get_text(strip=True)
            value_text = value.get_text(strip=True)
            description += f'• {label_text}: {value_text} \n'
            if any(keyword in label_text for keyword in keywords):
                abmessungen[label_text] = value_text

    return description.strip(), abmessungen

# ----------------------------------
# --- Data Extraction for GGM/GH/NC ---
# ----------------------------------
def find_ggm_information(url, position, products, images, usage):
    """
    Scrapes product information from a GGM website and stores it in session state.

    Args:
        url (str): The URL of the product page.
        position (int): The product's position in the offer.
        products (str): The session key name for the product DataFrame.
        images (str): The session key name for the product images.
        usage (int): If 1, override with database values when available.
    """
    api_soup = get_soup(url)
    soup = BeautifulSoup(api_soup, 'html.parser')

    # Article
    article_div = soup.find('div', {'class': 'text-sm font-light text-[#332e2e]'})
    article_number = article_div.text if article_div else ''
    artnr_match = re.search(r'Art\.-Nr\.\s*([\S\s]+)', article_number)
    article_number = artnr_match.group(1).strip() if artnr_match else None

    # Title
    title_div = soup.find('h1')
    title = title_div.text.strip() if title_div else ''

    # Description
    description, abmessungen = get_ggm_description(soup)

    # Price
    price_span = soup.find('span', class_=lambda c: c and 'product-text-shadow' in c)
    price_text = price_span.text.strip() if price_span else '0'
    price_match = re.search(r'(\d{1,3}(?:\.\d{3})*,\d{2})', price_text)
    price = price_match.group(1) if price_match else '0'
    price_float = float(price.replace('.', '').replace(',', '.'))

    # Hersteller
    hersteller = 'GGM'

    # Ask database
    if usage == 1:
        product_db_data = get_product(article_number)
        if product_db_data:
            title = product_db_data.get("Titel")
            description = product_db_data.get("Beschreibung")
            hersteller = product_db_data.get("Hersteller")

        new_row = {
            'Position': position,
            '2. Position': '',
            'Art_Nr': article_number,
            'Titel': title,
            'Beschreibung': description,
            'Menge': 1,
            'Preis': price_float,
            'Gesamtpreis': price_float,
            'Hersteller': hersteller,
            'Alternative': False,
            'Breite': int(abmessungen.get('Breite')) if abmessungen.get('Breite') else None,
            'Tiefe': int(abmessungen.get('Tiefe')) if abmessungen.get('Tiefe') else None,
            'Höhe': int(abmessungen.get('Höhe')) if abmessungen.get('Höhe') else None,
            'Url': url
        }

    elif usage == 0:
        new_row = {
            "Art_Nr": article_number,
            "Titel": title,
            "Beschreibung": description,
            "Hersteller": hersteller,
            "Preis": None,
            "Alternative": False,
            'Breite': int(abmessungen.get('Breite')) if abmessungen.get('Breite') else None,
            'Tiefe': int(abmessungen.get('Tiefe')) if abmessungen.get('Tiefe') else None,
            'Höhe': int(abmessungen.get('Höhe')) if abmessungen.get('Höhe') else None,
            'Url': url
        }

    # Image
    image_tag = soup.find('div', {"class": "object-cover lg:cursor-zoom-in"}).find('img', src=lambda x: x and 'ggm.bynder.com' in x)
    image_url = image_tag.get('src') if image_tag else ''

    # Auto-crop and save custom image
    if new_row['Art_Nr'] not in st.session_state.get(f"images_{images}", {}):
        db_image = get_image(new_row['Art_Nr'])
        if db_image:
            image = Image.open(BytesIO(db_image))
            st.session_state[f"images_{images}"][new_row['Art_Nr']] = image
        else:
            image = auto_crop_image_with_rembg(image_url)
            if image:
                st.session_state[f"images_{images}"][new_row['Art_Nr']] = image

    # Save row
    new_df = pd.DataFrame([new_row])
    key = f"product_df_{products}"

    if st.session_state.get(key) is None or st.session_state[key].empty:
        st.session_state[key] = new_df.copy()

    else:
        existing_df = st.session_state[key]
        if (not new_df.empty):
            st.session_state[key] = pd.concat([existing_df, new_df], ignore_index=True)

def find_gh_information(url, position, products, images, usage):
    """
    Scrapes product information from a GastroHero product page and stores it in session state.

    Args:
        url (str): The URL of the product page.
        position (int): The product's position in the offer.
        products (str): The session key name for the product DataFrame.
        images (str): The session key name for the product images.
        usage (int): If 1, override with database values when available.
    """
    api_soup = get_soup(url)
    soup = BeautifulSoup(api_soup, 'html.parser')

    article_div = soup.find('span', {'class': 'inner-sku'})
    article_number = article_div.text.strip() if article_div else ''

    title_div = soup.find('h1')
    title = title_div.text.strip() if title_div else ''

    description_text, abmessungen = get_gh_description(soup)

    price_div = soup.find('div', class_='buy-box-price__display')

    price_raw = None

    # Look for strings directly under the main div (not inside inner <div>, <span>, etc.)
    for child in price_div.children:
        if isinstance(child, NavigableString):
            text = child.strip()
            if '€' in text:
                price_raw = text
                break  # Stop at the first matching outer price

    # Extract numeric value
    if price_raw:
        match = re.search(r'[\d.,]+', price_raw)
        if match:
            price_str = match.group(0)
            price_float = float(price_str.replace('.', '').replace(',', '.'))
        else:
            price_float = None
    else:
        price_float = None

    # Hersteller
    hersteller = 'GH'

    # Ask database
    if usage == 1:
        product_db_data = get_product(article_number)
        if product_db_data:
            title = product_db_data.get("Titel")
            description_text = product_db_data.get("Beschreibung")
            hersteller = product_db_data.get("Hersteller")

        new_row = {
            'Position': position,
            '2. Position': '',
            'Art_Nr': article_number,
            'Titel': title,
            'Beschreibung': description_text,
            'Menge': 1,
            'Preis': price_float,
            'Gesamtpreis': price_float,
            'Hersteller': hersteller,
            'Alternative': False,            
            'Breite': int(abmessungen.get('Breite')) if abmessungen.get('Breite') else None,
            'Tiefe': int(abmessungen.get('Tiefe')) if abmessungen.get('Tiefe') else None,
            'Höhe': int(abmessungen.get('Höhe')) if abmessungen.get('Höhe') else None,
            'Url': url
        }

    elif usage == 0:
        new_row = {
            "Art_Nr": article_number,
            "Titel": title,
            "Beschreibung": description_text,
            "Hersteller": hersteller,
            "Preis": None,
            "Alternative": False, # Indicate GGM/GH scraped product, instead of self-filled product
            'Breite': int(abmessungen.get('Breite')) if abmessungen.get('Breite') else None,
            'Tiefe': int(abmessungen.get('Tiefe')) if abmessungen.get('Tiefe') else None,
            'Höhe': int(abmessungen.get('Höhe')) if abmessungen.get('Höhe') else None,
            'Url': url
        }

    image_tag = soup.find('div', {"class": "preview"}).find('img', src=lambda x: x and 'api.gastro-hero.de' in x)
    image_url = image_tag.get('src') if image_tag else ''
    # Auto-crop and save custom image
    if new_row['Art_Nr'] not in st.session_state.get(f"images_{images}", {}):
        db_image = get_image(new_row['Art_Nr'])
        if db_image:
            image = Image.open(BytesIO(db_image))
            st.session_state[f"images_{images}"][new_row['Art_Nr']] = image
        else:
            image = auto_crop_image_with_rembg(image_url)
            if image:
                st.session_state[f"images_{images}"][new_row['Art_Nr']] = image

    # Save row
    new_df = pd.DataFrame([new_row])
    key = f"product_df_{products}"

    if st.session_state.get(key) is None or st.session_state[key].empty:
        st.session_state[key] = new_df.copy()

    else:
        existing_df = st.session_state[key]
        if (not new_df.empty):
            st.session_state[key] = pd.concat([existing_df, new_df], ignore_index=True)

def find_nc_information(url, position, products, images, usage):
    """
    Scrapes product information from a NordCap product page and stores it in session state.

    Args:
        url (str): The URL of the product page.
        position (int): The product's position in the offer.
        products (str): The session key name for the product DataFrame.
        images (str): The session key name for the product images.
        usage (int): If 1, override with database values when available.
    """

    # Get the content of the page of the url
    api_soup = get_soup(url)
    soup = BeautifulSoup(api_soup, 'html.parser')

    # Article Number
    article_div = soup.find('span', {'class': 'entry--content'})
    article_number = article_div.text.strip() if article_div else ''

    # Title
    title_div = soup.find('h1', {'class': 'product--title'})
    title = ' '.join(title_div.stripped_strings) if title_div else ''

    # Description
    description_text, abmessungen = get_nc_description(soup)

    # Hersteller
    hersteller = 'NC'

    # Price
    price_div = soup.find('span', {'class': 'price--content content--default'})
    price_meta = price_div.find('meta', {'itemprop': 'price'})
    price = price_meta['content'] if price_meta else None
    price_float = float(price) if price else 0

    # Image
    image_div = soup.find('span', {'class': 'image--media'}).find('img', src=lambda x: x and 'nordcap.de' in x)
    image_url = image_div.get('src') if image_div else ''

    # Ask database
    if usage == 1:
        product_db_data = get_product(article_number)
        if product_db_data:
            title = product_db_data.get("Titel")
            description_text = product_db_data.get("Beschreibung")
            hersteller = product_db_data.get("Hersteller")

        new_row = {
            'Position': position,
            '2. Position': '',
            'Art_Nr': article_number,
            'Titel': title,
            'Beschreibung': description_text,
            'Menge': 1,
            'Preis': price_float,
            'Gesamtpreis': price_float,
            'Hersteller': hersteller,
            'Alternative': False,
            'Breite': int(abmessungen.get('Breite außen:')) if abmessungen.get('Breite außen:') else None,
            'Tiefe': int(abmessungen.get('Tiefe außen:')) if abmessungen.get('Tiefe außen:') else None,
            'Höhe': int(abmessungen.get('Höhe außen:')) if abmessungen.get('Höhe außen:') else None,
            'Url': url
        }

    elif usage == 0:
        new_row = {
            "Art_Nr": article_number,
            "Titel": title,
            "Beschreibung": description_text,
            "Hersteller": hersteller,
            "Preis": None,
            "Alternative": False, # Indicate GGM/GH scraped product, instead of self-filled product
            'Breite': int(abmessungen.get('Breite außen:')) if abmessungen.get('Breite außen:') else None,
            'Tiefe': int(abmessungen.get('Tiefe außen:')) if abmessungen.get('Tiefe außen:') else None,
            'Höhe': int(abmessungen.get('Höhe außen:')) if abmessungen.get('Höhe außen:') else None,
            'Url': url
        }

    # Auto-crop and save custom image
    if new_row['Art_Nr'] not in st.session_state.get(f"images_{images}", {}):
        db_image = get_image(new_row['Art_Nr'])
        if db_image:
            image = Image.open(BytesIO(db_image))
            st.session_state[f"images_{images}"][new_row['Art_Nr']] = image
        else:
            image = auto_crop_image_with_rembg(image_url)
            if image:
                st.session_state[f"images_{images}"][new_row['Art_Nr']] = image

    # Save row
    new_df = pd.DataFrame([new_row])
    key = f"product_df_{products}"

    if st.session_state.get(key) is None or st.session_state[key].empty:
        st.session_state[key] = new_df.copy()

    else:
        existing_df = st.session_state[key]
        if (not new_df.empty):
            st.session_state[key] = pd.concat([existing_df, new_df], ignore_index=True)

def find_sg_information(url, position, products, images, usage):
    api_soup = get_soup('https://www.stalgast.de/bx10580f-warmeunterschrank-boxversion-2-0-mit-schiebeturen-sockelbau-1000x540x660-mm.html')
    soup = BeautifulSoup(api_soup, 'html.parser')

    # Article Number
    article_number = ""
    article_div = soup.find('div', {'class': 'additional-attributes-wrapper table-wrapper main-info-data'})

    for p in article_div.find_all('p'):
        if "artikelnummer" in p.get_text(strip=True).lower():
            artikel_p = p
            break

    if artikel_p:
        article_number = artikel_p.find('b').text.strip()

    # Title 
    title_h1 = soup.find('h1', {'class': 'page-title'})
    title_span = title_h1.find('span', {'class': 'base', 'data-ui-id': 'page-title-wrapper'})
    title = title_span.get_text(strip=True)

    # Description
    description, abmessungen = get_sg_information(soup)

    # Hersteller
    hersteller = 'SG'

    # Price
    price_div = soup.find('div', class_='product-info-price')
    meta_number = price_div.find('meta', attrs={'content': True})
    price_value = meta_number['content']
    price_float = float(price_value)

    # Image
    image_div = soup.find('div', {'class': 'fotorama__stage__frame fotorama__active fotorama_vertical_ratio fotorama__loaded fotorama__loaded--img'})
    image_src = image_div.find('img', src=lambda x: x and 'stalgast.de' in x)
    image_url = image_src.get('src') if image_src else ''

    # Ask database
    if usage == 1:
        product_db_data = get_product(article_number)
        if product_db_data:
            title = product_db_data.get("Titel")
            description = product_db_data.get("Beschreibung")
            hersteller = product_db_data.get("Hersteller")

        new_row = {
            'Position': position,
            '2. Position': '',
            'Art_Nr': article_number,
            'Titel': title,
            'Beschreibung': description,
            'Menge': 1,
            'Preis': price_float,
            'Gesamtpreis': price_float,
            'Hersteller': hersteller,
            'Alternative': False,
            'Breite': int(abmessungen.get('Breite [mm]')) if abmessungen.get('Breite [mm]') else None,
            'Tiefe': int(abmessungen.get('Tiefe [mm]')) if abmessungen.get('Tiefe [mm]') else None,
            'Höhe': int(abmessungen.get('Höhe [mm]')) if abmessungen.get('Höhe [mm]') else None,
            'Url': url
        }

    elif usage == 0:
        new_row = {
            "Art_Nr": article_number,
            "Titel": title,
            "Beschreibung": description,
            "Hersteller": hersteller,
            "Preis": None,
            "Alternative": False,
            'Breite': int(abmessungen.get('Breite [mm]')) if abmessungen.get('Breite [mm]') else None,
            'Tiefe': int(abmessungen.get('Tiefe [mm]')) if abmessungen.get('Tiefe [mm]') else None,
            'Höhe': int(abmessungen.get('Höhe [mm]')) if abmessungen.get('Höhe [mm]') else None,
            'Url': url
        }

    # Auto-crop and save custom image
    if new_row['Art_Nr'] not in st.session_state.get(f"images_{images}", {}):
        db_image = get_image(new_row['Art_Nr'])
        if db_image:
            image = Image.open(BytesIO(db_image))
            st.session_state[f"images_{images}"][new_row['Art_Nr']] = image
        else:
            image = auto_crop_image_with_rembg(image_url)
            if image:
                st.session_state[f"images_{images}"][new_row['Art_Nr']] = image

    # Save row
    new_df = pd.DataFrame([new_row])
    key = f"product_df_{products}"

    if st.session_state.get(key) is None or st.session_state[key].empty:
        st.session_state[key] = new_df.copy()

    else:
        existing_df = st.session_state[key]
        if (not new_df.empty):
            st.session_state[key] = pd.concat([existing_df, new_df], ignore_index=True)