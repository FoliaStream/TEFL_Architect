import streamlit as st
import os 
import yaml

from src.fe.support_functions import setup_sidebar
from src.fe.styles import HIDE_SIDEBAR_NAV, TEXT_JUSTIFIED


# --- PAGE CONFIG --- 
st.set_page_config(page_title="Theory", layout="wide")

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
