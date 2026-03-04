import streamlit as st
import re

# 1. Page Configuration
st.set_page_config(page_title="Enterprise Python Logic Debugger", layout="wide")

# 2. CSS - EXACT MATCH FOR IMAGE 2 (Orange Headers & Green Fix Boxes)
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    
    /* Terminal - Teal Focus */
    .stTextArea div[data-baseweb="textarea"] { border: 1px solid #333333 !important; }
    .stTextArea div[data-baseweb="textarea"]:focus-within { border: 1px solid #00d4ff !important; }
    .stTextArea textarea { 
        background-color: #0b0b0b !important; 
        color: #00ffcc !important; 
        font-family: 'Fira Code', monospace; 
    }

    /* RESTORED FEATURE: IMAGE 2 STYLE CARDS */
    .analysis-card {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
    }
    /* Orange Title */
    .card-header { 
        color: #ffa657; 
        font-weight: 800; 
        font-size: 1.15em; 
        margin-bottom: 8px; 
    }
    /* Grey Explanation */
    .explanation-text { 
        color: #8b949e; 
        font-size: 0.95em; 
        margin-bottom: 12px; 
        line-height: 1.4; 
    }
    /* Green Fix Box */
    .suggested-fix-box {
        background-color: #0d1117;
        border: 1px solid #238636;
        border-left: 8px solid #238636; 
        padding: 12px;
        border-radius: 6px;
        color: #3fb950;
        font-family: 'Fira Code', monospace;
        display: flex;
        align-items: center;
    }
    .bulb-icon { margin-right: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 3. Persistent State
if "input_val" not in st.session_state: st.session_state.input_val = ""
if "fixed_val" not in st.session_state: st.session_state.fixed_val = ""
if "bug_data" not in st.session_state: st.session_state.bug_data = []

# --- MAIN UI ---
st.title("🤖 Enterprise Python Logic & Syntax Debugger")

# Linked Input
user_code = st.text_area("Input Terminal:", height=350, value=st.session_state.input_val, key="editor_final")

c1, c2 = st.columns([1, 5])

# 🚀 THE FEATURE: ANALYZE & DEEP FIX
if c1.button("🚀 Analyze & Deep Fix"):
    if not user_code:
        st.warning("Please enter code.")
    else:
        st.session_state.input_val = user_code
        lines = user_code.split('\n')
        corrected = []
        st.session_state.bug_data = []
        
        # Variable Mapping for Typos
        defined = set(re.findall(r'\b(\w+)\b\s*=', user_code))
        defined.update(re.findall(r'def\s+(\w+)', user_code))
        args = re.findall(r'def\s+\w+\((.*?)\)', user_code)
        for g in args:
            for a in g.split(','): defined.add(a.strip())
        defined.update(["print", "int", "input", "range", "len", "str", "float", "if", "elif", "else"])

        for i, line in enumerate(lines):
            indent = line[:len(line) - len(line.lstrip())]
            clean = line.strip()
            if not clean or clean.startswith("#"):
                corrected.append(line); continue
            
            f_line, f_errs = clean, []

            # Colon Check
            if any(clean.startswith(x) for x in ["def ","if ","for ","while ","elif ","else"]) and not clean.endswith(":"):
                f_errs.append("Missing colon (:)")
                f_line = f_line.rstrip() + ":"

            # Logic Check (= vs ==)
            if (clean.startswith("if ") or clean.startswith("elif ")) and "=" in clean and "==" not in clean and not any(op in clean for op in [">=", "<=", "!="]):
                f_errs.append("Logic Error: '=' used instead of '=='")
                f_line = f_line.replace("=", "==")

            # Typo Check
            tokens = re.findall(r'\b\w+\b', clean)
            for t in tokens:
                if t.isdigit() or t in defined or len(t) < 3: continue
                for d in defined:
                    if d and t != d and (t in d or d in token if 'token' in locals() else d in t) and abs(len(t)-len(d)) <= 1:
                        f_errs.append(f"Typo: '{t}' likely '{d}'")
                        f_line = f_line.replace(t, d)

            if f_errs:
                st.session_state.bug_data.append({"line": i+1, "msg": " & ".join(f_errs), "fix": f_line})
            corrected.append(indent + f_line)

        st.session_state.fixed_val = "\n".join(corrected)
        st.rerun()

if c2.button("🗑️ Clear All"):
    st.session_state.input_val = ""
    st.session_state.fixed_val = ""
    st.session_state.bug_data = []
    st.rerun()

# --- RENDER THE FEATURE FROM IMAGE 2 ---
for bug in st.session_state.bug_data:
    st.markdown(f"""
    <div class="analysis-card">
        <div class="card-header">⚠️ Bug Detected at Line {bug['line']}</div>
        <div class="explanation-text">
            <b>Explanation:</b> {bug['msg']}. Python syntax and logic rules must be followed for the interpreter to execute code correctly.
        </div>
        <div class="suggested-fix-box">
            <span class="bulb-icon">💡</span>
            <span><b>Suggested fix:</b> {bug['fix']}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Corrected Block
if st.session_state.fixed_val:
    st.subheader("💻 Corrected Application Block")
    st.code(st.session_state.fixed_val, language="python")
