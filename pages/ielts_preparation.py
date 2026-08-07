import streamlit as st
import os 
import yaml 

from src.fe.support_functions import setup_sidebar, grid_buttons, natural_sort
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

# Navigation on click
if selected_page == "HOME":
    st.switch_page("HOME.py")
elif selected_page == "Whiteboard":
    st.switch_page("pages/whiteboard.py")
elif selected_page == "IELTS Preparation":
    st.title(selected_page)
elif selected_page == "Lesson Planner":
    st.switch_page("pages/lesson_planner.py")
elif selected_page == "Syllabus Planner":
    st.switch_page("pages/syllabus_planner.py")
elif selected_page == "TEFL Theory":
    st.switch_page("pages/tefl_theory.py")



# --- SESSION STATE VARIABLES INIT ---
if 'selected_topic' not in st.session_state:
    st.session_state.selected_topic = None
if 'topic_info' not in st.session_state:
    st.session_state.topic_info = None


# --- CONFIG IMPORT VARIABLES ---
sorted_speaking = sorted(config['ielts_map']['speaking'].items(), key=lambda x: x[1]['index'])
speaking_tips = [key for key, _ in sorted_speaking]
speaking_labels = [info['label'] for _, info in sorted_speaking]
speaking_titles = [info['title'] for _, info in sorted_speaking]
speaking_indexes = [info['index'] for _, info in sorted_speaking]
speaking_label_to_folder = dict(zip(speaking_labels, speaking_tips))


sorted_writing = sorted(config['ielts_map']['writing'].items(), key=lambda x: x[1]['index'])
writing_tips = [key for key, _ in sorted_writing]
writing_labels = [info['label'] for _, info in sorted_writing]
writing_titles = [info['title'] for _, info in sorted_writing]
writing_indexes = [info['index'] for _, info in sorted_writing]
writing_label_to_folder = dict(zip(writing_labels, writing_tips))



###########################
# --- PAGE MAIN CONTENT ---
###########################

# Work in progress
ielts_tabs = ["Speaking", "Reading", "Listening", "Writing", "Mock Exams"]
tab1, tab2, tab3, tab4, tab5 = st.tabs([label.center(23, "\u2001") for label in ielts_tabs])

with tab1: 
    ### SPEAKING ###
    st.subheader("Select a topic")
    clicked_button = grid_buttons(num_columns=4, button_labels=speaking_labels, button_info=speaking_titles)

    # Set chapter and slide
    if clicked_button:
        st.session_state.selected_topic = clicked_button['label']
        st.session_state.topic_info = clicked_button['info']
        st.rerun()

    st.divider()

    # Clear Selection
    if st.session_state.selected_topic:
        if st.button("Clear Selection", key="clear_btn_speaking"):
            st.session_state.selected_topic = None
            st.session_state.topic_info = None
            st.rerun()
    
    active_topic = st.session_state.selected_topic
    active_topic_info = st.session_state.topic_info

    # Display 

    if active_topic:
        st.markdown(f"<h1 style='text-align: center;'>{active_topic}</h1>", unsafe_allow_html=True)
        if active_topic_info:
            st.markdown(f"<h2 style='text-align: center;'>{active_topic_info}</h2>", unsafe_allow_html=True)

        # Get the folder name from the mapping
        speaking_folder = speaking_label_to_folder.get(active_topic)

        # Get slides
        speaking_path = f"{os.getcwd()}/db/ielts/speaking/{speaking_folder}/"
        
        # Plot
        if os.path.exists(speaking_path):
            slides = natural_sort([f for f in os.listdir(speaking_path) if f.endswith('.jpg')])
            for slide in slides:
                st.image(str(speaking_path+slide), use_container_width=True)
