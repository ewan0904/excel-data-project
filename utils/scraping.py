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
from datetime import date

# --- Session State Initialization ---
initialize_session_state_angebot_erstellen()
initialize_session_state_angebot_suchen()

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
def process_url(url, idx):
    try:
        row, image_url = "", ""
        if "gastro-hero.de" in url:
            row, image_url = find_gh_information(url, idx)
        elif "ggmgastro.com" in url:
            row, image_url = find_ggm_information(url, idx)
        elif "nordcap.de" in url:
            row, image_url = find_nc_information(url, idx)
        elif "stalgast.de" in url:
            row, image_url = find_sg_information(url, idx)
        elif "grimm-gastrobedarf.de" in url:
            row, image_url = find_gg_information(url, idx)
        elif "gastronomie-moebel.eu" in url:
            row, image_url = find_gm_information(url, idx)
        elif "stapelstuhl24.com" in url:
            row, image_url = find_s24_information(url, idx)
        elif "intergastro.de" in url:
            row, image_url = find_ig_information(url, idx)
        elif "gastrodax.de" in url:
            row, image_url = find_gdax_information(url, idx)
        return {"ok": True, "row": row, "image_url": image_url}
    except Exception as e:
        return {"ok": False, "idx": idx, "err": str(e), "url": url}

def process_image(art_nr, image_url):
    """
    Runs in a background thread: tries DB first, then cropping.
    Returns (art_nr, PIL.Image or None).
    """
    # 1) DB first
    db_image = get_image(art_nr)
    if db_image:
        try:
            return art_nr, Image.open(BytesIO(db_image))
        except Exception:
            pass

    # 2) Crop from remote
    try:
        img = auto_crop_image_with_rembg(image_url)
        return art_nr, img
    except Exception:
        return art_nr, None

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

# ----------------------------------
# ------------ SCRAPING ------------
# ----------------------------------
def find_ggm_information(url, position):
    """
    Scrapes product information from a GGM website and stores it in session state.

    Args:
        url (str): The URL of the product page.
        position (int): The product's position in the offer.
        products (str): The session key name for the product DataFrame.
        images (str): The session key name for the product images.
    """
    api_soup = get_soup(url)
    soup = BeautifulSoup(api_soup, 'html.parser')

    # ---------------- Article ----------------
    article_div = soup.find('div', {'class': 'text-sm font-light text-[#332e2e]'})
    if article_div:
        article_number = article_div.text
        if article_number:
            artnr_match = re.search(r'Art\.-Nr\.\s*([\S\s]+)', article_number)
            article_number = artnr_match.group(1).strip() if artnr_match else None

    # ---------------- Title ------------------
    title_h1 = soup.find('h1')
    title = title_h1.text.strip() if title_h1 else ''

    # ---------------- Description-------------
    description = ''
    desc_div = soup.find('div', class_='ggmDescription')
    if desc_div:
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
        description = description.strip()

    # ---------------- Abmessungen ------------
    abmessungen = {}
    technical_div = soup.find('div', {'class': 'ggmTechnical'})

    if technical_div:
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

    # ---------------- Price ------------------
    price_span = soup.find('span', class_=lambda c: c and 'product-text-shadow' in c)
    price_text = price_span.text.strip() if price_span else '0'
    price_match = re.search(r'(\d{1,3}(?:\.\d{3})*,\d{2})', price_text)
    price_raw = price_match.group(1) if price_match else '0'
    price = float(price_raw.replace('.', '').replace(',', '.'))

    # ---------------- Hersteller -------------
    hersteller = 'GGM'

    # ---------------- Create row -------------
    new_row = {
        'Position': position,
        '2. Position': '',
        'Art_Nr': article_number,
        'Titel': title,
        'Beschreibung': description,
        'Menge': 1,
        'Preis': price,
        'Gesamtpreis': price,
        'Hersteller': hersteller,
        'Alternative': False,
        'Breite': int(abmessungen.get('Breite')) if abmessungen.get('Breite') else None,
        'Tiefe': int(abmessungen.get('Tiefe')) if abmessungen.get('Tiefe') else None,
        'Höhe': int(abmessungen.get('Höhe')) if abmessungen.get('Höhe') else None,
        'Url': url
    }

    # ---------------- Image ------------------
    image_tag = soup.find('div', {"class": "object-cover lg:cursor-zoom-in"}).find('img', src=lambda x: x and 'ggm.bynder.com' in x)
    image_url = image_tag.get('src') if image_tag else ''

    return new_row, image_url

