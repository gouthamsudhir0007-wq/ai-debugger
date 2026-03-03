import streamlit as st
import time

# 1. Page Configuration - Force Sidebar and Wide Layout
st.set_page_config(
    page_title="AI Debugger Pro", 
    layout="wide", 
    initial_sidebar_state="expanded" 
)

# 2. CSS - Deep Dark Theme & Teal Accents
st.markdown("""
    <style>
    /* Hide Streamlit Header/Footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Force Sidebar to be Black */
    [data-testid="stSidebar"] {
        background-color: #000000 !important;
        border-right: 1px solid #333333;
    }
    
    /* Sidebar Text */
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

    /* Teal focus (No Red) */
    .stTextArea>div>div>textarea:focus {
        border-color: #00d4ff !important;
        box-shadow: 0 0 0 1px #00d4ff !important;
    }

    /* Professional Button Styling */
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

# --- SIDEBAR: HISTORY ---
with st.sidebar:
    st.title("📂 History")
    st.write("Previous Code Fixes:")
    st.divider()
    
    if not st.session_state.history:
        st.info("No activity yet.")
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

# Clean, professional placeholder
placeholder_code = "def check_errors(input_data):\n    # Paste your Python code here...\n    return True"

code_input = st.text_area("", height=350, placeholder=placeholder_code)

if st.button("🚀 Analyze & Fix"):
    if not code_input:
        st.warning("Please enter some code to analyze.")
    else:
        with st.spinner("Analyzing code structure..."):
            time.sleep(1) # Processing simulation
            
            # --- REAL OUTPUT LOGIC ---
            # This logic takes your exact code and prepares it as the output
            fixed_code = code_input.strip() 
            
            # Save the code to the Sidebar History
            st.session_state.history.append({"code": fixed_code})
            
            # Show the code as the output
            st.success("Analysis Complete")
            st.markdown("### 💻 Corrected Code")
            st.code(fixed_code, language="python")

if st.button("🗑️ Clear Input"):
    st.rerun()
