import streamlit as st
import re

# 1. Page Configuration
st.set_page_config(page_title="Enterprise Python Logic Debugger", layout="wide")

# 2. CSS - EXACT MATCH FOR IMAGE 1 (Cards, Colors, Borders)
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    
    /* Terminal - Teal Focus, No Red */
    .stTextArea div[data-baseweb="textarea"] { border: 1px solid #333333 !important; }
    .stTextArea div[data-baseweb="textarea"]:focus-within { border: 1px solid #00d4ff !important; }
    .stTextArea textarea { 
        background-color: #0b0b0b !important; 
        color: #00ffcc !important; 
        font-family: 'Fira Code', monospace; 
    }

    /* RESTORED: THE EXACT CARD FEATURE FROM IMAGE 1 */
    .analysis-card {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 25px;
        margin-bottom: 25px;
    }
    .card-header { 
        color: #ffa657; 
        font-weight: 800; 
        font-size: 1.25em; 
        margin-bottom: 12px; 
    }
    .explanation-text { 
        color: #8b949e; 
        font-size: 1.0em; 
        margin-bottom: 18px; 
        line-height: 1.6; 
    }
    .suggested-fix-container {
        background-color: #0d1117;
        border: 1px solid #238636;
        border-left: 8px solid #238636; /* Heavy green bar from image */
        padding: 15px;
        border-radius: 8px;
        color: #3fb950;
        font-family: 'Fira Code', monospace;
        display: flex;
        align-items: center;
    }
    .fix-icon { margin-right: 12px; font-size: 1.2em; }
    </style>
    """, unsafe_allow_html=True)

# 3. Persistent State Management
if "input_text" not in st.session_state: st.session_state.input_text = ""
if "fixed_text" not in st.session_state: st.session_state.fixed_text = ""
if "bug_report" not in st.session_state: st.session_state.bug_report = []

# --- MAIN UI ---
st.title("🤖 Enterprise Python Logic & Syntax Debugger")

# Linked Input Area
user_code = st.text_area("Input Terminal:", height=350, value=st.session_state.input_text, key="editor_v5")

c1, c2 = st.columns([1, 5])

# 🚀 THE "ONE JOB" FEATURE: DEEP ANALYSIS
if c1.button("🚀 Analyze & Deep Fix"):
    if not user_code:
        st.warning("Please enter code.")
    else:
        st.session_state.input_text = user_code
        lines = user_code.split('\n')
        corrected_list = []
        st.session_state.bug_report = []
        
        # 4. DEEP LOGIC SCANNER (Variables & Typos)
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

            # Check 1: Colons
            if any(clean.startswith(x) for x in ["def ","if ","for ","while ","elif ","else"]) and not clean.endswith(":"):
                f_errs.append("Missing colon (:)")
                f_line = f_line.rstrip() + ":"

            # Check 2: Strings
            if "print(" in clean and not (re.search(r"['\"].*['\"]", clean) or "+" in clean or "," in clean):
                f_errs.append("Missing string quotes")
                inner = clean.split('(', 1)[1].rsplit(')', 1)[0]
                f_line = f_line.replace(inner, f"'{inner}'")

            # Check 3: Logic Assignment Error
            if (clean.startswith("if ") or clean.startswith("elif ")) and "=" in clean and "==" not in clean and not any(op in clean for op in [">=", "<=", "!="]):
                f_errs.append("Logic Error: '=' used instead of '=='")
                f_line = f_line.replace("=", "==")

            # Check 4: Variable Typos
            tokens = re.findall(r'\b\w+\b', clean)
            for t in tokens:
                if t.isdigit() or t in defined or len(t) < 3: continue
                for d in defined:
                    if d and t != d and (t in d or d in t) and abs(len(t)-len(d)) <= 1:
                        f_errs.append(f"Typo detected: '{t}' likely should be '{d}'")
                        f_line = f_line.replace(t, d)

            if f_errs:
                st.session_state.bug_report.append({
                    "line": i+1,
                    "msg": " & ".join(f_errs),
                    "fix": f_line
                })
            corrected_list.append(indent + f_line)

        st.session_state.fixed_text = "\n".join(corrected_list)
        st.rerun()

if c2.button("🗑️ Clear All"):
    st.session_state.input_text = ""
    st.session_state.fixed_text = ""
    st.session_state.bug_report = []
    st.rerun()

# --- 5. RENDER THE RESTORED FEATURE ---
for bug in st.session_state.bug_report:
    st.markdown(f"""
    <div class="analysis-card">
        <div class="card-header">⚠️ Bug Detected at Line {bug['line']}</div>
        <div class="explanation-text">
            <b>Explanation:</b> {bug['msg']}. Python syntax and logic rules must be followed for the interpreter to execute code correctly. 
            This error prevents code from running or causes incorrect logical results.
        </div>
        <div class="suggested-fix-container">
            <span class="fix-icon">💡</span>
            <span><b>Suggested fix:</b> {bug['fix']}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Corrected Block
if st.session_state.fixed_text:
    st.subheader("💻 Corrected Application Block")
    st.code(st.session_state.fixed_text, language="python")