def find_gh_information(url, position):
    """
    Scrapes product information from a GastroHero product page and stores it in session state.

    Args:
        url (str): The URL of the product page.
        position (int): The product's position in the offer.
        products (str): The session key name for the product DataFrame.
        images (str): The session key name for the product images.
    """
    api_soup = get_soup(url)
    soup = BeautifulSoup(api_soup, 'html.parser')

    # ---------------- Article ----------------
    article_div = soup.find('span', {'class': 'inner-sku'})
    article_number = article_div.text.strip() if article_div else ''

    # ---------------- Title ------------------
    title_h1 = soup.find('h1')
    title = title_h1.text.strip() if title_h1 else ''

    # ---------------- Description ------------
    description = ""
    desc_container = soup.find("div", {"data-tracking": "product.tab-container.description"})
    if desc_container:

        tab_content = desc_container.select_one(".tab-content")

        if tab_content:
            skip_next_ul = False

            tags = tab_content.find_all(["strong", "ul"])
            for i, tag in enumerate(tags):
                # Check the next tag (if it exists)
                if i + 1 < len(tags):
                    next_tag = tags[i + 1]
                else:
                    next_tag = None

                text = tag.get_text(strip=True)
                text_lower = text.lower()
                
                # Skip certain sections based on keywords
                if next_tag and next_tag.name == "ul" and any(k in text_lower for k in ["produktvorteile im überblick", "hinweis"]):
                    skip_next_ul = True  # skip the list that follows
                    continue

                # Check for <strong> tags that are immediately followed by another <strong> or non-<ul> tag
                if tag.name == "strong" and next_tag and next_tag.name != "ul":
                    continue
                
                # Skip <strong> tags that contain "Hinweis"
                if tag.name == "strong" and "hinweis" in text_lower:
                    continue

                # Skip <strong> tags that are inside a <ul>
                if tag.name == "strong" and tag.find_parent("ul"):
                    continue  # ignore this <strong> because it's within a list

                if skip_next_ul and tag.name == "ul":
                    skip_next_ul = False  # skip this one and stop skipping
                    continue

                # Otherwise, keep the content
                if tag.name == "strong" and text:
                    if description == "":
                        description += f"{text}"
                    else:
                        description += f"\n{text}"
                elif tag.name == "ul":
                    description += "\n" + "\n".join(f"• {li.get_text(strip=True)}" for li in tag.find_all("li"))
                    description += "\n"
            description = description.strip()

    # ---------------- Abmessungen ------------
    abmessungen = {}
    dimension_div = soup.find('div', {'class': 'feature-list'})

    # Loop through table rows to find the Maße label
    for li in dimension_div.find_all('li'):
        li_text = li.get_text(strip=True)
        if "produktmaße" in li_text.lower():
            # Extract numbers using regex (e.g. 1316 x 885 x 710)
                match = re.search(r"(\d+)\s*x\s*(\d+)\s*x\s*(\d+)", li_text)
                if match:
                    breite, tiefe, höhe = match.groups()
                    abmessungen = {
                        "Breite": int(breite),
                        "Tiefe": int(tiefe),
                        "Höhe": int(höhe)
                    }   

    # ---------------- Price ------------------
    price_div = soup.find('div', class_='buy-box-price__display')
    price_raw = None
    price = None

    if price_div:
        for child in price_div.children:
            if isinstance(child, NavigableString):
                text = child.strip()
                if '€' in text:
                    price_raw = text
                    match = re.search(r'[\d.,]+', price_raw)
                    if match:
                        price_str = match.group(0)
                        price = float(price_str.replace('.', '').replace(',', '.'))
                    break

    # ---------------- Hersteller -------------
    hersteller = 'GH'

    # ---------------- Create row -------------
    new_row = {
        'Position': position,
        '2. Position': '',
        'Art_Nr': article_number,
        'Titel': title,
        'Beschreibung': description,
        'Menge': 1,
        'Preis': price,
        'Gesamtpreis': price,
        'Hersteller': hersteller,
        'Alternative': False,            
        'Breite': int(abmessungen.get('Breite')) if abmessungen.get('Breite') else None,
        'Tiefe': int(abmessungen.get('Tiefe')) if abmessungen.get('Tiefe') else None,
        'Höhe': int(abmessungen.get('Höhe')) if abmessungen.get('Höhe') else None,
        'Url': url
    }

    # ---------------- Image ------------------
    image_tag = soup.find('div', {"class": "preview"}).find('img', src=lambda x: x and 'api.gastro-hero.de' in x)
    image_url = image_tag.get('src') if image_tag else ''
    
    return new_row, image_url

