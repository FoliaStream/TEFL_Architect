# import streamlit as st 
# import pandas as pd
# import base64

# import os 

# from transformers import pipeline
# from streamlit_option_menu import option_menu
# from src.fe.styles import SIDEBAR_STYLES, BUTTON_STYLE


# # --- SUPPORT FUNCTIONS TO BE USED IN FRONT END ---


# # SIDEBAR
# def setup_sidebar(pages,
#                   main_page):
#     with st.sidebar:
#         col1, col2, col3 = st.columns([0.2, 0.7, 0.2])
#         with col2:
#             st.image(f"{os.getcwd()}/LOGO.png")
        
#         # Initialize session state for page if it doesn't exist
#         if 'selected_page' not in st.session_state:
#             st.session_state.selected_page = main_page
        
#         choose = option_menu("", 
#                             pages,
#                             default_index=pages.index(st.session_state.selected_page),
#                             styles=SIDEBAR_STYLES)
        
#         if choose != st.session_state.selected_page:
#             st.session_state.selected_page = choose
#             st.rerun()  
    
#     return st.session_state.selected_page


# # SEARCH TEXT
# def search_text(keystring, db_dir):
#     results = []

#     for chapter in os.listdir(db_dir):
#         chapter_path = os.path.join(db_dir, chapter)
        
#         for page in os.listdir(chapter_path):
#             try:
#                 with open(os.path.join(chapter_path, page), "r", encoding="utf-8") as f:
#                     for line_num, line in enumerate(f, 1):
#                         if keystring.lower() in line.lower():
#                             results.append({
#                                 'folder': chapter,
#                                 'file': page,
#                                 'line': line_num,
#                                 'content': line
#                             })
#             except Exception as e:
#                 print(f"Error reading {page}: {e}")
#                 continue  

#     # Create DataFrame AFTER all loops are done
#     if results:  # Only create DataFrame if there are results
#         df_res = pd.DataFrame(results)
#         res_folders = df_res['folder'].tolist()
#         res_files = df_res['file'].tolist()
#         res_lines = df_res['line'].tolist()
#         res_contents = df_res['content'].tolist()
#     else:
#         # Return empty lists if no results
#         res_folders, res_files, res_lines, res_contents = [], [], [], []

#     return res_folders, res_files, res_lines, res_contents


# # GRID BUTTONS
# def grid_buttons(num_columns, button_labels, button_info):

#     button_data = [{"label":label, "info":info} for label, info in zip(button_labels, button_info)]
#     cols = st.columns(num_columns)
#     clicked = None

#     for i, btn in enumerate(button_data):
#         with cols[i % num_columns]:
#             if st.button(btn['label'], key=f"btn_{i}", use_container_width=True):
#                 clicked = btn
            
#     return clicked
    
# # AI SUMMARY
# def summarizer_ai():
#     return pipeline("summarization", model="t5-small", device=-1)

# # DISPLAY PDF
# def display_pdf(pdf_path, height=700):
#     """
#     Display a PDF file in a scrollable iframe.
#     """
#     try:
#         with open(pdf_path, "rb") as f:
#             base64_pdf = base64.b64encode(f.read()).decode('utf-8')
        
#         # Create an iframe with the PDF embedded
#         pdf_display = f'''
#         <iframe
#             src="data:application/pdf;base64,{base64_pdf}"
#             width="100%"
#             height="{height}px"
#             type="application/pdf"
#             style="border: 1px solid #ddd; border-radius: 5px;"
#         ></iframe>
#         '''
#         st.markdown(pdf_display, unsafe_allow_html=True)
        
#         # Add download button
#         st.download_button(
#             label="📥 Download PDF",
#             data=open(pdf_path, "rb").read(),
#             file_name=os.path.basename(pdf_path),
#             mime="application/pdf"
#         )
        
#     except FileNotFoundError:
#         st.error(f"PDF file not found: {pdf_path}")
#         st.info("Please ensure the PDF files are in the correct directory.")
import streamlit as st 
import pandas as pd
import base64
import os 
from pathlib import Path
import io
from PIL import Image

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


# --- NEW PDF DISPLAY FUNCTIONS (MORE RELIABLE FOR DEPLOYMENT) ---

def convert_pdf_to_images(pdf_path, dpi=150):
    """
    Convert PDF to images using PyMuPDF (fitz).
    Requires: pip install PyMuPDF pillow
    """
    try:
        import fitz  # PyMuPDF
        
        # Open the PDF
        doc = fitz.open(pdf_path)
        images = []
        
        for page_num in range(doc.page_count):
            page = doc[page_num]
            # Render page to an image
            pix = page.get_pixmap(matrix=fitz.Matrix(dpi/72, dpi/72))
            img_data = pix.tobytes("png")
            img = Image.open(io.BytesIO(img_data))
            images.append(img)
        
        doc.close()
        return images
    except ImportError:
        st.error("⚠️ PyMuPDF not installed. Run: pip install PyMuPDF pillow")
        return None
    except Exception as e:
        st.error(f"❌ Error converting PDF: {str(e)}")
        return None


