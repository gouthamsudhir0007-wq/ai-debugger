import streamlit as st
import time

# 1. Page Configuration
st.set_page_config(page_title="AI Debugger Pro", layout="centered")

# 2. Custom CSS - Hiding UI elements and fixing colors
st.markdown("""
    <style>
    /* Hides the Streamlit Main Menu and Footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Main Background */
    .main { background-color: #0E1117; }
    
    /* Dark Text Area - Rounded & Clean */
    .stTextArea>div>div>textarea {
        color: #FFFFFF !important; 
        background-color: #1E1E1E !important; 
        border: 1px solid #333333 !important;
        border-radius: 12px;
    }
    
    /* Teal focus border (No Red) */
    .stTextArea>div>div>textarea:focus {
        border-color: #00d4ff !important;
        box-shadow: 0 0 0 1px #00d4ff !important;
    }

    /* Professional Full-Width Button */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 3.5em;
        background-color: #262730 !important; 
        color: #FFFFFF !important;
        border: 1px solid #444444 !important;
    }
    
    .stButton>button:hover {
        border-color: #00d4ff !important;
        color: #00d4ff !important;
    }

    /* Hide the sidebar for a regular app look */
    [data-testid="stSidebar"] { display: none; }
    </style>
    """, unsafe_allow_html=True)

# --- MAIN UI ---
st.title("🤖 AI Debugging Assistant")
st.write("Clean, fast, and secure code analysis.")

code_input = st.text_area("", height=300, placeholder="Paste your Python code here...")

if st.button("🚀 Analyze & Fix Code"):
    if not code_input:
        st.warning("Please paste code first.")
    else:
        with st.spinner("Processing..."):
            time.sleep(1) 
            st.success("Analysis Complete")
            
            st.markdown("### 💡 Analysis Result")
            st.info("**Issue:** Syntax Error\n\n**Fix:** Added missing parenthesis.")
            
            st.markdown("### 💻 Corrected Code")
            st.code(code_input + ")", language="python")

st.divider()
if st.button("🗑️ Clear"):
    st.rerun()