def find_nc_information(url, position):
    """
    Scrapes product information from a NordCap product page and stores it in session state.

    Args:
        url (str): The URL of the product page.
        position (int): The product's position in the offer.
        products (str): The session key name for the product DataFrame.
        images (str): The session key name for the product images.
    """

    # Get the content of the page of the url
    api_soup = get_soup(url)
    soup = BeautifulSoup(api_soup, 'html.parser')

    # ---------------- Article ----------------
    article_div = soup.find('span', {'class': 'entry--content'})
    article_number = article_div.text.strip() if article_div else ''

    # ---------------- Title ------------------
    title_div = soup.find('h1', {'class': 'product--title'})
    title = ' '.join(title_div.stripped_strings) if title_div else ''

    # ---------------- Description ------------
    desc_soup = soup.find('div', {'class': 'tab-menu--product js--tab-menu'})
    description = ""

    # 1 Beschreibung
    # product_description = soup.find('div', {'class': 'product--description'})
    product_description = desc_soup.select_one('.product--description > ul')
    if product_description:
        description += "Beschreibung\n"
        product_description_without_hinweis = product_description.find_all('li')
        for item in product_description_without_hinweis:
            description += f'• {item.get_text(strip=True)} \n'

    # 2 Produktdetails
    product_details = desc_soup.find('div', {'class': 'nc-table-container is-full'})
    if product_details:
        description += "\nProduktdetails\n"
    # Each detail seems to be structured in sub-divs
        details = product_details.find_all('div', recursive=False)
        if details:

            # Extracting textual information clearly
            for detail in details:
                # Find key-value pairs
                label = detail.find('span', {'class': 'nc-table-title'})
                value = detail.find('span', {'class': 'nc-table-value'})
                if label and value:
                    description += f"• {label.get_text(strip=True)} {value.get_text(strip=True)} \n"

    # ---------------- Abmessungen ------------
    abmessungen = {}
    all_details = desc_soup.find_all('div', {'class': 'nc-table-container is-full'})

    if len(all_details) >= 2:
        description += "\nAbmessungen\n"
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

    description = description.strip()

    # ---------------- Hersteller -------------
    hersteller = 'NC'

    # ---------------- Price ------------------
    price_span = soup.find('span', {'class': 'price--content content--default'})
    price_meta = price_span.find('meta', {'itemprop': 'price'})
    price_raw = price_meta['content'] if price_meta else None
    price = float(price_raw) if price_raw else 0

    # ---------------- Image ------------------
    image_div = soup.find('span', {'class': 'image--media'}).find('img', src=lambda x: x and 'nordcap.de' in x)
    image_url = image_div.get('src') if image_div else ''

    # ---------------- Create row -------------
    new_row = {
        'Position': position,
        '2. Position': '',
        'Art_Nr': article_number,
        'Titel': title,
        'Beschreibung': description,
        'Menge': 1,
        'Preis': price,
        'Gesamtpreis': price,
        'Hersteller': hersteller,
        'Alternative': False,
        'Breite': int(abmessungen.get('Breite außen:')) if abmessungen.get('Breite außen:') else None,
        'Tiefe': int(abmessungen.get('Tiefe außen:')) if abmessungen.get('Tiefe außen:') else None,
        'Höhe': int(abmessungen.get('Höhe außen:')) if abmessungen.get('Höhe außen:') else None,
        'Url': url
    }

    return new_row, image_url

