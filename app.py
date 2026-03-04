import streamlit as st
import time
import sys
from io import StringIO

# 1. Page Configuration
st.set_page_config(page_title="Python AI Pro", layout="wide", initial_sidebar_state="expanded")

# 2. CSS - FIXED SIDEBAR / TEAL FOCUS / HIDE HINTS
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    
    /* Ensure Sidebar Arrow is Visible and Teal */
    [data-testid="stSidebarNav"] { background-color: #000000 !important; }
    .st-emotion-cache-6qob1r { color: #00d4ff !important; } 

    /* Terminal Styling */
    .stTextArea div[data-baseweb="textarea"] + div { display: none !important; }
    .stTextArea>div>div>textarea {
        background-color: #111111 !important; 
        color: #FFFFFF !important; 
        border: 1px solid #333333 !important;
        border-radius: 10px;
    }
    .stTextArea>div>div>textarea:focus {
        border-color: #00d4ff !important;
        box-shadow: 0 0 0 1px #00d4ff !important;
    }

    /* Enterprise Result Cards */
    .error-card {
        background-color: #1E1E1E;
        border: 1px solid #444444;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
    }
    .card-header { color: #FFA500; font-weight: bold; }
    .fix-box {
        background-color: #142E1F;
        border-left: 5px solid #2ECC71;
        padding: 12px;
        border-radius: 6px;
        color: #D1FFD6;
    }
    .console-box {
        background-color: #000000;
        border: 1px solid #00d4ff;
        color: #00ff00;
        padding: 15px;
        font-family: monospace;
        border-radius: 8px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Persistent State Management
if "history" not in st.session_state: st.session_state.history = []
if "last_fixed" not in st.session_state: st.session_state.last_fixed = ""
if "editor_content" not in st.session_state: st.session_state.editor_content = ""

# --- SIDEBAR HISTORY ---
with st.sidebar:
    st.markdown("<h2 style='color:#00d4ff;'>📂 Code History</h2>", unsafe_allow_html=True)
    if st.button("🗑️ Clear All History"):
        st.session_state.history = []
        st.rerun()
    st.markdown("---")
    for i, entry in enumerate(reversed(st.session_state.history)):
        if st.button(f"Sess {len(st.session_state.history)-i}: {entry[:15]}...", key=f"hist_{i}"):
            st.session_state.editor_content = entry
            st.rerun()

# --- MAIN UI ---
st.title("🤖 Python Enterprise Debugger & Runner")

# Input Terminal with State Link
code_input = st.text_area("Input Terminal:", height=300, value=st.session_state.editor_content, key="main_editor")

col1, col2, col3 = st.columns([1, 1, 4])

# 🚀 ANALYZE & FIX LOGIC
if col1.button("🚀 Analyze & Fix"):
    if not code_input:
        st.warning("Please enter code.")
    else:
        st.session_state.editor_content = code_input # Save state
        lines = code_input.split('\n')
        fixed_lines = []
        cards = []
        
        for i, line in enumerate(lines):
            indent = line[:len(line) - len(line.lstrip())]
            clean = line.strip()
            if not clean:
                fixed_lines.append("")
                continue
            
            errs, fix = [], clean
            if any(clean.startswith(x) for x in ["def ","if ","for ","while "]) and not clean.endswith(":"):
                errs.append("Missing colon (:)"); fix += ":"
            if "print(" in clean and not ('"' in clean or "'" in clean):
                errs.append("Missing quotes")
                content = clean.split('(', 1)[1].rsplit(')', 1)[0]
                fix = f"print('{content}')"
            
            if errs: cards.append({"ln": i+1, "m": " & ".join(errs), "f": fix})
            fixed_lines.append(indent + fix)
        
        st.session_state.last_fixed = "\n".join(fixed_lines)
        st.session_state.history.append(code_input)
        
        for c in cards:
            st.markdown(f'<div class="error-card"><div class="card-header">Line {c["ln"]}: {c["m"]}</div><div class="fix-box">💡 {c["f"]}</div></div>', unsafe_allow_html=True)
        st.code(st.session_state.last_fixed, language="python")

# ▶️ RUN WITH RUNTIME INPUT
if col2.button("▶️ Run Code"):
    if st.session_state.last_fixed:
        # Check if code requires input()
        if "input(" in st.session_state.last_fixed:
            user_val = st.text_input("Console Input Required:", placeholder="Enter value here and press Enter...")
            if not user_val: st.info("Waiting for input..."); st.stop()
            # Inject input value for execution
            exec_code = f"def input(prompt=''): return '{user_val}'\n" + st.session_state.last_fixed
        else:
            exec_code = st.session_state.last_fixed

        old_stdout = sys.stdout
        sys.stdout = output_capture = StringIO()
        try:
            exec(exec_code)
            sys.stdout = old_stdout
            st.markdown(f'<div class="console-box">{output_capture.getvalue() or "Finished."}</div>', unsafe_allow_html=True)
        except Exception as e:
            sys.stdout = old_stdout
            st.error(f"Error: {e}")

# 🗑️ CLEAR EVERYTHING
if col3.button("🗑️ Clear All"):
    st.session_state.editor_content = ""
    st.session_state.last_fixed = ""
    st.rerun()
