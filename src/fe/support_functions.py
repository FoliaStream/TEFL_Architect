import streamlit as st 
import pandas as pd

import os 

from transformers import pipeline
from streamlit_option_menu import option_menu
from src.fe.styles import SIDEBAR_STYLES, BUTTON_STYLE


# --- SUPPORT FUNCTIONS TO BE USED IN FRONT END ---


# SIDEBAR
def setup_sidebar(pages,
                  main_page):
    with st.sidebar:
        col1, col2, col3 = st.columns([0.2, 0.7, 0.2])
        with col2:
            st.image(f"{os.getcwd()}/LOGO.png")
        
        # Initialize session state for page if it doesn't exist
        if 'selected_page' not in st.session_state:
            st.session_state.selected_page = main_page
        
        choose = option_menu("", 
                            pages,
                            default_index=pages.index(st.session_state.selected_page),
                            styles=SIDEBAR_STYLES)
        
        if choose != st.session_state.selected_page:
            st.session_state.selected_page = choose
            st.rerun()  
    
    return st.session_state.selected_page


# SEARCH TEXT
def search_text(keystring, db_dir):
    results = []

    for chapter in os.listdir(db_dir):
        chapter_path = os.path.join(db_dir, chapter)
        
        for page in os.listdir(chapter_path):
            try:
                with open(os.path.join(chapter_path, page), "r", encoding="utf-8") as f:
                    for line_num, line in enumerate(f, 1):
                        if keystring.lower() in line.lower():
                            results.append({
                                'folder': chapter,
                                'file': page,
                                'line': line_num,
                                'content': line
                            })
            except Exception as e:
                print(f"Error reading {page}: {e}")
                continue  

    # Create DataFrame AFTER all loops are done
    if results:  # Only create DataFrame if there are results
        df_res = pd.DataFrame(results)
        res_folders = df_res['folder'].tolist()
        res_files = df_res['file'].tolist()
        res_lines = df_res['line'].tolist()
        res_contents = df_res['content'].tolist()
    else:
        # Return empty lists if no results
        res_folders, res_files, res_lines, res_contents = [], [], [], []

    return res_folders, res_files, res_lines, res_contents


# GRID BUTTONS
def grid_buttons(num_columns, button_labels, button_info):

    button_data = [{"label":label, "info":info} for label, info in zip(button_labels, button_info)]
    cols = st.columns(num_columns)
    clicked = None

    for i, btn in enumerate(button_data):
        with cols[i % num_columns]:
            if st.button(btn['label'], key=f"btn_{i}", use_container_width=True):
                clicked = btn
            
    return clicked
    
# AI SUMMARY
def summarizer_ai():
    return pipeline("summarization", model="t5-small", device=-1)