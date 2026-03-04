import streamlit as st
import re

# 1. Page Configuration - Sidebar Locked
st.set_page_config(page_title="Master Python Debugger", layout="wide", initial_sidebar_state="expanded")

# 2. CSS - NO RED / TEAL FOCUS / SIDEBAR VISIBLE
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    [data-testid="stSidebar"] { background-color: #000000 !important; min-width: 260px !important; }
    
    /* Terminal - Dark/Teal focus, No Red */
    .stTextArea div[data-baseweb="textarea"] { border: 1px solid #333333 !important; }
    .stTextArea div[data-baseweb="textarea"]:focus-within { border: 1px solid #00d4ff !important; }
    .stTextArea textarea { background-color: #0b0b0b !important; color: #00ffcc !important; font-family: 'Fira Code', monospace; }
    .stTextArea div[data-baseweb="textarea"] + div { display: none !important; }

    /* Enterprise Cards */
    .error-card { background-color: #161b22; border: 1px solid #30363d; border-radius: 10px; padding: 20px; margin-bottom: 15px; }
    .card-header { color: #ffa657; font-weight: 800; font-size: 1.1em; }
    .explanation { color: #8b949e; font-size: 0.9em; margin-bottom: 10px; }
    .fix-box { background-color: #0d1117; border-left: 6px solid #238636; padding: 12px; border-radius: 8px; color: #3fb950; font-family: monospace; }
    </style>
    """, unsafe_allow_html=True)

# 3. State Setup
if "history" not in st.session_state: st.session_state.history = []
if "code" not in st.session_state: st.session_state.code = ""
if "fixed" not in st.session_state: st.session_state.fixed = ""
if "bugs" not in st.session_state: st.session_state.bugs = []

# --- SIDEBAR: HISTORY ---
with st.sidebar:
    st.markdown("<h2 style='color:#00d4ff;'>📂 Code Versions</h2>", unsafe_allow_html=True)
    if st.button("🗑️ Clear History"):
        st.session_state.history = []
        st.rerun()
    st.markdown("---")
    for i, item in enumerate(reversed(st.session_state.history)):
        if st.button(f"📄 Version {len(st.session_state.history)-i}", key=f"v_{i}"):
            st.session_state.code = item
            st.rerun()

# --- MAIN INTERFACE ---
st.title("🤖 Master Python Logic & Syntax Debugger")
user_input = st.text_area("Input Terminal:", height=350, value=st.session_state.code, key="editor")

c1, c2 = st.columns([1, 5])

if c1.button("🚀 Analyze & Fix"):
    if not user_input:
        st.warning("Enter code first.")
    else:
        st.session_state.code = user_input
        lines = user_input.split('\n')
        corrected = []
        st.session_state.bugs = []
        
        # MAP DEFINED VARIABLES
        # Catches: x = 10, def func(a, b):, for i in...
        defined = set(re.findall(r'\b(\w+)\b\s*=', user_input))
        defined.update(re.findall(r'def\s+(\w+)', user_input))
        defined.update(re.findall(r'def\s+\w+\((.*?)\)', user_input)) # args
        defined.update(["print", "int", "input", "range", "len", "str", "float"]) # built-ins

        for i, line in enumerate(lines):
            indent = line[:len(line) - len(line.lstrip())]
            clean = line.strip()
            if not clean or clean.startswith("#"):
                corrected.append(line); continue
            
            f_line, f_errs = clean, []

            # 1. Syntax: Colons
            if any(clean.startswith(x) for x in ["def ","if ","for ","while ","elif ","else"]) and not clean.endswith(":"):
                f_errs.append("Missing colon (:)")
                f_line = f_line.rstrip() + ":"

            # 2. Syntax: Unclosed Brackets
            if clean.count("(") > clean.count(")"):
                f_errs.append("Unclosed parenthesis")
                f_line += ")" * (clean.count("(") - clean.count(")"))

            # 3. Syntax: Naked Strings in Print
            if "print(" in clean and not (re.search(r"['\"].*['\"]", clean) or "+" in clean or "," in clean):
                f_errs.append("Missing quotes in print")
                inner = clean.split('(', 1)[1].rsplit(')', 1)[0]
                f_line = f_line.replace(inner, f"'{inner}'")

            # 4. Logic: Assignment in If/Elif
            if (clean.startswith("if ") or clean.startswith("elif ")) and "=" in clean and "==" not in clean:
                f_errs.append("Logic: '=' used instead of '=='")
                f_line = f_line.replace("=", "==")

            # 5. Naming: Variable Typos
            words = re.findall(r'\b\w+\b', clean)
            for w in words:
                if w.isdigit() or w in defined or len(w) < 3: continue
                # Fuzzy match for typos
                for d in defined:
                    if w != d and (w in d or d in w) and abs(len(w)-len(d)) <= 1:
                        f_errs.append(f"Typo: '{w}' should likely be '{d}'")
                        f_line = f_line.replace(w, d)

            if f_errs:
                st.session_state.bugs.append({"ln": i+1, "msg": " & ".join(f_errs), "fix": f_line})
            corrected.append(indent + f_line)

        st.session_state.fixed = "\n".join(corrected)
        if user_input not in st.session_state.history:
            st.session_state.history.append(user_input)
        st.rerun()

if c2.button("🗑️ Clear All"):
    st.session_state.code = ""
    st.session_state.fixed = ""
    st.session_state.bugs = []
    st.rerun()

# RENDER
for bug in st.session_state.bugs:
    st.markdown(f"""
    <div class="error-card">
        <div class="card-header">⚠️ Error Detected at Line {bug['ln']}</div>
        <div class="explanation">Explanation: Fixed syntax/logic to prevent Python execution failure.</div>
        <div class="fix-box">💡 Suggested fix: {bug['fix']}</div>
    </div>
    """, unsafe_allow_html=True)

if st.session_state.fixed:
    st.subheader("💻 Corrected Application Block")
    st.code(st.session_state.fixed, language="python")
