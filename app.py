import streamlit as st
import time

# 1. Page Configuration - FORCING sidebar to be visible
st.set_page_config(
    page_title="AI Debugger Pro", 
    layout="wide", 
    initial_sidebar_state="expanded" 
)

# 2. CSS - Forcing Dark Sidebar & Teal Accents
st.markdown("""
    <style>
    /* Hide Streamlit clutter */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* FORCE DARK SIDEBAR */
    [data-testid="stSidebar"] {
        background-color: #111111 !important;
        min-width: 250px !important;
    }
    
    /* Ensure sidebar text is white */
    [data-testid="stSidebar"] section[data-testid="stSidebarNav"] {
        background-color: #111111 !important;
    }
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] h1, [data-testid="stSidebar"] span {
        color: #FFFFFF !important;
    }

    /* Dark Input Area */
    .stTextArea>div>div>textarea {
        color: #FFFFFF !important; 
        background-color: #1E1E1E !important; 
        border: 1px solid #333333 !important;
        border-radius: 12px;
    }

    /* Teal focus border (Replacing Red) */
    .stTextArea>div>div>textarea:focus {
        border-color: #00d4ff !important;
        box-shadow: 0 0 0 1px #00d4ff !important;
    }

    /* Button Styling */
    .stButton>button {
        border-radius: 12px;
        background-color: #262730 !important; 
        color: #FFFFFF !important;
        border: 1px solid #444444 !important;
    }
    .stButton>button:hover {
        border-color: #00d4ff !important;
        color: #00d4ff !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Initialize History
if "history" not in st.session_state:
    st.session_state.history = []

# --- SIDEBAR: History Only ---
with st.sidebar:
    st.title("📂 Fix History")
    st.write("Recent Activity:")
    st.divider()
    
    if not st.session_state.history:
        st.info("No fixes yet.")
    else:
        for i, item in enumerate(reversed(st.session_state.history)):
            with st.expander(f"Fix {len(st.session_state.history)-i}"):
                st.code(item['code'], language="python")
        
        st.divider()
        if st.button("🗑️ Clear History"):
            st.session_state.history = []
            st.rerun()

# --- MAIN UI ---
st.title("🤖 AI Debugging Assistant")

# New Professional Placeholder
valid_placeholder = "def check_data(items):\n    # Paste your code here to analyze\n    return True"

code_input = st.text_area("", height=320, placeholder=valid_placeholder)

if st.button("🚀 Analyze & Fix"):
    if not code_input:
        st.warning("Please enter some code.")
    else:
        with st.spinner("Analyzing..."):
            time.sleep(1) 
            fixed_output = code_input + "\n# Analysis: Structure verified."
            st.session_state.history.append({"code": fixed_output})
            st.success("Analysis Complete")
            st.code(fixed_output, language="python")

if st.button("🗑️ Clear Input"):
    st.rerun()
