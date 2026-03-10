import streamlit as st
import os 
import yaml 

from src.fe.support_functions import setup_sidebar
from src.fe.styles import HIDE_SIDEBAR_NAV, TEXT_JUSTIFIED


################
# --- SET UP ---
################

# --- PAGE CONFIG --- 
st.set_page_config(page_title="HOME", layout="wide")

# --- STYLES ---
st.markdown(HIDE_SIDEBAR_NAV, unsafe_allow_html=True)
st.markdown(TEXT_JUSTIFIED, unsafe_allow_html=True)

# --- CONFIG ---
with open(f"{os.getcwd()}/src/be/config.yaml", "r") as config_file:
    config = yaml.safe_load(config_file)

# --- SIDEBAR & TITLE ---
selected_page = setup_sidebar(
    pages=config['pages'],
    main_page=config['main_page'])

# Navigation on click
if selected_page == "HOME":
    pass
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

# --- LOGO-TITLE ---
col1,col2,col3 = st.columns([1,2,1])
with col2:
    st.image(f"{os.getcwd()}/LOGO.png")

st.divider()

# --- DESCRIPTION ---
col1, col2 = st.columns([1,1])
with col1:
    st.header("Welcome to TEFL Architect!")
    st.info("""
        This interactive web tool aims to support teachers in their activities. \n

        Get started by exploring the pages!  

        """)

with col2:

    st.header("Description:")
    st.info("**Whiteboard**: Use an interactive whiteboard to take, load, and save notes")
    st.info("**IELTS Preparation**: IELTS Exam helper tool")
    st.info("**Lesson Planner**: Generate structured lesson plans")
    st.info("**Syllabus Planner**: Generate structured syllabus and course plans")
    st.info("**TEFL Theory**: Explore the theory beyond TEFL")


st.divider()


# --- FOOTER ---


col1, col2, col3, col4 = st.columns([1,1,1,1.1])
with col1:
    st.subheader("CONTACT")
with col2:
    st.markdown("**Mail**")
    st.markdown("📩 foliastream@gmail.com")
with col3:
    st.markdown("**Link**")
    st.caption("🌐 https://teflarchitect.streamlit.app")
with col4:
    st.markdown("**GitHub**")
    st.caption("</>  https://github.com/FoliaStream/TEFL_Architect")