import streamlit as st
import os 
import yaml 

from src.fe.support_functions import setup_sidebar
from src.fe.styles import HIDE_SIDEBAR_NAV, TEXT_JUSTIFIED


################
# --- SET UP ---
################


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

# Navigation on click
if selected_page == "HOME":
    st.switch_page("HOME.py")
elif selected_page == "Whiteboard":
    st.switch_page("pages/whiteboard.py")
elif selected_page == "IELTS Preparation":
    st.switch_page("pages/ielts_preparation.py")
elif selected_page == "Lesson Planner":
    st.title(selected_page)
elif selected_page == "Syllabus Planner":
    st.switch_page("pages/syllabus_planner.py")
elif selected_page == "TEFL Theory":
    st.switch_page("pages/tefl_theory.py")


# --- DEFAULT SECTIONS ---





###########################
# --- PAGE MAIN CONTENT ---
###########################


# --- BASIC INFO ---
col1, col2, col3 = st.columns(3)
with col1: plan_title = st.text_input("Title")
with col2: plan_teacher = st.text_input("Teacher")
with col3: plan_date = st.date_input("Date", format="DD/MM/YYYY")
st.markdown("---")

# --- CLASS INFO FORM ---

with st.form("class_info_form", border=True):

    st.subheader("Class Information")
    st.multiselect("Add Information", options=[])


    st.form_submit_button()