def find_sg_information(url, position):
    api_soup = get_soup(url)
    soup = BeautifulSoup(api_soup, 'html.parser')

    # ---------------- Article ----------------
    article_number = ""
    article_div = soup.find('div', {'class': 'additional-attributes-wrapper table-wrapper main-info-data'})
    if article_div:
        for p in article_div.find_all('p'):
            if "artikelnummer" in p.get_text(strip=True).lower():
                artikel_p = p
                break

    if artikel_p:
        article_number = artikel_p.find('b').text.strip()

    # ---------------- Title ------------------
    title = ""
    title_h1 = soup.find('h1', {'class': 'page-title'})
    if title_h1:
        title_span = title_h1.find('span', {'class': 'base', 'data-ui-id': 'page-title-wrapper'})
        if title_span:
            title = title_span.get_text(strip=True)

    # ---------------- Description ------------
    description = ""
    abmessungen = {}
    keywords = ['Breite', 'Tiefe', 'Höhe']

    # Get the table with the information
    table = soup.find('table', id='product-attribute-specs-table')
    if table:

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
        description = description.strip()

    # ---------------- Hersteller -------------
    hersteller = 'SG'

    # ---------------- Price ------------------
    price = None
    price_div = soup.find('div', class_='product-info-price')
    if price_div:
        meta_number = price_div.find('meta', attrs={'content': True})
        if meta_number:
            price_value = meta_number['content']
            price = float(price_value)

    # ---------------- Image ------------------
    image_url = ""
    image_div = soup.find('div', {'class': 'fotorama__stage__frame fotorama__active fotorama_vertical_ratio fotorama__loaded fotorama__loaded--img'})
    if image_div:
        image_src = image_div.find('img', src=lambda x: x and 'stalgast.de' in x)
        image_url = image_src.get('src') if image_src else ''

    # ---------------- Create row -------------
    new_row = {
        'Position': position,
        '2. Position': '',
        'Art_Nr': article_number,
        'Titel': title,
        'Beschreibung': description,
        'Menge': 1,
        'Preis': price,
        'Gesamtpreis': price,
        'Hersteller': hersteller,
        'Alternative': False,
        'Breite': int(abmessungen.get('Breite [mm]')) if abmessungen.get('Breite [mm]') else None,
        'Tiefe': int(abmessungen.get('Tiefe [mm]')) if abmessungen.get('Tiefe [mm]') else None,
        'Höhe': int(abmessungen.get('Höhe [mm]')) if abmessungen.get('Höhe [mm]') else None,
        'Url': url
    }

    return new_row, image_url

