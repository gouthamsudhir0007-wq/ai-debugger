import streamlit as st
import re

# 1. Page Configuration
st.set_page_config(page_title="Enterprise Python Logic Debugger", layout="wide")

# 2. CSS - EXACT MATCH FOR IMAGE 2 & 8 (Orange Headers & Green Fix Boxes)
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    
    /* Terminal Styling */
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
    .card-header { 
        color: #ffa657; 
        font-weight: 800; 
        font-size: 1.15em; 
        margin-bottom: 8px; 
    }
    .explanation-text { 
        color: #8b949e; 
        font-size: 0.95em; 
        margin-bottom: 12px; 
        line-height: 1.4; 
    }
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

# 3. State Management
if "input" not in st.session_state: st.session_state.input = ""
if "fixed" not in st.session_state: st.session_state.fixed = ""
if "bugs" not in st.session_state: st.session_state.bugs = []

# --- MAIN UI ---
st.title("🤖 Enterprise Python Logic & Syntax Debugger")

user_code = st.text_area("Input Terminal:", height=350, value=st.session_state.input, key="v_final")

col1, col2 = st.columns([1, 5])

# 🚀 THE UPGRADED DEEP FIX FEATURE
if col1.button("🚀 Analyze & Deep Fix"):
    if not user_code:
        st.warning("Please enter code.")
    else:
        st.session_state.input = user_code
        lines = user_code.split('\n')
        corrected_list = []
        st.session_state.bugs = []
        
        # --- STEP 1: DEEP VARIABLE MAPPING ---
        # This maps all real variables so we can find the "fakes" (typos)
        defined_vars = set(re.findall(r'\b(\w+)\b\s*=', user_code))
        defined_vars.update(re.findall(r'def\s+(\w+)', user_code))
        # Capture function parameters
        params = re.findall(r'def\s+\w+\((.*?)\)', user_code)
        for p_group in params:
            for p in p_group.split(','):
                defined_vars.add(p.strip())
        # Add Python keywords and built-ins to ignore list
        defined_vars.update(["print", "int", "input", "range", "len", "str", "float", "if", "elif", "else", "return", "name", "score", "age"])

        # --- STEP 2: LINE-BY-LINE LOGIC ANALYSIS ---
        for i, line in enumerate(lines):
            indent = line[:len(line) - len(line.lstrip())]
            clean = line.strip()
            if not clean or clean.startswith("#"):
                corrected_list.append(line); continue
            
            f_line, f_errs = clean, []

            # 1. Logic Check: Equality vs Assignment
            if (clean.startswith("if ") or clean.startswith("elif ")) and "=" in clean and "==" not in clean and not any(op in clean for op in [">=", "<=", "!="]):
                f_errs.append("Logic Error: Using '=' (assignment) instead of '==' (comparison)")
                f_line = f_line.replace("=", "==")

            # 2. Syntax Check: Missing Colons
            if any(clean.startswith(x) for x in ["def ","if ","for ","while ","elif ","else"]) and not clean.endswith(":"):
                f_errs.append("Syntax Error: Missing colon (:)")
                f_line = f_line.rstrip() + ":"

            # 3. Naming Check: Deep Typo Detection
            # Compares words against our 'defined_vars' map
            words = re.findall(r'\b\w+\b', clean)
            for w in words:
                if w.isdigit() or w in defined_vars or len(w) < 3:
                    continue
                # If a word is 90% similar to a defined variable, it's a bug
                for d in defined_vars:
                    if d and w != d and (w in d or d in w) and abs(len(w)-len(d)) <= 1:
                        f_errs.append(f"Naming Error: '{w}' is undefined; did you mean '{d}'?")
                        f_line = f_line.replace(w, d)

            if f_errs:
                st.session_state.bugs.append({"line": i+1, "msg": " & ".join(f_errs), "fix": f_line})
            corrected_list.append(indent + f_line)

        st.session_state.fixed = "\n".join(corrected_list)
        st.rerun()

if col2.button("🗑️ Clear All"):
    st.session_state.input = ""
    st.session_state.fixed = ""
    st.session_state.bugs = []
    st.rerun()

# --- 4. RENDER ANALYSIS CARDS (IMAGE 2 & 8 STYLE) ---
for bug in st.session_state.bugs:
    st.markdown(f"""
    <div class="analysis-card">
        <div class="card-header">⚠️ Bug Detected at Line {bug['line']}</div>
        <div class="explanation-text">
            <b>Explanation:</b> {bug['msg']}. Python syntax and logic rules must be followed for the interpreter to execute code. 
            This error prevents code from running or causes incorrect results.
        </div>
        <div class="suggested-fix-box">
            💡 <b>Suggested fix:</b> {bug['fix']}
        </div>
    </div>
    """, unsafe_allow_html=True)

# 5. Corrected Application Block
if st.session_state.fixed:
    st.subheader("💻 Corrected Application Block")
    st.code(st.session_state.fixed, language="python")
