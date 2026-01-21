HIDE_SIDEBAR_NAV = """
<style>
    /* Hide the default multi-page navigation */
    [data-testid="stSidebarNav"] {
        display: none;
    }
    
    /* Make the custom sidebar navigation more prominent */
    .sidebar .sidebar-content {
        padding-top: 2rem;
    }
</style>
"""

SIDEBAR_STYLES = {
    "container": {"padding": "1!important", "background-color": "#fafafa"},
    "icon": {"color": "#FCA500", "font-size": "24px"}, 
    "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px", "--hover-color": "#eee"},
    "nav-link-selected": {"background-color": "#68AD3A"}
}

GRID_BUTTONS_STYLE = """
<style>
    .stButton > button {
        width: 100%;
        height: 80px;
        border-radius: 8px;
        border: 1px solid #e0e0e0;
        font-size: 15px;
        font-weight: 500;
        background: white;
        color: #333;
    }
    
    .stButton > button:hover {
        border-color: #68AD3A;
        color: #68AD3A;
        background: #f8fff8;
    }
</style>
"""

BUTTON_STYLE= """
<style>
    div[data-testid="column"]:nth-of-type({(i % num_cols) + 1}) button {{
        background: {btn['color']} !important;
    }}
</style>
""" 

TEXT_JUSTIFIED = """
<style>
    .justified-text {
        text-align: justify;
        text-justify: inter-word;
    }
    
    /* Apply to all Streamlit markdown */
    .stMarkdown {
        text-align: justify;
    }
</style>
"""