def find_gg_information(url, position):
    api_soup = get_soup(url)
    soup = BeautifulSoup(api_soup, 'html.parser')

    # ---------------- Article ----------------
    article_number = ""
    article_span = soup.find('span', {'class': 'product-detail-ordernumber'})
    if article_span:
        article_number = article_span.get_text(strip=True)
    
    # ---------------- Title ------------------
    title = ""
    title_div = soup.find('h1', {'class': 'product-detail-name'})
    if title_div:
        title = title_div.get_text(strip=True)
    
    # ---------------- Description ------------
    description = ""
    abmessungen = {}

    # Get the table with the information
    desc_div = soup.find('div', {'class': 'product-detail-description-text'})
    if desc_div:
        # Loop over each h3 in the div
        for section in desc_div.find_all("h3"):
            section_title = section.get_text(strip=True)
            description += f'{section_title}\n'
            ul = section.find_next_sibling("ul")
            
            if ul:
                for li in ul.find_all("li"):
                    item_text = li.get_text(strip=True)
                    if item_text:  # skip empty items
                        description += f"• {item_text}\n"

    # ---------------- Abmessungen ------------
    tech_table = soup.find('table', {'class': 'table table-striped product-detail-properties-table'})
    if tech_table:
        description += "Technische Daten\n"
        for row in tech_table.find_all('tr'):
            label = row.find('th', 'properties-label') 
            value = row.find('td', 'properties-value')

            if label and value:
                label_text = label.get_text(strip=True)
                value_text = value.get_text(strip=True)

                if label_text == "Abmessung in mm:":
                    # Extract numbers
                    match = re.findall(r"\d+", value_text)
                    if len(match) == 3:
                        abmessungen = {
                            "Breite": int(match[0]),
                            "Tiefe": int(match[1]),
                            "Höhe": int(match[2])
                        }
                    clean_value = re.sub(r"\s+", " ", value_text.replace("\xa0", " ")).strip()
                    description += f"• {label_text} {clean_value} \n"
                else:        
                    description += f'• {label_text} {value_text} \n'

    # ---------------- Hersteller -------------
    hersteller = 'GG'

    # ---------------- Price ------------------
    price = None
    price_p = soup.find('p', {'class': 'product-detail-price'})
    if price_p:
        price_text = price_p.get_text(strip=True)

        # Remove currency symbol and spaces
        price_text = price_text.replace("€", "").replace("\xa0", "").strip()
        
        # Convert from German format to float
        price = float(price_text.replace(".", "").replace(",", "."))

    # ---------------- Image ------------------
    image_url = ""
    image_div = soup.find('div', {'class': 'gallery-slider-item-container tns-item tns-slide-active'})
    if image_div:
        image_src = image_div.find('img', src=lambda x: x and 'grimm-gastrobedarf.de' in x)
        image_url = image_src.get('src') if image_src else ''

    else:
        image_div = soup.find('div', {'class': 'gallery-slider-single-image is-contain js-magnifier-container'})
        if image_div:
            image_src = image_div.find('img', src=lambda x: x and 'grimm-gastrobedarf.de' in x)
            image_url = image_src.get('src') if image_src else ''

    # ---------------- Create row -------------
    new_row = {
        'Position': position,
        '2. Position': '',
        'Art_Nr': article_number,
        'Titel': title,
        'Beschreibung': description,
        'Menge': 1,
        'Preis': price,
        'Gesamtpreis': price,
        'Hersteller': hersteller,
        'Alternative': False,
        'Breite': int(abmessungen.get('Breite')) if abmessungen.get('Breite') else None,
        'Tiefe': int(abmessungen.get('Tiefe')) if abmessungen.get('Tiefe') else None,
        'Höhe': int(abmessungen.get('Höhe')) if abmessungen.get('Höhe') else None,
        'Url': url
    }

    return new_row, image_url

