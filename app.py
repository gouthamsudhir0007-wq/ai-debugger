import streamlit as st
import time

# 1. Page Configuration
st.set_page_config(page_title="AI Debugger Pro", layout="wide")

# 2. Custom CSS - Dark Sidebar & Dark Input
st.markdown("""
    <style>
    /* Hiding Streamlit header/footer for a clean look */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Force Dark Sidebar */
    [data-testid="stSidebar"] {
        background-color: #111111 !important;
        color: white !important;
    }
    
    /* Dark Text Area */
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

    /* Button Styling */
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
    st.title("📂 History")
    st.write("Your recent code fixes:")
    st.divider()
    
    if not st.session_state.history:
        st.info("No history yet.")
    else:
        # Loop through history and show as expanders
        for i, item in enumerate(reversed(st.session_state.history)):
            with st.expander(f"Fix {len(st.session_state.history)-i}: {item['type']}"):
                st.write(f"**Issue:** {item['type']}")
                st.code(item['code'], language="python")
        
        st.divider()
        if st.button("🗑️ Clear History"):
            st.session_state.history = []
            st.rerun()

# --- MAIN UI ---
st.title("🤖 AI Debugging Assistant")
st.write("Paste your code to see the fix.")

code_input = st.text_area("", height=300, placeholder="Enter your Python code...")

if st.button("🚀 Analyze & Fix"):
    if not code_input:
        st.warning("Please enter code first.")
    else:
        with st.spinner("Analyzing..."):
            time.sleep(1)
            
            # Logic for data
            res_type = "Syntax Fix"
            res_code = code_input + " # Fixed"
            
            # Save to Sidebar History
            st.session_state.history.append({"type": res_type, "code": res_code})
            
            st.success("Analysis Complete")
            st.code(res_code, language="python")

if st.button("🗑️ Clear Input"):
    st.rerun()
