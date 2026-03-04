import streamlit as st
import re

# 1. Page Configuration
st.set_page_config(page_title="Enterprise Logic Debugger", layout="wide")

# 2. CSS - ENTERPRISE STYLING & ANALYSIS CARDS (Image 1 Style)
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    
    /* Input Terminal */
    .stTextArea div[data-baseweb="textarea"] { border: 1px solid #333333 !important; }
    .stTextArea div[data-baseweb="textarea"]:focus-within { border: 1px solid #00d4ff !important; }
    .stTextArea textarea { 
        background-color: #0b0b0b !important; 
        color: #00ffcc !important; 
        font-family: 'Fira Code', monospace; 
    }
    
    /* Hide the 'Press Ctrl+Enter' hint */
    .stTextArea div[data-baseweb="textarea"] + div { display: none !important; }

    /* --- RESTORED FEATURE: Analysis Cards --- */
    .error-card {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 20px;
    }
    /* Orange Color Stuffs */
    .card-header { 
        color: #ffa657; 
        font-weight: 800; 
        font-size: 1.25em; 
        margin-bottom: 10px; 
    }
    .explanation { 
        color: #8b949e; 
        font-size: 0.95em; 
        margin-bottom: 15px; 
        line-height: 1.5; 
    }
    /* The Green Box */
    .fix-box {
        background-color: #0d1117;
        border: 1px solid #238636;
        border-left: 8px solid #238636; /* Heavy green bar from image */
        padding: 15px;
        border-radius: 8px;
        color: #3fb950;
        font-family: 'Fira Code', monospace;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Session State Management
if "user_code" not in st.session_state: st.session_state.user_code = ""
if "fixed_code" not in st.session_state: st.session_state.fixed_code = ""
if "analysis_log" not in st.session_state: st.session_state.analysis_log = []

# --- MAIN UI ---
st.title("🤖 Enterprise Python Logic & Syntax Debugger")

# Linked Input
code_input = st.text_area("Input Terminal:", height=350, value=st.session_state.user_code, key="v_editor")

# Buttons
col1, col2 = st.columns([1, 4])

# 🚀 DEEP ANALYSIS LOGIC (RESTORED)
if col1.button("🚀 Analyze & Deep Fix"):
    if not code_input:
        st.warning("Input is empty.")
    else:
        st.session_state.user_code = code_input
        lines = code_input.split('\n')
        corrected_lines = []
        st.session_state.analysis_log = []
        
        # Track defined variables for typo detection
        defined_vars = set(re.findall(r'\b(\w+)\b\s*=', code_input))
        defined_vars.update(re.findall(r'def\s+(\w+)', code_input))
        
        # built-ins
        defined_vars.update(["print", "int", "input", "range", "len", "str", "float", "if", "elif", "else"])

        for i, line in enumerate(lines):
            indent = line[:len(line) - len(line.lstrip())]
            clean = line.strip()
            if not clean or clean.startswith("#"):
                corrected_lines.append(line); continue
            
            f_line, f_errs = clean, []

            # 1. SYNTAX: Colons
            if any(clean.startswith(x) for x in ["def ","if ","for ","while ","elif ","else"]) and not clean.endswith(":"):
                f_errs.append("Missing colon (:)")
                f_line = f_line.rstrip() + ":"

            # 2. LOGIC: Assignment vs Equality
            if (clean.startswith("if ") or clean.startswith("elif ")) and "=" in clean and "==" not in clean:
                f_errs.append("Logic: '=' used instead of '=='")
                f_line = f_line.replace("=", "==")

            # 3. NAMING: Deep Typo Detection
            tokens = re.findall(r'\b\w+\b', clean)
            for token in tokens:
                if token.isdigit() or token in defined_vars or len(token) < 3:
                    continue
                # Fuzzy match for typos
                for d in defined_vars:
                    if d and token != d and (token in d or d in token) and abs(len(token)-len(d)) <= 1:
                        f_errs.append(f"Naming: Typo found ('{token}' -> '{d}')")
                        f_line = f_line.replace(token, d)

            if f_errs:
                st.session_state.analysis_log.append({"ln": i+1, "msg": " & ".join(f_errs), "fix": f_line})
            corrected_lines.append(indent + f_line)

        st.session_state.fixed_code = "\n".join(corrected_lines)
        st.rerun()

if col2.button("🗑️ Clear All"):
    st.session_state.user_code = ""
    st.session_state.fixed_code = ""
    st.session_state.analysis_log = []
    st.rerun()

# --- RENDER RESTORED ANALYSIS CARDS ---
for bug in st.session_state.analysis_log:
    st.markdown(f"""
    <div class="error-card">
        <div class="card-header">⚠️ Bug Detected at Line {bug['ln']}</div>
        <div class="explanation">
            <b>Explanation:</b> {bug['msg']}. Python syntax and logic rules must be followed for the interpreter to execute code correctly. 
            This error prevents code from running or causes incorrect logical results.
        </div>
        <div class="fix-box">💡 Suggested fix: {bug['fix']}</div>
    </div>
    """, unsafe_allow_html=True)

# Render Corrected Block
if st.session_state.fixed_code:
    st.subheader("💻 Corrected Application Block")
    st.code(st.session_state.fixed_code, language="python")
