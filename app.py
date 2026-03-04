import streamlit as st
import time
import re

# 1. Page Configuration - Sidebar Always Open
st.set_page_config(page_title="Enterprise Logic Debugger", layout="wide", initial_sidebar_state="expanded")

# 2. CSS - Matching Image 1 Exactly
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    [data-testid="stSidebar"] { background-color: #000000 !important; min-width: 300px !important; }
    .stTextArea div[data-baseweb="textarea"] + div { display: none !important; }

    /* Dark Terminal */
    .stTextArea>div>div>textarea {
        background-color: #0b0b0b !important; 
        color: #00ffcc !important; 
        border: 1px solid #333333 !important;
        border-radius: 12px;
        font-family: 'Fira Code', monospace;
    }
    .stTextArea>div>div>textarea:focus { border-color: #00d4ff !important; }

    /* Enterprise Result Cards (Matching Image 1) */
    .error-card {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 10px;
        padding: 24px;
        margin-bottom: 20px;
    }
    .card-header { color: #ffa657; font-weight: 800; font-size: 1.1em; margin-bottom: 8px; }
    .explanation { color: #8b949e; font-size: 0.92em; margin-bottom: 15px; }
    
    .fix-box {
        background-color: #0d1117;
        border: 1px solid #238636;
        border-left: 6px solid #238636;
        padding: 15px;
        border-radius: 8px;
        color: #3fb950;
        font-family: 'Fira Code', monospace;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. State Management
if "history" not in st.session_state: st.session_state.history = []
if "editor_content" not in st.session_state: st.session_state.editor_content = ""
if "fixed_code" not in st.session_state: st.session_state.fixed_code = ""
if "bugs" not in st.session_state: st.session_state.bugs = []

# --- SIDEBAR: HISTORY ---
with st.sidebar:
    st.markdown("<h1 style='color:#00d4ff;'>📂 Version History</h1>", unsafe_allow_html=True)
    if st.button("🗑️ Wipe History"):
        st.session_state.history = []
        st.rerun()
    st.markdown("---")
    for i, code in enumerate(reversed(st.session_state.history)):
        if st.button(f"📄 Entry {len(st.session_state.history)-i}", key=f"h_{i}"):
            st.session_state.editor_content = code
            st.rerun()

# --- MAIN INTERFACE ---
st.title("🤖 Enterprise Python Logic & Syntax Debugger")
code_input = st.text_area("Input Terminal:", height=350, value=st.session_state.editor_content, key="main_editor")

col1, col2 = st.columns([1, 4])

if col1.button("🚀 Analyze & Deep Fix"):
    if not code_input:
        st.warning("Input is empty.")
    else:
        st.session_state.editor_content = code_input
        lines = code_input.split('\n')
        final_lines = []
        st.session_state.bugs = []
        
        # 4. Multi-Pass Analysis Engine
        defined_vars = set(re.findall(r'(\w+)\s*=', code_input))
        
        for i, line in enumerate(lines):
            indent = line[:len(line) - len(line.lstrip())]
            clean = line.strip()
            ln = i + 1
            if not clean:
                final_lines.append(""); continue
            
            t_fix = clean
            t_errs = []

            # Pass 1: Syntax (Colons/Quotes)
            if any(clean.startswith(x) for x in ["def ","if ","for ","while ","elif ","else"]) and not clean.endswith(":"):
                t_errs.append("Missing colon (:) for block start")
                t_fix = t_fix.rstrip() + ":"

            if "print(" in clean and not (re.search(r"['\"].*['\"]", clean) or "+" in clean or "," in clean):
                t_errs.append("Missing quotes in print function")
                inner = clean.split('(', 1)[1].rsplit(')', 1)[0]
                t_fix = f"print('{inner}')"

            # Pass 2: Logic (Equality Errors)
            if clean.startswith("if ") or clean.startswith("elif "):
                if "=" in clean and "==" not in clean and "!=" not in clean and ">=" not in clean and "<=" not in clean:
                    t_errs.append("Logic Error: Using '=' (set value) instead of '==' (check value)")
                    t_fix = t_fix.replace("=", "==")

            # Pass 3: Naming (Variable Typos)
            words = re.findall(r'\b\w+\b', clean)
            for w in words:
                if w in defined_vars: continue
                # Basic fuzzy match for typos
                for d in defined_vars:
                    if len(w) > 3 and w != d and (w in d or d in w) and len(w) - len(d) in [-1, 0, 1]:
                        t_errs.append(f"Possible Typo: '{w}' might be '{d}'")
                        t_fix = t_fix.replace(w, d)

            if t_errs:
                st.session_state.bugs.append({"ln": ln, "msg": " & ".join(t_errs), "fix": t_fix})
            final_lines.append(indent + t_fix)

        st.session_state.fixed_code = "\n".join(final_lines)
        if code_input not in st.session_state.history:
            st.session_state.history.append(code_input)
        st.rerun()

if col2.button("🗑️ Clear All"):
    st.session_state.editor_content = ""
    st.session_state.fixed_code = ""
    st.session_state.bugs = []
    st.rerun()

# 5. Render Enterprise Cards
for bug in st.session_state.bugs:
    st.markdown(f"""
    <div class="error-card">
        <div class="card-header">⚠️ Bug Detected at Line {bug['ln']}</div>
        <div class="explanation">Explanation: Python logic and syntax rules must be followed. This fix ensures correct interpretation by the computer.</div>
        <div class="fix-box">💡 Suggested fix: {bug['fix']}</div>
    </div>
    """, unsafe_allow_html=True)

if st.session_state.fixed_code:
    st.subheader("💻 Corrected Application Block")
    st.code(st.session_state.fixed_code, language="python")
