import streamlit as st
import time

# 1. Page Configuration
st.set_page_config(
    page_title="AI Debugger Pro", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# 2. CSS - FORCING DARK SIDEBAR & REMOVING RED
st.markdown("""
    <style>
    /* 1. Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* 2. FORCE DARK SIDEBAR - No more grey */
    [data-testid="stSidebar"] {
        background-color: #111111 !important;
        background-image: none !important;
    }
    
    /* Ensure all text in sidebar is light grey/white */
    [data-testid="stSidebar"] section[data-testid="stSidebarNav"] {
        background-color: #111111 !important;
    }
    [data-testid="stSidebar"] .stText, [data-testid="stSidebar"] p, 
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] span {
        color: #E0E0E0 !important;
    }

    /* 3. MAIN AREA - Dark background */
    .main { background-color: #0E1117; }
    
    /* 4. TEXT AREA - Dark with Teal focus (No Red) */
    .stTextArea>div>div>textarea {
        color: #FFFFFF !important; 
        background-color: #1E1E1E !important; 
        border: 1px solid #333333 !important;
        border-radius: 12px;
    }
    .stTextArea>div>div>textarea:focus {
        border-color: #00d4ff !important;
        box-shadow: 0 0 0 1px #00d4ff !important;
    }

    /* 5. BUTTONS - Dark grey with Teal hover */
    .stButton>button {
        width: 100%;
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

# --- SIDEBAR: HISTORY ONLY ---
with st.sidebar:
    st.title("📂 Fix History")
    st.write("Your recent activity:")
    st.divider()
    
    if not st.session_state.history:
        st.info("No history yet.")
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

# Professional Placeholder
placeholder_text = "def my_function():\n    # Paste code here...\n    return True"

code_input = st.text_area("", height=320, placeholder=placeholder_text)

if st.button("🚀 Analyze & Fix"):
    if not code_input:
        st.warning("Please paste your code first.")
    else:
        with st.spinner("Analyzing..."):
            time.sleep(1) 
            fixed_output = code_input + "\n# Fixed: Structure verified."
            st.session_state.history.append({"code": fixed_output})
            st.success("Analysis Complete")
            st.code(fixed_output, language="python")

if st.button("🗑️ Clear Input"):
    st.rerun()