def find_gm_information(url, position):
    api_soup = get_soup(url)
    soup = BeautifulSoup(api_soup, 'html.parser')

    # ---------------- Article ----------------
    article_number = ""
    article_span = soup.find('span', {'class': 'product-detail-ordernumber',
                                      'itemprop': 'sku'})
    if article_span:
        article_number = article_span.get_text(strip=True)
    
    # ---------------- Title ------------------
    title = ""
    title_h1 = soup.find('h1', {'class': 'product-detail-name'})
    if title_h1:
        title = title_h1.get_text(strip=True)

    # ---------------- Description ------------
    description = ""
    
    # 1) Find the heading <p> that contains <strong>Produktdetails</strong>
    produkt_p = None
    for p in soup.find_all("p"):
        strong = p.find("strong")
        if strong and "Produktdetails" in strong.get_text(strip=True):
            produkt_p = p
            break

    # 2) Walk forward through siblings after the heading
    if produkt_p:
        for sib in produkt_p.next_siblings:
            # Skip plain whitespace text nodes
            if isinstance(sib, NavigableString):
                if not sib.strip():
                    continue
                # If there's unexpected text between sections, keep going
                continue

            # If we hit another heading, stop (new section begins)
            if getattr(sib, "name", None) == "p" and sib.find("strong"):
                break

            # Also stop on HTML headings like <h2>, <h3>, etc.
            if getattr(sib, "name", "").lower().startswith("h"):
                break

            # Collect bullets from any <ul> directly after the heading (could be multiple)
            if getattr(sib, "name", None) == "ul":
                for li in sib.find_all("li"):
                    if description == "":
                        description += "Produktdetails\n"
                    else:
                        description += f"• {li.get_text(strip=True)}\n"

    # 3) Technische Tabelle
    tech_table = soup.find('table', {'class': 'table table-striped product-detail-properties-table'})
    if tech_table:
        description += "Eigenschaften\n"
        for row in tech_table.find_all('tr'):
            th = row.find('th')
            td = row.find('td')

            if th and td:
                label = th.get_text(strip=True)
                value = td.get_text(strip=True)
                description += f"• {label} {value}\n"

    # ---------------- Price ------------------
    price = 0
    price_p = soup.find('p', {'class': 'product-detail-price with-list-price'})
    if price_p:
        price_raw = price_p.get_text(strip=True)
        price_cleaned = re.sub(r"[^\d,\.]", "", price_raw).replace(",", ".")
        price = float(price_cleaned)
    else:
        price_p = soup.find('p', {'class': 'product-detail-price'})
        price_raw = price_p.get_text(strip=True)
        price_cleaned = re.sub(r"[^\d,\.]", "", price_raw).replace(",", ".")
        price = float(price_cleaned)

    # ---------------- Hersteller -------------
    hersteller = 'GM Möbel'

    # ---------------- Image ------------------
    image_url = ""
    image_div = soup.find('div', {'class': 'gallery-slider-item-container tns-item tns-slide-active'})
    if image_div:
        image_src = image_div.find('img', src=lambda x: x and 'gastronomie-moebel.eu' in x)
        image_url = image_src.get('src') if image_src else ''

    # ---------------- Create new row ---------
    new_row = {
        'Position': position,
        '2. Position': '',
        'Art_Nr': article_number,
        'Titel': title,
        'Beschreibung': description,
        'Menge': 1,
        'Preis': price,
        'Gesamtpreis': price,
        'Hersteller': hersteller,
        'Alternative': False,
        'Breite': None, # None bc website does not provide standard information on it
        'Tiefe': None,
        'Höhe': None,
        'Url': url
    }

    return new_row, image_url

def find_s24_information(url, position):
    api_soup = get_soup(url)
    soup = BeautifulSoup(api_soup, 'html.parser')

    # ---------------- Article ----------------
    # Create a unique article number: S24-Date-position
    today = date.today()
    code = today.strftime("%d%m")
    article_number = f"S24-{code}-{position}"

    # ---------------- Title ------------------
    title_h1 = soup.find('h1', {'class': 'productname fading showpost full-visible'})
    title = title_h1.get_text(strip=True) if title_h1 else ''

    # ---------------- Description-------------
    description = ""
    abmessungen = {}
    keywords = ["Gesamtbreite", "Gesamttiefe", "Gesamthöhe"]
    legend = soup.find_all('div', {'class': 'legendrow'})
    if legend:
        description += f"Produktdetails\n"
        for row in legend:
            label = row.find('div', 'legendtext') 
            value = row.find('div', 'legendvalue')
            
            if label and value:
                label_text = label.get_text(strip=True)
                value_text = value.get_text(strip=True)
                if value_text == "" or value_text == "\xa0":
                    description += f"• {label_text}\n"
                else:
                    description += f"• {label_text}: {value_text}\n"

                if any(keyword in label_text for keyword in keywords):
                    value_text = value_text.replace("cm", "").strip()
                    value_text = int(value_text) * 10
                    abmessungen[label_text] = value_text
        description = description.strip()

    # ---------------- Price ------------------
    price = None
    price_span = soup.find('span', {'id': 'price', 'itemprop': 'price'}) 
    if price_span:
        price_raw = price_span.get_text(strip=True).replace(",", ".")
        price = float(price_raw)

    # ---------------- Hersteller -------------
    hersteller = 'S24 Möbel'

    # ---------------- Create row -------------
    new_row = {
        'Position': position,
        '2. Position': '',
        'Art_Nr': article_number,
        'Titel': title,
        'Beschreibung': description,
        'Menge': 1,
        'Preis': price,
        'Gesamtpreis': price,
        'Hersteller': hersteller,
        'Alternative': False,
        'Breite': abmessungen.get('Gesamtbreite') if abmessungen.get('Gesamtbreite') else None,
        'Tiefe': abmessungen.get('Gesamttiefe') if abmessungen.get('Gesamttiefe') else None,
        'Höhe': abmessungen.get('Gesamthöhe') if abmessungen.get('Gesamthöhe') else None,
        'Url': url
    }

    # ---------------- Image ------------------
    image_url = ""
    image_div = soup.find('div', {'id': 'produktabbildung'})
    if image_div:
        image_src = image_div.find('img')
        if image_src:
            image_url_raw = image_src.get('src')
            image_url = f"https://www.stapelstuhl24.com/{image_url_raw}"

    return new_row, image_url

