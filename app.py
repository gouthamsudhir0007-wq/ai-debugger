import streamlit as st
import re

# 1. Page Configuration
st.set_page_config(page_title="Master Python Debugger", layout="wide")

# 2. CSS - ENTERPRISE UI (No Red, Deep Teal Focus)
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    
    /* Input Terminal Styling */
    .stTextArea div[data-baseweb="textarea"] { border: 1px solid #333333 !important; }
    .stTextArea div[data-baseweb="textarea"]:focus-within { border: 1px solid #00d4ff !important; }
    .stTextArea textarea { 
        background-color: #0b0b0b !important; 
        color: #00ffcc !important; 
        font-family: 'Fira Code', monospace; 
    }

    /* Enterprise Analysis Cards */
    .error-card {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 15px;
    }
    .card-header { color: #ffa657; font-weight: 800; font-size: 1.1em; margin-bottom: 8px; }
    .explanation { color: #8b949e; font-size: 0.9em; margin-bottom: 12px; line-height: 1.4; }
    
    .fix-box {
        background-color: #0d1117;
        border-left: 6px solid #238636;
        padding: 12px;
        border-radius: 8px;
        color: #3fb950;
        font-family: 'Fira Code', monospace;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Persistent State
if "main_code" not in st.session_state: st.session_state.main_code = ""
if "fixed_code" not in st.session_state: st.session_state.fixed_code = ""
if "detected_bugs" not in st.session_state: st.session_state.detected_bugs = []

# --- MAIN UI ---
st.title("🤖 Enterprise Python Logic & Syntax Debugger")

user_input = st.text_area("Input Terminal:", height=350, value=st.session_state.main_code)

col1, col2 = st.columns([1, 5])

# 🚀 DEEP ANALYSIS FEATURE (RESTORED)
if col1.button("🚀 Analyze & Deep Fix"):
    if not user_input:
        st.warning("Input terminal is empty.")
    else:
        st.session_state.main_code = user_input
        lines = user_input.split('\n')
        corrected_lines = []
        st.session_state.detected_bugs = []
        
        # VARIABLE MAPPING (For Typo Detection)
        # Finds: var = x, def func(param), for i in...
        defined_vars = set(re.findall(r'\b(\w+)\b\s*=', user_input))
        defined_vars.update(re.findall(r'def\s+(\w+)', user_input))
        args = re.findall(r'def\s+\w+\((.*?)\)', user_input)
        for arg_set in args:
            for a in arg_set.split(','):
                defined_vars.add(a.strip())
        # Add common built-ins
        defined_vars.update(["print", "int", "input", "range", "len", "str", "float", "if", "elif", "else"])

        for i, line in enumerate(lines):
            indent = line[:len(line) - len(line.lstrip())]
            clean = line.strip()
            if not clean or clean.startswith("#"):
                corrected_lines.append(line); continue
            
            f_line, f_errs = clean, []

            # 1. SYNTAX: Missing Colons
            if any(clean.startswith(x) for x in ["def ","if ","for ","while ","elif ","else"]) and not clean.endswith(":"):
                f_errs.append("Missing colon (:)")
                f_line = f_line.rstrip() + ":"

            # 2. SYNTAX: String/Quote Errors
            if "print(" in clean and not (re.search(r"['\"].*['\"]", clean) or "+" in clean or "," in clean):
                f_errs.append("Missing string quotes")
                inner = clean.split('(', 1)[1].rsplit(')', 1)[0]
                f_line = f_line.replace(inner, f"'{inner}'")

            # 3. LOGIC: Assignment instead of Equality
            if (clean.startswith("if ") or clean.startswith("elif ")) and "=" in clean and "==" not in clean and "!=" not in clean and ">=" not in clean and "<=" not in clean:
                f_errs.append("Logic: Using '=' instead of '=='")
                f_line = f_line.replace("=", "==")

            # 4. NAMING: Deep Typo Detection
            # Scans every word to see if it's a "close match" to a defined variable
            tokens = re.findall(r'\b\w+\b', clean)
            for token in tokens:
                if token.isdigit() or token in defined_vars or len(token) < 3:
                    continue
                # Fuzzy match for 1-character typos
                for d in defined_vars:
                    if d and token != d and (token in d or d in token) and abs(len(token)-len(d)) <= 1:
                        f_errs.append(f"Naming: Typo found ('{token}' -> '{d}')")
                        f_line = f_line.replace(token, d)

            if f_errs:
                st.session_state.detected_bugs.append({
                    "line": i+1, 
                    "msg": " & ".join(f_errs), 
                    "fix": f_line
                })
            corrected_lines.append(indent + f_line)

        st.session_state.fixed_code = "\n".join(corrected_lines)
        st.rerun()

if col2.button("🗑️ Clear All"):
    st.session_state.main_code = ""
    st.session_state.fixed_code = ""
    st.session_state.detected_bugs = []
    st.rerun()

# --- RENDER RESTORED FEATURES ---

# 1. Enterprise Analysis Cards
for bug in st.session_state.detected_bugs:
    st.markdown(f"""
    <div class="error-card">
        <div class="card-header">⚠️ Bug Detected at Line {bug['line']}</div>
        <div class="explanation"><b>Explanation:</b> Python syntax and logic rules must be followed. This fix ensures the interpreter can correctly execute your instructions.</div>
        <div class="fix-box">💡 Suggested fix: {bug['fix']}</div>
    </div>
    """, unsafe_allow_html=True)

# 2. Corrected Application Block
if st.session_state.fixed_code:
    st.subheader("💻 Corrected Application Block")
    st.code(st.session_state.fixed_code, language="python")
