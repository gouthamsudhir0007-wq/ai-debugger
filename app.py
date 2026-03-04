import streamlit as st
import re

# 1. Page Configuration - Sidebar Hard-Locked Open
st.set_page_config(
    page_title="Enterprise Python Logic Debugger",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. CSS - ABSOLUTELY NO RED / SIDEBAR LOCK
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    
    /* Force Sidebar Visibility */
    [data-testid="stSidebar"] { 
        background-color: #000000 !important; 
        min-width: 260px !important;
    }

    /* Input Terminal - NO RED BORDERS */
    .stTextArea div[data-baseweb="textarea"] {
        border: 1px solid #333333 !important;
    }
    .stTextArea div[data-baseweb="textarea"]:focus-within {
        border: 1px solid #00d4ff !important;
    }
    .stTextArea textarea {
        background-color: #0b0b0b !important; 
        color: #00ffcc !important; 
        font-family: 'Fira Code', monospace;
    }

    /* Hide the 'Press Ctrl+Enter' hint */
    .stTextArea div[data-baseweb="textarea"] + div { display: none !important; }

    /* Enterprise Cards (Image 1 Style) */
    .error-card {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 15px;
    }
    .card-header { color: #ffa657; font-weight: 800; font-size: 1.1em; }
    .explanation { color: #8b949e; font-size: 0.9em; margin-bottom: 10px; }
    
    .fix-box {
        background-color: #0d1117;
        border-left: 6px solid #238636;
        padding: 12px;
        border-radius: 8px;
        color: #3fb950;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. State Management
if "history" not in st.session_state: st.session_state.history = []
if "main_editor" not in st.session_state: st.session_state.main_editor = ""
if "fixed_code" not in st.session_state: st.session_state.fixed_code = ""
if "bugs" not in st.session_state: st.session_state.bugs = []

# --- SIDEBAR: CONTENT ENSURES VISIBILITY ---
with st.sidebar:
    st.markdown("<h2 style='color:#00d4ff;'>📂 Code Versions</h2>", unsafe_allow_html=True)
    if st.button("🗑️ Clear History"):
        st.session_state.history = []
        st.rerun()
    st.markdown("---")
    for i, code in enumerate(reversed(st.session_state.history)):
        if st.button(f"📄 Version {len(st.session_state.history)-i}", key=f"v_{i}"):
            st.session_state.main_editor = code
            st.rerun()

# --- MAIN UI ---
st.title("🤖 Enterprise Python Logic & Syntax Debugger")

# Linked Input
user_input = st.text_area("Input Terminal:", height=350, value=st.session_state.main_editor, key="editor_key")

col1, col2 = st.columns([1, 5])

if col1.button("🚀 Analyze & Fix"):
    if not user_input:
        st.warning("Input is empty.")
    else:
        st.session_state.main_editor = user_input
        lines = user_input.split('\n')
        corrected_lines = []
        st.session_state.bugs = []
        
        for i, line in enumerate(lines):
            indent = line[:len(line) - len(line.lstrip())]
            clean = line.strip()
            if not clean:
                corrected_lines.append(""); continue
            
            fix, errs = clean, []

            # Syntax: Block colons
            if any(clean.startswith(x) for x in ["def ","if ","for ","while ","elif ","else"]) and not clean.endswith(":"):
                errs.append("Missing colon (:)")
                fix = fix.rstrip() + ":"

            # Syntax: String quotes
            if "print(" in clean and not (re.search(r"['\"].*['\"]", clean) or "+" in clean or "," in clean):
                errs.append("Missing string quotes")
                inner = clean.split('(', 1)[1].rsplit(')', 1)[0]
                fix = f"print('{inner}')"

            # Logic: Equality check
            if (clean.startswith("if ") or clean.startswith("elif ")) and "=" in clean and "==" not in clean:
                errs.append("Logic Error: '=' instead of '=='")
                fix = fix.replace("=", "==")

            if errs:
                st.session_state.bugs.append({"ln": i+1, "msg": " & ".join(errs), "fix": fix})
            corrected_lines.append(indent + fix)

        st.session_state.fixed_code = "\n".join(corrected_lines)
        if user_input not in st.session_state.history:
            st.session_state.history.append(user_input)
        st.rerun()

if col2.button("🗑️ Clear All"):
    st.session_state.main_editor = ""
    st.session_state.fixed_code = ""
    st.session_state.bugs = []
    st.rerun()

# --- RENDER ANALYSIS ---
for bug in st.session_state.bugs:
    st.markdown(f"""
    <div class="error-card">
        <div class="card-header">⚠️ Bug at Line {bug['ln']}</div>
        <div class="explanation">Explanation: Corrected syntax to ensure the Python interpreter can process your logic.</div>
        <div class="fix-box">💡 Suggested fix: {bug['fix']}</div>
    </div>
    """, unsafe_allow_html=True)

if st.session_state.fixed_code:
    st.subheader("💻 Corrected Application Block")
    st.code(st.session_state.fixed_code, language="python")
