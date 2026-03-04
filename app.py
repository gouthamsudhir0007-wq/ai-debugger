import streamlit as st
import re

# 1. Page Configuration
st.set_page_config(page_title="Enterprise Logic Debugger", layout="wide", initial_sidebar_state="expanded")

# 2. CSS - ENTERPRISE DARK THEME
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    [data-testid="stSidebar"] { background-color: #000000 !important; min-width: 300px !important; }
    
    /* Terminal Styling */
    .stTextArea div[data-baseweb="textarea"] + div { display: none !important; }
    .stTextArea>div>div>textarea {
        background-color: #0b0b0b !important; 
        color: #00ffcc !important; 
        border: 1px solid #333333 !important;
        border-radius: 12px;
        font-family: 'Fira Code', monospace;
    }

    /* Enterprise Result Cards */
    .error-card {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 15px;
    }
    .card-header { color: #ffa657; font-weight: 800; font-size: 1.1em; }
    .explanation { color: #8b949e; font-size: 0.9em; margin-bottom: 10px; }
    
    .fix-box {
        background-color: #0d1117;
        border: 1px solid #238636;
        border-left: 6px solid #238636;
        padding: 12px;
        border-radius: 8px;
        color: #3fb950;
        font-family: 'Fira Code', monospace;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. State Management
if "history" not in st.session_state: st.session_state.history = []
if "editor_val" not in st.session_state: st.session_state.editor_val = ""
if "fixed_code" not in st.session_state: st.session_state.fixed_code = ""
if "bugs" not in st.session_state: st.session_state.bugs = []

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 style='color:#00d4ff;'>📂 Versions</h2>", unsafe_allow_html=True)
    if st.button("🗑️ Wipe History"):
        st.session_state.history = []
        st.rerun()
    for i, code in enumerate(reversed(st.session_state.history)):
        if st.button(f"📄 Entry {len(st.session_state.history)-i}", key=f"h_{i}"):
            st.session_state.editor_val = code
            st.rerun()

# --- MAIN UI ---
st.title("🤖 Enterprise Python Logic & Syntax Debugger")

# Linked Input Area
code_input = st.text_area("Input Terminal:", height=350, value=st.session_state.editor_val, key="main_editor")

# Button Row
c1, c2, c3 = st.columns([1, 1, 1])

if c1.button("🚀 Analyze & Deep Fix"):
    if not code_input:
        st.warning("Input is empty.")
    else:
        st.session_state.editor_val = code_input
        lines = code_input.split('\n')
        final_lines = []
        st.session_state.bugs = []
        
        # Track defined variables for typo detection
        defined_vars = set(re.findall(r'\b(\w+)\s*=', code_input))
        
        for i, line in enumerate(lines):
            indent = line[:len(line) - len(line.lstrip())]
            clean = line.strip()
            if not clean:
                final_lines.append(""); continue
            
            t_fix, t_errs = clean, []

            # 1. Colon Check
            if any(clean.startswith(x) for x in ["def ","if ","for ","while ","elif ","else"]) and not clean.endswith(":"):
                t_errs.append("Missing colon (:)")
                t_fix = t_fix.rstrip() + ":"

            # 2. String/Print Check
            if "print(" in clean and not (re.search(r"['\"].*['\"]", clean) or "+" in clean or "," in clean):
                t_errs.append("Missing quotes")
                inner = clean.split('(', 1)[1].rsplit(')', 1)[0]
                t_fix = f"print('{inner}')"

            # 3. Logic: Assignment vs Equality
            if (clean.startswith("if ") or clean.startswith("elif ")) and "=" in clean and "==" not in clean:
                t_errs.append("Logic Error: '=' used for comparison")
                t_fix = t_fix.replace("=", "==")

            if t_errs:
                st.session_state.bugs.append({"ln": i+1, "msg": " & ".join(t_errs), "fix": t_fix})
            final_lines.append(indent + t_fix)

        st.session_state.fixed_code = "\n".join(final_lines)
        if code_input not in st.session_state.history:
            st.session_state.history.append(code_input)
        st.rerun()

# --- THE NEW CLEAR BUTTONS ---
if c2.button("🧹 Clear Input Only"):
    st.session_state.editor_val = ""
    st.rerun()

if c3.button("🗑️ Clear All (Reset)"):
    st.session_state.editor_val = ""
    st.session_state.fixed_code = ""
    st.session_state.bugs = []
    st.rerun()

# --- RENDER RESULTS ---
for bug in st.session_state.bugs:
    st.markdown(f"""
    <div class="error-card">
        <div class="card-header">⚠️ Bug Detected at Line {bug['ln']}</div>
        <div class="explanation">Explanation: Python logic and syntax rules must be followed. This fix ensures the interpreter executes your code correctly.</div>
        <div class="fix-box">💡 Suggested fix: {bug['fix']}</div>
    </div>
    """, unsafe_allow_html=True)

if st.session_state.fixed_code:
    st.subheader("💻 Corrected Application Block")
    st.code(st.session_state.fixed_code, language="python")
