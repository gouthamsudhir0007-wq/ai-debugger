import streamlit as st
import time
import sys
import re
from io import StringIO

# 1. Page Configuration - Sidebar Always Open
st.set_page_config(page_title="Python AI Pro", layout="wide", initial_sidebar_state="expanded")

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

    /* Enterprise Result Cards (Matching Image 1) */
    .error-card {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 10px;
        padding: 24px;
        margin-bottom: 20px;
    }
    .card-header { color: #ffa657; font-weight: 800; font-size: 1.2em; margin-bottom: 10px; display: flex; align-items: center; }
    .explanation { color: #8b949e; font-size: 0.95em; margin-bottom: 15px; line-height: 1.5; }
    
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
if "editor_val" not in st.session_state: st.session_state.editor_val = ""
if "fixed_code" not in st.session_state: st.session_state.fixed_code = ""

# --- SIDEBAR: PERMANENTLY VISIBLE ---
with st.sidebar:
    st.markdown("<h1 style='color:#00d4ff;'>📦 Version History</h1>", unsafe_allow_html=True)
    if st.button("🗑️ Wipe All History"):
        st.session_state.history = []
        st.rerun()
    st.markdown("---")
    for i, code in enumerate(reversed(st.session_state.history)):
        if st.button(f"📄 Version {len(st.session_state.history)-i}", key=f"hist_{i}"):
            st.session_state.editor_val = code
            st.rerun()

# --- MAIN INTERFACE ---
st.title("🤖 Enterprise Python Logic & Syntax Debugger")

# Input with Dynamic State
code_input = st.text_area("Input Terminal:", height=350, value=st.session_state.editor_val, key="python_editor")

c1, c2, c3 = st.columns([1, 1, 1])

# 🚀 DEEP ANALYSIS ENGINE
if c1.button("🚀 Analyze & Deep Fix"):
    if not code_input:
        st.warning("Please provide code to analyze.")
    else:
        st.session_state.editor_val = code_input
        lines = code_input.split('\n')
        final_lines = []
        found_bugs = []
        
        for i, line in enumerate(lines):
            indent = line[:len(line) - len(line.lstrip())]
            clean = line.strip()
            ln = i + 1
            if not clean:
                final_lines.append(""); continue
            
            temp_fix = clean
            line_errs = []

            # A. Block Keywords & Colons
            if any(clean.startswith(x) for x in ["def ","if ","for ","while ","elif ","else"]) and not clean.endswith(":"):
                line_errs.append("Missing colon (:) at end of block statement.")
                temp_fix = temp_fix.rstrip() + ":"

            # B. Advanced Print & String Check
            if "print(" in clean:
                if not (clean.count('"') >= 2 or clean.count("'") >= 2 or "+" in clean or "," in clean):
                    line_errs.append("Missing string delimiters (quotes) in print function.")
                    inner = clean.split('(', 1)[1].rsplit(')', 1)[0]
                    temp_fix = f"print('{inner}')"
                if clean.count('(') != clean.count(')'):
                    line_errs.append("Parentheses mismatch (unclosed bracket).")
                    temp_fix = temp_fix + ")"

            # C. Logic Check: Assignment vs Equality
            if clean.startswith("if ") and "=" in clean and "==" not in clean and "!=" not in clean:
                line_errs.append("Logic Error: Using '=' (assignment) instead of '==' (comparison).")
                temp_fix = temp_fix.replace("=", "==")

            if line_errs:
                found_bugs.append({"line": ln, "msg": " | ".join(line_errs), "fix": temp_fix})
            final_lines.append(indent + temp_fix)

        st.session_state.fixed_code = "\n".join(final_lines)
        if code_input not in st.session_state.history:
            st.session_state.history.append(code_input)

        # Display Enterprise Cards
        for bug in found_bugs:
            st.markdown(f"""
            <div class="error-card">
                <div class="card-header">⚠️ Bug Detected at Line {bug['line']}</div>
                <div class="explanation"><b>Explanation:</b> Python syntax and logic rules must be followed for the interpreter to execute code. This error prevents code from running or causes incorrect results.</div>
                <div class="fix-box">💡 Suggested fix: {bug['fix']}</div>
            </div>
            """, unsafe_allow_html=True)

        st.subheader("💻 Corrected Application Block")
        st.code(st.session_state.fixed_code, language="python")

# ▶️ SMART RUNNER
if c2.button("▶️ Run Program"):
    if st.session_state.fixed_code:
        st.subheader("🖥️ Enterprise Console")
        old_stdout = sys.stdout
        sys.stdout = capture = StringIO()
        try:
            # Handle input() mock
            exec_globals = {"input": lambda p="": "DemoValue"}
            exec(st.session_state.fixed_code, exec_globals)
            sys.stdout = old_stdout
            st.markdown(f'<div class="console-box">{capture.getvalue() or "Process finished (Exit Code 0)"}</div>', unsafe_allow_html=True)
        except Exception as e:
            sys.stdout = old_stdout
            st.error(f"Execution Error: {e}")

# 🗑️ RESET MASTER
if c3.button("🗑️ Clear All"):
    st.session_state.editor_val = ""
    st.session_state.fixed_code = ""
    st.rerun()
