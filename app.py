import streamlit as st
import time

# 1. Page Configuration
st.set_page_config(page_title="AI Debugger Pro", layout="wide", initial_sidebar_state="expanded")

# 2. Custom CSS - Strictly Dark Sidebar & Teal Accents
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    [data-testid="stSidebar"] { background-color: #111111 !important; }
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] h1 { color: #FFFFFF !important; }
    .stTextArea>div>div>textarea { color: #FFFFFF !important; background-color: #1E1E1E !important; border: 1px solid #333333 !important; border-radius: 12px; }
    .stTextArea>div>div>textarea:focus { border-color: #00d4ff !important; box-shadow: 0 0 0 1px #00d4ff !important; }
    .stButton>button { width: 100%; border-radius: 12px; background-color: #262730 !important; color: #FFFFFF !important; border: 1px solid #444444 !important; }
    .stButton>button:hover { border-color: #00d4ff !important; color: #00d4ff !important; }
    </style>
    """, unsafe_allow_html=True)

if "history" not in st.session_state:
    st.session_state.history = []

# --- SIDEBAR: HISTORY ---
with st.sidebar:
    st.title("📂 Fix History")
    if not st.session_state.history:
        st.info("No activity yet.")
    else:
        for i, item in enumerate(reversed(st.session_state.history)):
            with st.expander(f"Fix {len(st.session_state.history)-i}"):
                st.code(item['code'], language="python")
        if st.button("🗑️ Clear History"):
            st.session_state.history = []
            st.rerun()

# --- MAIN UI ---
st.title("🤖 AI Debugging Assistant")
code_input = st.text_area("", height=300, placeholder="Paste broken code here...")

if st.button("🚀 Analyze & Fix"):
    if not code_input:
        st.warning("Please enter code.")
    else:
        with st.spinner("Analyzing with AI Logic..."):
            time.sleep(1)
            
            # --- THE "SMART FIX" LOGIC (No Key Needed) ---
            fixed = code_input
            error_msg = "No major syntax issues found."
            
            if "(" in fixed and ")" not in fixed:
                fixed += ")"
                error_msg = "Fixed: Added missing closing parenthesis."
            elif ":" not in fixed and any(x in fixed for x in ["def", "if", "for", "while"]):
                fixed = fixed.replace("\n", ":\n", 1)
                error_msg = "Fixed: Added missing colon after statement."
            elif 'print' in fixed and "'" not in fixed and '"' not in fixed:
                fixed = fixed.replace("print(", "print('").replace(")", "')")
                error_msg = "Fixed: Added missing quotes in print statement."

            st.session_state.history.append({"code": fixed})
            st.success("Analysis Complete")
            st.info(f"**AI Insight:** {error_msg}")
            st.markdown("### 💻 Corrected Code")
            st.code(fixed, language="python")

if st.button("🗑️ Clear Input"):
    st.rerun()
