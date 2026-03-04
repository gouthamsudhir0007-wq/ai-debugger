import streamlit as st
import time
import sys
import re
from io import StringIO

# 1. Page Configuration - Sidebar Always Open
st.set_config = st.set_page_config(page_title="Python AI Pro", layout="wide", initial_sidebar_state="expanded")

# 2. CSS - ENTERPRISE STYLING & SIDEBAR LOCK
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    [data-testid="stSidebar"] { background-color: #000000 !important; min-width: 300px !important; }
    
    /* HIDE THE "Press Ctrl+Enter" HINT */
    .stTextArea div[data-baseweb="textarea"] + div { display: none !important; }

    /* Terminal Styling */
    .stTextArea>div>div>textarea {
        background-color: #0b0b0b !important; 
        color: #00ffcc !important; 
        border: 1px solid #333333 !important;
        border-radius: 12px;
        font-family: 'Fira Code', monospace;
    }
    .stTextArea>div>div>textarea:focus {
        border-color: #00d4ff !important;
        box-shadow: 0 0 0 2px rgba(0, 212, 255, 0.2) !important;
    }

    /* Enterprise Result Cards */
    .error-card {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 10px;
        padding: 24px;
        margin-bottom: 20px;
    }
    .card-header { color: #ffa657; font-weight: 800; font-size: 1.2em; margin-bottom: 10px; }
    .explanation { color: #8b949e; font-size: 0.95em; margin-bottom: 15px; }
    
    .fix-box {
        background-color: #0d1117;
        border: 1px solid #238636;
        border-left: 6px solid #238636;
        padding: 15px;
        border-radius: 8px;
        color: #3fb950;
        font-family: 'Fira Code', monospace;
    }

    .console-box {
        background-color: #000000;
        border: 2px solid #00d4ff;
        color: #00ff00;
        padding: 20px;
        font-family: 'Courier New', monospace;
        border-radius: 10px;
        white-space: pre-wrap;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Enhanced State Management
if "history" not in st.session_state: st.session_state.history = []
if "main_code" not in st.session_state: st.session_state.main_code = ""
if "fixed_code" not in st.session_state: st.session_state.fixed_code = ""
if "analysis_log" not in st.session_state: st.session_state.analysis_log = []

# --- SIDEBAR: HISTORY ---
with st.sidebar:
    st.markdown("<h1 style='color:#00d4ff;'>📦 Versions</h1>", unsafe_allow_html=True)
    if st.button("🗑️ Wipe All History"):
        st.session_state.history = []
        st.rerun()
    st.markdown("---")
    for i, code in enumerate(reversed(st.session_state.history)):
        if st.button(f"📄 Code Entry {len(st.session_state.history)-i}", key=f"h_{i}"):
            st.session_state.main_code = code
            st.rerun()

# --- MAIN UI ---
st.title("🤖 Enterprise Python Logic & Syntax Debugger")

# Fixed: The editor is now directly linked to 'main_code' session state
user_input = st.text_area("Input Terminal:", height=350, value=st.session_state.main_code, key="primary_editor")

c1, c2, c3 = st.columns([1, 1, 1])

# 🚀 ANALYZE & FIX
if c1.button("🚀 Analyze & Deep Fix"):
    if not user_input:
        st.warning("Input terminal is empty.")
    else:
        st.session_state.main_code = user_input # Sync typing area
        lines = user_input.split('\n')
        final_lines = []
        st.session_state.analysis_log = []
        
        for i, line in enumerate(lines):
            indent = line[:len(line) - len(line.lstrip())]
            clean = line.strip()
            if not clean:
                final_lines.append(""); continue
            
            temp_fix = clean
            errs = []

            # 1. Colon Check
            if any(clean.startswith(x) for x in ["def ","if ","for ","while ","elif ","else"]) and not clean.endswith(":"):
                errs.append("Missing colon (:)")
                temp_fix = temp_fix.rstrip() + ":"

            # 2. Print Quote Check
            if "print(" in clean and not (re.search(r"['\"].*['\"]", clean) or "+" in clean or "," in clean):
                errs.append("Missing string quotes")
                inner = clean.split('(', 1)[1].rsplit(')', 1)[0]
                temp_fix = f"print('{inner}')"

            # 3. Logic: Assignment vs Equality
            if clean.startswith("if ") and "=" in clean and "==" not in clean:
                errs.append("Logic Error: '=' used instead of '=='")
                temp_fix = temp_fix.replace("=", "==")

            if errs:
                st.session_state.analysis_log.append({"ln": i+1, "msg": " & ".join(errs), "fix": temp_fix})
            final_lines.append(indent + temp_fix)

        st.session_state.fixed_code = "\n".join(final_lines)
        if user_input not in st.session_state.history:
            st.session_state.history.append(user_input)
        st.rerun()

# Display Results if they exist
for bug in st.session_state.analysis_log:
    st.markdown(f"""
    <div class="error-card">
        <div class="card-header">⚠️ Bug Detected at Line {bug['ln']}</div>
        <div class="explanation">Explanation: Python syntax requires specific formatting to execute. This fixed version ensures the interpreter understands your logic.</div>
        <div class="fix-box">💡 Suggested fix: {bug['fix']}</div>
    </div>
    """, unsafe_allow_html=True)

if st.session_state.fixed_code:
    st.subheader("💻 Corrected Application Block")
    st.code(st.session_state.fixed_code, language="python")

# ▶️ RUN PROGRAM (FIXED TO RUN THE CORRECTED CODE)
if c2.button("▶️ Run Program"):
    if not st.session_state.fixed_code:
        st.error("Please 'Analyze & Fix' the code before running.")
    else:
        st.subheader("🖥️ Enterprise Console")
        old_stdout = sys.stdout
        sys.stdout = capture = StringIO()
        try:
            # Mock input to prevent freezing
            exec_env = {"input": lambda p="": "Admin"}
            exec(st.session_state.fixed_code, exec_env)
            sys.stdout = old_stdout
            st.markdown(f'<div class="console-box">{capture.getvalue() or "Finished (No Output)."}</div>', unsafe_allow_html=True)
        except Exception as e:
            sys.stdout = old_stdout
            st.error(f"Execution Error: {e}")

# 🗑️ CLEAR ALL (TOTAL RESET)
if c3.button("🗑️ Clear All"):
    st.session_state.main_code = ""
    st.session_state.fixed_code = ""
    st.session_state.analysis_log = []
    st.rerun()
