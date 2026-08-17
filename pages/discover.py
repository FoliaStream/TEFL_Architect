import streamlit as st
import pandas as pd

import os 
import yaml 
import re 
import time
import shutil

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.chrome.service import Service

from src.fe.support_functions import setup_sidebar
from src.fe.styles import HIDE_SIDEBAR_NAV, TEXT_JUSTIFIED


################
# --- SET UP ---
################

# --- PAGE CONFIG --- 
st.set_page_config(page_title="Discover", layout="wide")

# --- STYLES ---
st.markdown(HIDE_SIDEBAR_NAV, unsafe_allow_html=True)
st.markdown(TEXT_JUSTIFIED, unsafe_allow_html=True)

# --- CONFIG ---
with open(f"{os.getcwd()}/src/be/config.yaml", "r") as config_file:
    config = yaml.safe_load(config_file)

# --- SIDEBAR & TITLE ---
selected_page = setup_sidebar(
    pages=config['pages'],
    main_page=config['main_page']
)

# Navigation on click
if selected_page == "HOME":
    st.switch_page("HOME.py")
elif selected_page == "Whiteboard":
    st.switch_page("pages/whiteboard.py")
elif selected_page == "IELTS Preparation":
    st.switch_page("pages/ielts_preparation.py")
elif selected_page == "Lesson Planner":
    st.switch_page("pages/lesson_planner.py")
elif selected_page == "Syllabus Planner":
    st.switch_page("pages/syllabus_planner.py")
elif selected_page == "TEFL Theory":
    st.switch_page("pages/tefl_theory.py")
elif selected_page == "Discover":
    st.title(selected_page)

# PAGE

# Inputs
col1, col2, col3 = st.columns(3)
with col1:
    area = st.text_input("📍 Area", value="Hanoi, Vietnam")
with col2:
    place_type = st.text_input("🏢 Place Type", value="English center")
with col3:
    max_places = st.number_input("📊 Max Places", min_value=1, max_value=200, value=20)


class GoogleMapsScraper:
    def __init__(self):
        options = Options()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--single-process")   # helps in constrained containers
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--lang=en-US")
        options.add_experimental_option("prefs", {"intl.accept_languages": "en-US,en"})
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36"
        )

        chromium_path = shutil.which("chromium") or shutil.which("chromium-browser")
        chromedriver_path = shutil.which("chromedriver")

        if chromium_path:
            options.binary_location = chromium_path

        if chromedriver_path:
            service = Service(executable_path=chromedriver_path)
            self.driver = webdriver.Chrome(service=service, options=options)
        else:
            # local fallback (e.g. Selenium Manager auto-resolves it)
            self.driver = webdriver.Chrome(options=options)
        try:
            self.driver.execute_cdp_cmd(
                "Page.addScriptToEvaluateOnNewDocument",
                {"source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"},
            )
        except Exception:
            pass

        self.wait = WebDriverWait(self.driver, 4)

    def search(self, area, place_type):
        query = f"{place_type} in {area}"
        self.driver.get(f"https://www.google.com/maps/search/{query.replace(' ', '+')}?hl=en")
        try:
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[role="feed"]')))
        except TimeoutException:
            time.sleep(2)

    def scroll_until_enough_cards(self, max_places):
        """Scroll the results feed only as much as needed to load max_places cards."""
        stale_rounds = 0
        last_count = 0
        for _ in range(30):
            cards = self.driver.find_elements(By.CSS_SELECTOR, "div.Nv2PK")
            if len(cards) >= max_places:
                break

            if len(cards) == last_count:
                stale_rounds += 1
                if stale_rounds >= 3:
                    break
            else:
                stale_rounds = 0
            last_count = len(cards)

            try:
                feed = self.driver.find_element(By.CSS_SELECTOR, '[role="feed"]')
                self.driver.execute_script(
                    "arguments[0].scrollTop = arguments[0].scrollHeight", feed
                )
            except NoSuchElementException:
                self.driver.execute_script("window.scrollBy(0, 1200);")
            time.sleep(1)

    def clean_text(self, text):
        if not text:
            return "N/A"
        text = re.sub(r'[^\x00-\x7F]+', '', text)
        text = ' '.join(text.split())
        return text.strip() or "N/A"

    def parse_card(self, card):
        """Extract name, rating, address, and website directly from a
        results-list card (.Nv2PK)."""

        # Name
        try:
            name = self.clean_text(card.find_element(By.CSS_SELECTOR, ".qBF1Pd").text)
        except NoSuchElementException:
            name = "N/A"

        # Rating (e.g. "4,4" or "4.4")
        try:
            rating = card.find_element(By.CSS_SELECTOR, ".MW4etd").text.strip().replace(",", ".")
            if not rating:
                rating = "N/A"
        except NoSuchElementException:
            rating = "N/A"

        # Website — leave N/A if this business has no website link
        website = "N/A"
        try:
            website_elem = card.find_element(By.CSS_SELECTOR, "a.lcr4fd")
            href = website_elem.get_attribute("href")
            if href:
                website = href
        except NoSuchElementException:
            pass

        # Address (best effort). The card actually has two separate nested
        # blocks here: one with category + address, another with hours + phone.
        # We need the first one specifically, not just "the last .W4Efsd found".
        address = "N/A"
        try:
            addr_block = card.find_element(
                By.CSS_SELECTOR, ".W4Efsd:last-child > .W4Efsd:nth-of-type(1)"
            )
            spans = addr_block.find_elements(By.TAG_NAME, "span")
            if spans:
                text = self.clean_text(spans[-1].text)
                address = text if text != "N/A" else "N/A"
        except NoSuchElementException:
            pass

        return {"Name": name, "Rating": rating, "Address": address, "Website": website}

    def scrape(self, max_places):
        places = []
        self.scroll_until_enough_cards(max_places)

        cards = self.driver.find_elements(By.CSS_SELECTOR, "div.Nv2PK")[:max_places]
        for card in cards:
            try:
                data = self.parse_card(card)
                if data["Name"] != "N/A":
                    places.append(data)
            except StaleElementReferenceException:
                continue

        return places

    def close(self):
        self.driver.quit()


if st.button("🚀 Start Scraping"):
    if area and place_type:
        scraper = GoogleMapsScraper()
        try:
            with st.spinner(f"Searching for {place_type} in {area}..."):
                scraper.search(area, place_type)
                data = scraper.scrape(int(max_places))

            if data:
                df = pd.DataFrame(data)
                st.success(f"✅ Found {len(data)} places!")

                st.dataframe(
                    df,
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "Website": st.column_config.LinkColumn("Website"),
                        "Rating": st.column_config.TextColumn("Rating"),
                    },
                )

                csv = df.to_csv(index=False, encoding='utf-8-sig')
                st.download_button(
                    label="📥 Download CSV",
                    data=csv,
                    file_name=f"google_maps_{place_type}_{area}.csv",
                    mime="text/csv",
                )
            else:
                st.warning("No places found. Try different search terms.")
        except Exception as e:
            st.error(f"Error: {e}")
        finally:
            scraper.close()
    else:
        st.error("Please fill in both fields")