def find_ig_information(url, position):
    api_soup = get_soup(url)
    soup = BeautifulSoup(api_soup, 'html.parser')

    # ---------------- Hersteller -------------
    hersteller = "IG"

    # ---------------- Article ----------------
    article_number = ""
    hersteller_a = soup.find('a', {'id': 'brandLink'})
    if hersteller_a:
        hersteller = hersteller_a.get_text(strip=True)

    else:
        article_div = soup.find('div', {'class': 'product-info'})
        if article_div:
            product_div = article_div.find('div', {'class': 'product-number'})
            if product_div:
                product_span = product_div.find('span', {'itemprop': 'sku'})
                if product_span:
                    article_number = product_span.get_text(strip=True)

    # ---------------- Title ------------------
    title = ""
    title_h1 = soup.find('h1', {'class': 'product-name'})
    if title_h1:
        title_span = title_h1.find('span', {'itemprop': 'name'})
        if title_span:
            title = title_span.get_text(strip=True)

    # ---------------- Description-------------
    description = ""
    abmessungen = {}
    produktdetails_div = soup.find('div', {'id': 'ShortDescription'})
    if produktdetails_div:
        for dt in produktdetails_div.find_all('dt'):
            ul = dt.find_next_sibling('ul')
            stored_text = ""
            if ul:
                for li in ul.find_all('li'):
                    item_text = li.get_text()
                    if item_text:
                        text = re.sub(r"\s+", " ", item_text).replace("\xa0", " ").strip()
                        stored_text += f"• {text}\n"
                    if "Hersteller-Art.-Nr" in item_text:
                        text = re.sub(r"\s+", " ", item_text).replace("\xa0", " ").strip()
                        article_number = text.split(":")[1].strip()

                    if "Abmessungen" in dt.get_text():
                        if "Tiefe" in item_text:
                            abmessungen["Tiefe"] = item_text.split(":")[1].replace("mm", "").strip()

                        if "Breite" in item_text:
                            abmessungen["Breite"] = item_text.split(":")[1].replace("mm", "").strip()

                        if "Höhe" in item_text:
                            abmessungen["Höhe"] = item_text.split(":")[1].replace("mm", "").strip()
                
                if stored_text != "":
                    description += f"{dt.get_text(strip=True)}\n{stored_text}\n"
        
        description = description.strip()

    # ---------------- Price ------------------
    price = None
    price_div = soup.find('div', {'class': 'product-info'})
    if price_div:
        price_container = price_div.find('div', {'class': 'price-container'})
        if price_container:
            current_price_div = price_container.find('div', {'class': 'current-price'})
            if current_price_div:
                price_raw = current_price_div.find(string=True, recursive=False).strip()
                if price_raw:
                    price_raw = price_raw.replace(".", "").replace(",", ".").replace("€", "").strip()
                    price = float(price_raw)

    # ---------------- Create row -------------
    new_row = {
        'Position': position,
        '2. Position': '',
        'Art_Nr': article_number,
        'Titel': title,
        'Beschreibung': description,
        'Menge': 1,
        'Preis': price,
        'Gesamtpreis': price,
        'Hersteller': hersteller,
        'Alternative': False,
        'Breite': abmessungen.get('Breite') if abmessungen.get('Breite') else None,
        'Tiefe': abmessungen.get('Tiefe') if abmessungen.get('Tiefe') else None,
        'Höhe': abmessungen.get('Höhe') if abmessungen.get('Höhe') else None,
        'Url': url
    }

    # ---------------- Image ------------------
    image_url = ""
    image_div = soup.find('div', {'class': 'product-image-container'})
    if image_div:
        image_img = image_div.find('img')
        if image_img:
            image_url = f"https://www.intergastro.de{image_img.get('src')}"

    return new_row, image_url

