import streamlit as st
import re

# 1. Page Configuration
st.set_page_config(page_title="Enterprise Python Logic Debugger", layout="wide")

# 2. CSS - ENTERPRISE STYLING (Restoring the Analysis Card UI)
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

    /* RESTORED: Enterprise Analysis Cards (Image 1 Style) */
    .error-card {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 10px;
        padding: 24px;
        margin-bottom: 20px;
    }
    .card-header { 
        color: #ffa657; 
        font-weight: 800; 
        font-size: 1.2em; 
        margin-bottom: 10px; 
        display: flex; 
        align-items: center; 
    }
    .explanation { 
        color: #8b949e; 
        font-size: 0.95em; 
        margin-bottom: 15px; 
        line-height: 1.5; 
    }
    
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
if "input_code" not in st.session_state: st.session_state.input_code = ""
if "fixed_code" not in st.session_state: st.session_state.fixed_code = ""
if "analysis_results" not in st.session_state: st.session_state.analysis_results = []

# --- MAIN INTERFACE ---
st.title("🤖 Enterprise Python Logic & Syntax Debugger")

# Link input area to state
user_code = st.text_area("Input Terminal:", height=350, value=st.session_state.input_code, key="primary_editor")

col1, col2 = st.columns([1, 5])

# 🚀 RESTORED FEATURE: ANALYZE & DEEP FIX
if col1.button("🚀 Analyze & Deep Fix"):
    if not user_code:
        st.warning("Please enter code to analyze.")
    else:
        st.session_state.input_code = user_code
        lines = user_code.split('\n')
        corrected_output = []
        st.session_state.analysis_results = []
        
        # VARIABLE MAPPING (To detect NameErrors/Typos)
        defined_vars = set(re.findall(r'\b(\w+)\b\s*=', user_code))
        defined_vars.update(re.findall(r'def\s+(\w+)', user_code))
        args = re.findall(r'def\s+\w+\((.*?)\)', user_code)
        for group in args:
            for a in group.split(','):
                defined_vars.add(a.strip())
        defined_vars.update(["print", "int", "input", "range", "len", "str", "float", "if", "elif", "else"])

        for i, line in enumerate(lines):
            indent = line[:len(line) - len(line.lstrip())]
            clean = line.strip()
            if not clean or clean.startswith("#"):
                corrected_output.append(line); continue
            
            f_line, current_errors = clean, []

            # 1. Syntax: Colons
            if any(clean.startswith(x) for x in ["def ","if ","for ","while ","elif ","else"]) and not clean.endswith(":"):
                current_errors.append("Missing colon (:)")
                f_line = f_line.rstrip() + ":"

            # 2. Syntax: Missing Quotes in Print
            if "print(" in clean and not (re.search(r"['\"].*['\"]", clean) or "+" in clean or "," in clean):
                current_errors.append("Missing string quotes")
                inner = clean.split('(', 1)[1].rsplit(')', 1)[0]
                f_line = f_line.replace(inner, f"'{inner}'")

            # 3. Logic: Assignment vs Equality
            if (clean.startswith("if ") or clean.startswith("elif ")) and "=" in clean and "==" not in clean and not any(op in clean for op in [">=", "<=", "!="]):
                current_errors.append("Logic Error: Using '=' (assignment) instead of '==' (comparison)")
                f_line = f_line.replace("=", "==")

            # 4. Naming: Deep Typo Detection
            tokens = re.findall(r'\b\w+\b', clean)
            for token in tokens:
                if token.isdigit() or token in defined_vars or len(token) < 3:
                    continue
                for d in defined_vars:
                    if d and token != d and (token in d or d in token) and abs(len(token)-len(d)) <= 1:
                        current_errors.append(f"Naming Error: Possible typo detected ('{token}' -> '{d}')")
                        f_line = f_line.replace(token, d)

            if current_errors:
                st.session_state.analysis_results.append({
                    "line": i+1,
                    "title": f"Bug Detected at Line {i+1}",
                    "msg": " & ".join(current_errors),
                    "fix": f_line
                })
            corrected_output.append(indent + f_line)

        st.session_state.fixed_code = "\n".join(corrected_output)
        st.rerun()

if col2.button("🗑️ Clear All"):
    st.session_state.input_code = ""
    st.session_state.fixed_code = ""
    st.session_state.analysis_results = []
    st.rerun()

# --- RENDER ANALYSIS CARDS ---
for bug in st.session_state.analysis_results:
    st.markdown(f"""
    <div class="error-card">
        <div class="card-header">⚠️ {bug['title']}</div>
        <div class="explanation"><b>Explanation:</b> {bug['msg']}. Python syntax and logic rules must be followed for the interpreter to execute code. This error prevents code from running or causes incorrect results.</div>
        <div class="fix-box">💡 Suggested fix: {bug['fix']}</div>
    </div>
    """, unsafe_allow_html=True)

# --- RENDER CORRECTED BLOCK ---
if st.session_state.fixed_code:
    st.subheader("💻 Corrected Application Block")
    st.code(st.session_state.fixed_code, language="python")
