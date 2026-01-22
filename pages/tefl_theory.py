import streamlit as st
import os 
import yaml 

from src.fe.support_functions import setup_sidebar, search_text, grid_buttons, summarizer_ai
from src.fe.styles import HIDE_SIDEBAR_NAV, TEXT_JUSTIFIED, BUTTON_STYLE, GRID_BUTTONS_STYLE

########################
# --- INITIALIZATION ---
########################


# --- PAGE CONFIG --- 
st.set_page_config(page_title="Theory", layout="wide")

# --- STYLES ---
st.markdown(HIDE_SIDEBAR_NAV, unsafe_allow_html=True)
st.markdown(TEXT_JUSTIFIED, unsafe_allow_html=True)
st.markdown(BUTTON_STYLE, unsafe_allow_html=True)
st.markdown(GRID_BUTTONS_STYLE, unsafe_allow_html=True)


# --- CONFIG ---
with open(f"{os.getcwd()}/src/be/config.yaml", "r") as config_file:
    config = yaml.safe_load(config_file)

# --- PAGE SPECIFIC FUNCTIONs ---

# DISPLAY SEARCH RESULTS
def display_search_res(res_chapters, res_pages, res_lines, res_contents, search_query, chapters, chapters_labels, chapters_titles, chapters_indexes):
    
    # Recreate chapters_info_map from parallel lists
    chapters_info_map = {}
    for folder, label, title, index in zip(chapters, chapters_labels, chapters_titles, chapters_indexes):
        chapters_info_map[folder] = {
            'label': label,
            'title': title,
            'index': index
        }
    
    # Create mapping from folder name to display label
    folder_to_label = {folder: info['label'] for folder, info in chapters_info_map.items()}
    
    # Convert search result folder names to display labels
    res_labels = [folder_to_label.get(chapter, chapter) for chapter in res_chapters]
    
    # Create list of dictionaries from parallel lists
    results = [
        {
            'folder': folder,          
            'label': label,            
            'page': page,
            'line': line,
            'content': content
        }
        for folder, label, page, line, content in zip(
            res_chapters, res_labels, res_pages, res_lines, res_contents
        )
    ]
    
    # Sort by chapter label
    results.sort(key=lambda x: x['label'])
    
    # 6. Check if results exist
    if not results:
        st.info("No matches found")
        return
    
    st.success(f"**Found {len(results)} matches**")
    
    # Group by chapter label
    chapters_grouped = {}
    for result in results:
        chapter_label = result['label']
        if chapter_label not in chapters_grouped:
            chapters_grouped[chapter_label] = []
        chapters_grouped[chapter_label].append(result)
    
    # Generate results expanders
    for chapter_label, chapter_results in chapters_grouped.items():
        with st.expander(f"**{chapter_label} ({len(chapter_results)} matches)**", expanded=False):
            for result in chapter_results:
                col1, col2 = st.columns([5, 1])

                with col1:
                    with st.container():
                        page_num = result['page'][:-4]
                        st.markdown(f"**PAGE: {page_num}** (Line {result['line']})")
                        
                        content = result['content'].strip()
                        if search_query.lower() in content.lower():
                            highlighted = content.replace(
                                search_query, 
                                f":red[»**{search_query}**«]"
                            ).replace(
                                search_query.lower(),
                                f":red[»**{search_query.lower()}**«]"
                            ).replace(
                                search_query.upper(),
                                f":red[»**{search_query.upper()}**«]"
                            )
                            st.markdown(highlighted)
                        else:
                            st.write(content)
                
                with col2:
                    button_key = f"open_{result['folder']}_{result['page']}_{result['line']}_{hash(search_query)}"
                    if st.button("Open", key=button_key, type="secondary"):
                        # Set navigation state
                        st.session_state.from_search = True
                        st.session_state.selected_chapter = result['label']
                        st.session_state.active_slide = int(result['page'][:-4])
                        
                        # Get chapter info from our recreated map
                        chapter_data = chapters_info_map.get(result['folder'], {})
                        st.session_state.chapter_info = chapter_data.get('title', "")
                        
                        # Store search context
                        st.session_state.search_context = {
                            'query': search_query,
                            'line_number': result['line']
                        }
                        
                        st.session_state.force_tab_navigation = True
                        st.session_state.target_tab = int(result['page'][:-4]) - 1
                        st.rerun()
                
                st.divider()
    
    return

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
    st.title(selected_page)


# --- SESSION STATE VARIABLES INITIALIZATION ---

if 'selected_chapter' not in st.session_state:
    st.session_state.selected_chapter = None
if 'chapter_info' not in st.session_state:
    st.session_state.chapter_info = None
if 'active_slide' not in st.session_state:
    st.session_state.active_slide = None
if 'from_search' not in st.session_state:
    st.session_state.from_search = None


# --- CHAPTERS INFO MAP TO LISTS ---

sorted_chapters = sorted(config['chapter_info_map'].items(), key=lambda x: x[1]['index'])
chapters = [key for key, _ in sorted_chapters]
chapters_labels = [info['label'] for _, info in sorted_chapters]
chapters_titles = [info['title'] for _, info in sorted_chapters]
chapters_indexes = [info['index'] for _, info in sorted_chapters]
label_to_folder = dict(zip(chapters_labels, chapters))


















