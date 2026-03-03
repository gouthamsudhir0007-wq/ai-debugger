import streamlit as st
import time

# 1. Page Configuration - Force Sidebar to be visible
st.set_page_config(
    page_title="AI Debugger Pro", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# 2. Custom CSS - Strictly Dark Sidebar & Teal Accents
st.markdown("""
    <style>
    /* Hiding Streamlit clutter */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Professional Dark Sidebar */
    [data-testid="stSidebar"] {
        background-color: #111111 !important;
    }
    
    /* Ensuring sidebar text is white */
    [data-testid="stSidebar"] section[data-testid="stSidebarNav"] {
        background-color: #111111 !important;
    }
    
    [data-testid="stSidebar"] .stText, [data-testid="stSidebar"] p, [data-testid="stSidebar"] h1 {
        color: white !important;
    }

    /* Dark Input Area */
    .stTextArea>div>div>textarea {
        color: #FFFFFF !important; 
        background-color: #1E1E1E !important; 
        border: 1px solid #333333 !important;
        border-radius: 10px;
    }

    /* Teal focus (No Red) */
    .stTextArea>div>div>textarea:focus {
        border-color: #00d4ff !important;
        box-shadow: 0 0 0 1px #00d4ff !important;
    }

    /* Professional Buttons */
    .stButton>button {
        border-radius: 10px;
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

# --- SIDEBAR (History Only) ---
with st.sidebar:
    st.title("📂 Fix History")
    st.write("Your recent activity:")
    st.divider()
    
    if not st.session_state.history:
        st.info("No fixes yet.")
    else:
        # Show history items
        for i, item in enumerate(reversed(st.session_state.history)):
            with st.expander(f"Fix {len(st.session_state.history)-i}"):
                st.write(f"**Status:** Fixed")
                st.code(item['code'], language="python")
        
        st.divider()
        if st.button("🗑️ Clear History"):
            st.session_state.history = []
            st.rerun()

# --- MAIN UI ---
st.title("🤖 AI Debugging Assistant")

code_input = st.text_area("Paste code here:", height=300, placeholder="print('Hello'")

if st.button("🚀 Analyze & Fix"):
    if not code_input:
        st.warning("Please enter code first.")
    else:
        with st.spinner("Analyzing..."):
            time.sleep(1) # Fake delay for realism
            
            # Simulated Fix
            res_code = code_input + " # Fixed"
            
            # Save to History
            st.session_state.history.append({"code": res_code})
            
            st.success("Analysis Complete")
            st.code(res_code, language="python")

if st.button("🗑️ Clear Input"):
    st.rerun()
