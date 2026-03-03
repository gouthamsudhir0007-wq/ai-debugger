import streamlit as st
import time

# Page Configuration
st.set_page_config(page_title="AI Debugger Free", layout="wide")

# Custom CSS - Full Dark Theme
st.markdown("""
    <style>
    [data-testid="stSidebar"] { background-color: #111111; color: white; }
    .stTextArea>div>div>textarea {
        color: #FFFFFF !important; 
        background-color: #1E1E1E !important; 
        border: 1px solid #333333 !important;
        border-radius: 8px;
    }
    .stButton>button {
        border-radius: 8px;
        background-color: #262730 !important; 
        color: #FFFFFF !important;
        border: 1px solid #444444 !important;
    }
    .stButton>button:hover { border-color: #00d4ff !important; color: #00d4ff !important; }
    </style>
    """, unsafe_allow_html=True)

if "history" not in st.session_state:
    st.session_state.history = []

# --- SIDEBAR ---
with st.sidebar:
    st.title("📂 Project Lab")
    dev_mode = st.toggle("🛠️ Developer Mode")
    st.divider()
    if not st.session_state.history:
        st.info("No history yet.")
    else:
        for i, item in enumerate(reversed(st.session_state.history)):
            with st.expander(f"Bug: {item['type']}"):
                st.write(item['fix'])
    
    if st.button("🗑️ Clear History"):
        st.session_state.history = []
        st.rerun()

# --- MAIN UI ---
st.title("🤖 AI Debugging Assistant")
st.caption("Running in Free Demo Mode (No Key Required)")

code_input = st.text_area("Paste your code here:", height=300, placeholder="print('Hello'")

col1, col2 = st.columns(2)

if col1.button("🚀 Analyze & Fix") and code_input:
    with st.spinner("Simulating AI Analysis..."):
        time.sleep(1) # Makes it feel real
        
        # This is the "Mock" data that makes it work for free
        res_type = "Syntax Error"
        res_fix = "Check for missing parentheses or quotes."
        res_code = code_input + ")" # Simple simulation
        
        # Update History
        st.session_state.history.append({"type": res_type, "fix": res_fix, "full_code": res_code})
        
        st.success("Analysis Complete!")
        t1, t2 = st.tabs(["💡 Explanation", "💻 Fixed Code"])
        with t1:
            st.write(f"This looks like a **{res_type}**. {res_fix}")
        with t2:
            st.code(res_code, language="python")

        # THIS IS THE DEVELOPER TOGGLE WORKING:
        if dev_mode:
            st.divider()
            st.subheader("🛠️ Raw Developer Data (JSON)")
            st.json({
                "status": "success",
                "model": "Free-Simulator-v1",
                "detected_error": res_type,
                "suggestion": res_fix
            })

if col2.button("🗑️ Clear Input"):
    st.rerun()