def find_gdax_information(url, position):
    api_soup = get_soup(url)
    soup = BeautifulSoup(api_soup, 'html.parser')

    # ---------------- Hersteller -------------
    hersteller = "GDAX"

    # ---------------- Article ----------------
    article_number = ""

    article_div = soup.find('div', {'class': 'product-shop'})
    if article_div:
        product_div = article_div.find('p', {'class': 'sku'})
        if product_div:
            product_span = product_div.find('span')
            if product_span:
                article_number = product_span.get_text(strip=True)

    # ---------------- Title ------------------
    title = ""
    if article_div:
        title_li = article_div.find('li', {'class': 'title'})
        if title_li:
            title_h1 = title_li.find('h1')
            if title_h1:
                title = title_h1.get_text(strip=True)

    # ---------------- Description-------------
    description = ""
    abmessungen = {}
    produkt_beschreibung_div = soup.find('div', {'class': 'product-collateral'})
    if produkt_beschreibung_div:
        # produkt_strong = produkt_beschreibung_div.find(['strong', 'h3'], string=re.compile("Technische Daten", re.I))
        produkt_strong = produkt_beschreibung_div.find(["strong", "h3"],string=lambda t: t and re.search("Technische Daten", t, re.I))
        if produkt_strong:
            description += "Technische Daten\n"
            product_ul = produkt_strong.find_next('ul')
            if product_ul:
                for li in product_ul.find_all('li'):
                    item_text = li.get_text()
                    if item_text:
                        text = re.sub(r"\s+", " ", item_text).replace("\xa0", " ").strip()
                        description += f"• {text}\n"

    produkt_details_div = soup.find('div', {'id': 'additional_tabbed'})
    if produkt_details_div:
        details_text = "\nDetails\n"
        details_tr = produkt_details_div.find_all('tr')
        for tr in details_tr:
            cells = tr.find_all('td')
            if len(cells) >= 2:
              label_text = cells[0].get_text(strip=True)
              value_text = cells[1].get_text(strip=True)
              details_text += f"• {label_text}: {value_text}\n"
        
        if details_text != "\nDetails\n":
            description += details_text
    description = description.strip()

    # ---------------- Price ------------------
    price = None
    price_div = soup.find('p', {'class': 'regular-price'})
    if price_div:
        price_span = price_div.find('span', {'class': 'price'})
        if price_span:
            price_second_span = price_span.find('span')
            if price_second_span:
                price_raw = price_second_span.get_text(strip=True)
                if price_raw:
                    price_raw = price_raw.replace(".", "").replace(",", ".").replace("€", "").strip()
                    price = float(price_raw)

    # ---------------- Create row -------------
    new_row = {
        'Position': position,
        '2. Position': '',
        'Art_Nr': article_number,
        'Titel': title,
        'Beschreibung': description,
        'Menge': 1,
        'Preis': price,
        'Gesamtpreis': price,
        'Hersteller': hersteller,
        'Alternative': False,
        'Breite': abmessungen.get('Breite') if abmessungen.get('Breite') else None,
        'Tiefe': abmessungen.get('Tiefe') if abmessungen.get('Tiefe') else None,
        'Höhe': abmessungen.get('Höhe') if abmessungen.get('Höhe') else None,
        'Url': url
    }

    # ---------------- Image ------------------
    image_url = ""
    image_div = soup.find('div', {'class': 'product-img-box'})
    if image_div:
        image_div_2 = image_div.find('div', {'class': 'product-image'})
        if image_div_2:
            image_img = image_div_2.find('img')
            if image_img:
                image_url = image_img.get('src')

    return new_row, image_url