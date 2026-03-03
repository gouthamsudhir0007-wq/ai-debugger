import streamlit as st
import time

# 1. Page Configuration
st.set_page_config(
    page_title="AI Debugger Pro", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# 2. Custom CSS - Strictly Dark Theme & Teal Accents
st.markdown("""
    <style>
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Force Dark Sidebar */
    [data-testid="stSidebar"] {
        background-color: #111111 !important;
        border-right: 1px solid #333333;
    }
    
    /* Sidebar Text Styling */
    [data-testid="stSidebar"] .stText, 
    [data-testid="stSidebar"] p, 
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2 {
        color: #E0E0E0 !important;
    }

    /* Dark Input Area */
    .stTextArea>div>div>textarea {
        color: #FFFFFF !important; 
        background-color: #1E1E1E !important; 
        border: 1px solid #333333 !important;
        border-radius: 10px;
    }

    /* Teal focus border (No Red) */
    .stTextArea>div>div>textarea:focus {
        border-color: #00d4ff !important;
        box-shadow: 0 0 0 1px #00d4ff !important;
    }

    /* Professional Button Styling */
    .stButton>button {
        border-radius: 10px;
        background-color: #262730 !important; 
        color: #FFFFFF !important;
        border: 1px solid #444444 !important;
        transition: 0.3s;
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
    st.write("Your recent code fixes:")
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
st.write("Professional Python Code Analysis")

# Valid Professional Placeholder
valid_placeholder = "def calculate_sum(a, b):\n    return a + b\n\n# Paste your broken code here..."

code_input = st.text_area("", height=300, placeholder=valid_placeholder)

if st.button("🚀 Analyze & Fix"):
    if not code_input:
        st.warning("Please enter some code to analyze.")
    else:
        with st.spinner("Processing..."):
            time.sleep(1) 
            
            # Simulated Fix Logic
            fixed_code = code_input + "\n# Analysis: Code structure verified."
            
            # Save to History
            st.session_state.history.append({"code": fixed_code})
            
            st.success("Analysis Complete")
            st.markdown("### 💻 Corrected Code")
            st.code(fixed_code, language="python")

if st.button("🗑️ Clear Current Input"):
    st.rerun()