def display_pdf_as_images(pdf_path, height=700, width=800):
    """
    Display PDF as images with navigation controls.
    This is more reliable for deployment than iframe embedding.
    """
    # Check if PDF exists
    if not os.path.exists(pdf_path):
        st.error(f"❌ PDF not found: {pdf_path}")
        st.info("Please ensure the PDF file is in the correct directory.")
        return
    
    # Check for PyMuPDF
    try:
        import fitz
    except ImportError:
        st.error("⚠️ PyMuPDF not installed. Please install it to display PDFs as images.")
        st.info("Run: pip install PyMuPDF pillow")
        # Fallback to original method
        display_pdf_original(pdf_path, height)
        return
    
    # Convert PDF to images
    with st.spinner("🔄 Loading presentation..."):
        images = convert_pdf_to_images(pdf_path, dpi=120)
    
    if images is None:
        return
    
    # Display page navigation
    total_pages = len(images)
    
    # Create a unique key for this PDF
    pdf_key = os.path.basename(pdf_path).replace(".pdf", "").replace(".", "_")
    
    # Page selector
    if total_pages > 1:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            page_num = st.number_input(
                f"Page (1-{total_pages})",
                min_value=1,
                max_value=total_pages,
                value=st.session_state.get(f"page_{pdf_key}", 1),
                step=1,
                key=f"page_input_{pdf_key}"
            )
            # Store in session state
            st.session_state[f"page_{pdf_key}"] = page_num
    else:
        page_num = 1
        st.info("📄 This presentation has 1 page")
    
    # Display the selected page
    img = images[page_num - 1]
    
    # Resize image to fit width while maintaining aspect ratio
    img.thumbnail((width, 2000))
    st.image(img, use_container_width=True, caption=f"Page {page_num} of {total_pages}")
    
    # Navigation buttons
    if total_pages > 1:
        col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
        with col1:
            if st.button("⏮ First", key=f"first_{pdf_key}"):
                st.session_state[f"page_{pdf_key}"] = 1
                st.rerun()
        with col2:
            if st.button("◀ Previous", key=f"prev_{pdf_key}"):
                current = st.session_state.get(f"page_{pdf_key}", 1)
                if current > 1:
                    st.session_state[f"page_{pdf_key}"] = current - 1
                    st.rerun()
        with col4:
            if st.button("Next ▶", key=f"next_{pdf_key}"):
                current = st.session_state.get(f"page_{pdf_key}", 1)
                if current < total_pages:
                    st.session_state[f"page_{pdf_key}"] = current + 1
                    st.rerun()
        with col5:
            if st.button("⏭ Last", key=f"last_{pdf_key}"):
                st.session_state[f"page_{pdf_key}"] = total_pages
                st.rerun()
    
    # Download options
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        # Download current page as PNG
        buf = io.BytesIO()
        img_copy = img.copy()
        img_copy.save(buf, format="PNG", optimize=True)
        st.download_button(
            label=f"📥 Download Page {page_num} as PNG",
            data=buf.getvalue(),
            file_name=f"{pdf_key}_page_{page_num}.png",
            mime="image/png",
            use_container_width=True
        )
    
    with col2:
        # Download original PDF
        with open(pdf_path, "rb") as f:
            st.download_button(
                label="📥 Download Original PDF",
                data=f.read(),
                file_name=os.path.basename(pdf_path),
                mime="application/pdf",
                use_container_width=True
            )
    
    # Show all pages in an expander
    with st.expander("📄 View All Pages (Thumbnails)"):
        st.info("Scroll through all pages:")
        # Create a grid of thumbnails
        cols_per_row = 2
        for idx in range(0, len(images), cols_per_row):
            cols = st.columns(cols_per_row)
            for col_idx, img_idx in enumerate(range(idx, min(idx + cols_per_row, len(images)))):
                with cols[col_idx]:
                    thumb = images[img_idx].copy()
                    thumb.thumbnail((300, 400))
                    st.image(thumb, use_container_width=True, caption=f"Page {img_idx + 1}")
                    # Add a button to jump to this page
                    if st.button(f"Go to Page {img_idx + 1}", key=f"goto_{pdf_key}_{img_idx}"):
                        st.session_state[f"page_{pdf_key}"] = img_idx + 1
                        st.rerun()


def display_pdf_original(pdf_path, height=700):
    """
    Original display_pdf function using iframe (fallback).
    """
    try:
        with open(pdf_path, "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode('utf-8')
        
        # Create an iframe with the PDF embedded
        pdf_display = f'''
        <iframe
            src="data:application/pdf;base64,{base64_pdf}"
            width="100%"
            height="{height}px"
            type="application/pdf"
            style="border: 1px solid #ddd; border-radius: 5px;"
        ></iframe>
        '''
        st.markdown(pdf_display, unsafe_allow_html=True)
        
        # Add download button
        with open(pdf_path, "rb") as f:
            st.download_button(
                label="📥 Download PDF",
                data=f.read(),
                file_name=os.path.basename(pdf_path),
                mime="application/pdf"
            )
        
    except FileNotFoundError:
        st.error(f"PDF file not found: {pdf_path}")
        st.info("Please ensure the PDF files are in the correct directory.")


# MAIN DISPLAY PDF FUNCTION - REPLACE THE OLD ONE
def display_pdf(pdf_path, height=700):
    """
    Display PDF using images (more reliable for deployment).
    Falls back to iframe method if PyMuPDF is not installed.
    """
    # Check if PDF exists
    if not os.path.exists(pdf_path):
        st.error(f"❌ PDF not found: {pdf_path}")
        st.info("Please ensure the PDF file is in the correct directory.")
        return
    
    # Try to display as images
    try:
        display_pdf_as_images(pdf_path, height)
    except Exception as e:
        st.warning(f"⚠️ Image display failed: {str(e)}")
        st.info("Falling back to iframe display...")
        display_pdf_original(pdf_path, height)