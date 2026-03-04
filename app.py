import streamlit as st
import re

# 1. Page Configuration
st.set_page_config(page_title="Enterprise Python Logic Debugger", layout="wide")

# 2. CSS - EXACT MATCH FOR YOUR IMAGES (Orange Headers & Green Fix Boxes)
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    
    /* Terminal Styling - Teal Focus, No Red */
    .stTextArea div[data-baseweb="textarea"] { border: 1px solid #333333 !important; }
    .stTextArea div[data-baseweb="textarea"]:focus-within { border: 1px solid #00d4ff !important; }
    .stTextArea textarea { 
        background-color: #0b0b0b !important; 
        color: #00ffcc !important; 
        font-family: 'Fira Code', monospace; 
    }

    /* RESTORED: THE IMAGE 2 STYLE CARDS */
    .analysis-card {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
    }
    
    /* The Orange Header */
    .card-header { 
        color: #ffa657; 
        font-weight: 800; 
        font-size: 1.15em; 
        margin-bottom: 8px; 
    }
    
    /* The Grey Explanation */
    .explanation-text { 
        color: #8b949e; 
        font-size: 0.95em; 
        margin-bottom: 12px; 
        line-height: 1.4; 
    }
    
    /* The Green Fix Box */
    .suggested-fix-box {
        background-color: #0d1117;
        border: 1px solid #238636;
        border-left: 8px solid #238636; 
        padding: 12px;
        border-radius: 6px;
        color: #3fb950;
        font-family: 'Fira Code', monospace;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Persistent State Management
if "input_text" not in st.session_state: st.session_state.input_text = ""
if "fixed_text" not in st.session_state: st.session_state.fixed_text = ""
if "bugs_found" not in st.session_state: st.session_state.bugs_found = []

# --- MAIN UI ---
st.title("🤖 Enterprise Python Logic & Syntax Debugger")

# Linked Input Area
user_code = st.text_area("Input Terminal:", height=350, value=st.session_state.input_text, key="terminal_v6")

c1, c2 = st.columns([1, 5])

# 🚀 RESTORED FEATURE: ANALYZE & DEEP FIX
if c1.button("🚀 Analyze & Deep Fix"):
    if not user_code:
        st.warning("Please enter code first.")
    else:
        st.session_state.input_text = user_code
        lines = user_code.split('\n')
        corrected_list = []
        st.session_state.bugs_found = []
        
        # Deep Variable Mapping for Typos (Handles 'scorre' vs 'score')
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
                corrected_list.append(line); continue
            
            f_line, f_errs = clean, []

            # Syntax: Colon Check
            if any(clean.startswith(x) for x in ["def ","if ","for ","while ","elif ","else"]) and not clean.endswith(":"):
                f_errs.append("Missing colon (:)")
                f_line = f_line.rstrip() + ":"

            # Logic: Assignment Error (= vs ==)
            if (clean.startswith("if ") or clean.startswith("elif ")) and "=" in clean and "==" not in clean and not any(op in clean for op in [">=", "<=", "!="]):
                f_errs.append("Logic Error: '=' used instead of '=='")
                f_line = f_line.replace("=", "==")

            # Naming: Typo Detection
            tokens = re.findall(r'\b\w+\b', clean)
            for t in tokens:
                if t.isdigit() or t in defined or len(t) < 3: continue
                for d in defined:
                    if d and t != d and (t in d or d in t) and abs(len(t)-len(d)) <= 1:
                        f_errs.append(f"Typo detected: '{t}' likely should be '{d}'")
                        f_line = f_line.replace(t, d)

            if f_errs:
                st.session_state.bugs_found.append({"line": i+1, "msg": " & ".join(f_errs), "fix": f_line})
            corrected_list.append(indent + f_line)

        st.session_state.fixed_text = "\n".join(corrected_list)
        st.rerun()

if c2.button("🗑️ Clear All"):
    st.session_state.input_text = ""
    st.session_state.fixed_text = ""
    st.session_state.bugs_found = []
    st.rerun()

# --- 4. RENDER ANALYSIS CARDS (FEATURE FROM IMAGE 2) ---
for bug in st.session_state.bugs_found:
    st.markdown(f"""
    <div class="analysis-card">
        <div class="card-header">⚠️ Bug Detected at Line {bug['line']}</div>
        <div class="explanation-text">
            <b>Explanation:</b> {bug['msg']}. Python syntax and logic rules must be followed for the interpreter to execute code correctly.
        </div>
        <div class="suggested-fix-box">
            💡 <b>Suggested fix:</b> {bug['fix']}
        </div>
    </div>
    """, unsafe_allow_html=True)

# 5. Corrected Application Block
if st.session_state.fixed_text:
    st.subheader("💻 Corrected Application Block")
    st.code(st.session_state.fixed_text, language="python")