###########################
# --- PAGE MAIN CONTENT ---
###########################

# Search bar
key_string = st.text_input("Search:")

if key_string and len(key_string) > 1:
    res_chapters, res_pages, res_lines, res_contents = search_text(key_string, str(f"{os.getcwd()}/db/tefl_chapters/"))

    if len(res_chapters)>0:
        with st.container(border=True):
            display_search_res(res_chapters, res_pages, res_lines, res_contents, key_string, chapters, chapters_labels, chapters_titles, chapters_indexes) # here pass the lists of config chapters and not whole
#TODO add clear search button
    

# Chapter buttons grid 
st.subheader("Select a Chapter")
clicked_button = grid_buttons(num_columns=4, button_labels=chapters_labels, button_info=chapters_titles)

# Set chapter and slide
if clicked_button:
    st.session_state.selected_chapter = clicked_button['label']
    st.session_state.chapter_info = clicked_button['info']
    st.session_state.active_slide = 1  
    st.rerun()

# Clear selection
if st.session_state.selected_chapter:
    if st.button("Clear Selection", key="clear_btn"):
        st.session_state.selected_chapter = None
        st.session_state.chapter_info = None
        st.session_state.active_slide = None
        st.rerun()

active_chapter = st.session_state.selected_chapter
active_chapter_info = st.session_state.chapter_info
active_slide = st.session_state.active_slide

# Display 

if active_chapter:
    st.markdown(f"<h1 style='text-align: center;'>{active_chapter}</h1>", unsafe_allow_html=True)
    if active_chapter_info:
        st.markdown(f"<h2 style='text-align: center;'>{active_chapter_info}</h2>", unsafe_allow_html=True)

    # Get the folder name from the mapping
    chapter_folder = label_to_folder.get(active_chapter)
    
    # Get slides 
    chapter_path = f"{os.getcwd()}/db/tefl_chapters/{chapter_folder}/"
    if os.path.exists(chapter_path):
        num_slides = len([f for f in os.listdir(chapter_path) if f.endswith('.txt')])
        
        # Create horizontal radio buttons for slide selection
        slide_options = [f"Page {i}" for i in range(1, num_slides + 1)]

        # Determine default selection - handle None case
        if active_slide is None:
            default_index = 0  # Default to first slide
        else:
            default_index = active_slide - 1

        # Ensure index is within bounds
        default_index = max(0, min(default_index, len(slide_options) - 1))

        # Radio buttons for slide selection
        selected_option = st.radio(
            "Pages:",
            slide_options,
            index=default_index,
            horizontal=True,
            key=f"slide_select_{active_chapter}_{default_index}"
        )

        # Extract slide number
        selected_slide = int(selected_option.split()[1])
        
        # Update session state if slide changed
        if selected_slide != active_slide:
            st.session_state.active_slide = selected_slide
            st.rerun()

        # Check if we're viewing a slide from search results
        is_from_search = False
        search_line = None
        query = None

        if 'search_context' in st.session_state:
            search_ctx = st.session_state.search_context
            if (search_ctx.get('chapter') == active_chapter and 
                search_ctx.get('slide') == selected_slide):
                is_from_search = True
                search_line = search_ctx.get('line_number')
                query = search_ctx.get('query')
        
        # Display the slide content
        slide_path = f"{chapter_path}{selected_slide}.txt"


        if is_from_search:
            st.markdown("🔍 *Opened from search results*")
        
        if os.path.exists(slide_path):
            try: 
                with open(slide_path, 'r', encoding='utf-8') as file:
                    slide_content = file.read()
                
                # Highlight search term if applicable
                if is_from_search and search_line and query:
                    lines = slide_content.split('\n')
                    
                    for j, line in enumerate(lines, 1):
                        if j == search_line and query.lower() in line.lower():
                            # Bold the search term
                            start = line.lower().find(query.lower())
                            end = start + len(query)
                            highlighted_line = (
                                line[:start] + 
                                "**" + line[start:end] + "**" + 
                                line[end:]
                            )
                            st.markdown(highlighted_line)
                        else:
                            st.markdown(line)
                else:
                    st.markdown(slide_content)
                    
            except Exception as e:
                st.error(f"Error reading file: {e}")
            
            st.divider()
            
            # AI Summary button
            if st.button("AI Summary", key=f"summary_{active_chapter}_{selected_slide}", type="secondary"):
                summarizer = summarizer_ai()
                
                def chunk_text(text, max_words=300):
                    words = text.split()
                    for i in range(0, len(words), max_words):
                        yield " ".join(words[i:i+max_words])
                
                summaries = []
                for chunk in chunk_text(slide_content, max_words=300):
                    summary_chunk = summarizer(
                        chunk, 
                        max_length=100, 
                        min_length=30, 
                        do_sample=False
                    )
                    summaries.append(summary_chunk[0]['summary_text'])
                
                final_summary = " ".join(summaries)
                
                with st.container(border=True):
                    st.caption("Summary")
                    st.markdown(final_summary)
        else:
            st.info(f"File not found: {slide_path}")
# ----
