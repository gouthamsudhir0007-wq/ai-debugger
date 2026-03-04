import streamlit as st
import re

# 1. Page Configuration - FORCING SIDEBAR TO BE VISIBLE
st.set_page_config(
    page_title="Enterprise Python Logic Debugger",
    layout="wide",
    initial_sidebar_state="expanded" 
)

# 2. CSS - Matching your Image 1 Styles exactly
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    
    /* Ensure Sidebar stays dark and visible */
    [data-testid="stSidebar"] { 
        background-color: #000000 !important; 
        min-width: 250px !important;
    }

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
    }
    </style>
    """, unsafe_allow_html=True)

# 3. State Management
if "history" not in st.session_state: st.session_state.history = []
if "editor_text" not in st.session_state: st.session_state.editor_text = ""
if "fixed_block" not in st.session_state: st.session_state.fixed_block = ""
if "bug_list" not in st.session_state: st.session_state.bug_list = []

# --- SIDEBAR: FORCED ELEMENTS ---
with st.sidebar:
    st.markdown("<h2 style='color:#00d4ff;'>📂 Code History</h2>", unsafe_allow_html=True)
    if st.button("🗑️ Wipe All History"):
        st.session_state.history = []
        st.rerun()
    st.markdown("---")
    # Display saved versions
    for i, code in enumerate(reversed(st.session_state.history)):
        if st.button(f"📄 Version {len(st.session_state.history)-i}", key=f"v_{i}"):
            st.session_state.editor_text = code
            st.rerun()

# --- MAIN UI ---
st.title("🤖 Enterprise Python Logic & Syntax Debugger")

# Link the terminal directly to the state
code_input = st.text_area("Input Terminal:", height=350, value=st.session_state.editor_text, key="main_editor")

# Button Layout
c1, c2, c3 = st.columns([1, 1, 1])

if c1.button("🚀 Analyze & Deep Fix"):
    if not code_input:
        st.warning("Please enter code first.")
    else:
        st.session_state.editor_text = code_input
        lines = code_input.split('\n')
        final_lines = []
        st.session_state.bug_list = []
        
        for i, line in enumerate(lines):
            indent = line[:len(line) - len(line.lstrip())]
            clean = line.strip()
            if not clean:
                final_lines.append(""); continue
            
            t_fix, t_errs = clean, []

            # 1. Block/Colon Mistakes
            if any(clean.startswith(x) for x in ["def ","if ","for ","while ","elif ","else"]) and not clean.endswith(":"):
                t_errs.append("Missing colon (:)")
                t_fix = t_fix.rstrip() + ":"

            # 2. String/Quote Mistakes
            if "print(" in clean and not (re.search(r"['\"].*['\"]", clean) or "+" in clean or "," in clean):
                t_errs.append("Missing string quotes")
                inner = clean.split('(', 1)[1].rsplit(')', 1)[0]
                t_fix = f"print('{inner}')"

            # 3. Logic: Assignment vs Equality Mistakes
            if (clean.startswith("if ") or clean.startswith("elif ")) and "=" in clean and "==" not in clean:
                t_errs.append("Logic Error: '=' used instead of '=='")
                t_fix = t_fix.replace("=", "==")

            if t_errs:
                st.session_state.bug_list.append({"ln": i+1, "msg": " & ".join(t_errs), "fix": t_fix})
            final_lines.append(indent + t_fix)

        st.session_state.fixed_block = "\n".join(final_lines)
        if code_input not in st.session_state.history:
            st.session_state.history.append(code_input)
        st.rerun()

# --- NEW INDIVIDUAL CLEAR BUTTONS ---
if c2.button("🧹 Clear Input Only"):
    st.session_state.editor_text = ""
    st.rerun()

if c3.button("🗑️ Clear All (Reset)"):
    st.session_state.editor_text = ""
    st.session_state.fixed_block = ""
    st.session_state.bug_list = []
    st.rerun()

# --- RENDER ANALYSIS CARDS ---
for bug in st.session_state.bug_list:
    st.markdown(f"""
    <div class="error-card">
        <div class="card-header">⚠️ Bug Detected at Line {bug['ln']}</div>
        <div class="explanation">Explanation: Python requires strict syntax and logic rules. This correction ensures your program follows standard PEP 8 guidelines.</div>
        <div class="fix-box">💡 Suggested fix: {bug['fix']}</div>
    </div>
    """, unsafe_allow_html=True)

if st.session_state.fixed_block:
    st.subheader("💻 Corrected Application Block (Copy Below)")
    st.code(st.session_state.fixed_block, language="python")
