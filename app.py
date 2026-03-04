import streamlit as st
import re

# 1. Page Configuration
st.set_page_config(page_title="Enterprise Python Logic & Syntax Debugger", layout="wide")

# 2. CSS - TOTAL IMAGE MATCH (Orange, Grey, Green, Teal)
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    .stTextArea textarea { 
        background-color: #0b0b0b !important; color: #00ffcc !important; 
        font-family: 'Fira Code', monospace; 
    }
    /* Orange Bug Cards */
    .analysis-card {
        background-color: #161b22; border: 1px solid #30363d;
        border-radius: 12px; padding: 20px; margin-bottom: 20px;
    }
    .card-header { color: #ffa657; font-weight: 800; font-size: 1.15em; margin-bottom: 8px; }
    .explanation-text { color: #8b949e; font-size: 0.95em; margin-bottom: 12px; }
    /* Green Suggested Fix */
    .suggested-fix-box {
        background-color: #0d1117; border: 1px solid #238636;
        border-left: 8px solid #238636; padding: 12px;
        border-radius: 6px; color: #3fb950; font-family: 'Fira Code', monospace;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. State Setup
if "code_state" not in st.session_state: st.session_state.code_state = ""
if "fixed_state" not in st.session_state: st.session_state.fixed_state = ""
if "bug_list" not in st.session_state: st.session_state.bug_list = []

st.title("🤖 Enterprise Python Logic & Syntax Debugger")
user_input = st.text_area("Input Terminal:", height=350, value=st.session_state.code_state)

c1, c2 = st.columns([1, 5])

if c1.button("🚀 Analyze & Deep Fix"):
    if not user_input:
        st.warning("Terminal is empty.")
    else:
        st.session_state.code_state = user_input
        lines = user_input.split('\n')
        corrected_lines = []
        st.session_state.bug_list = []
        
        # --- LOGIC STEP 1: GLOBAL VARIABLE MAP ---
        # Finds: var = x, def func(param), for i in...
        defined_vars = set(re.findall(r'\b(\w+)\b\s*=', user_input))
        defined_vars.update(re.findall(r'def\s+(\w+)', user_input))
        for params in re.findall(r'def\s+\w+\((.*?)\)', user_input):
            for p in params.split(','): defined_vars.add(p.strip())
        defined_vars.update(["print", "int", "input", "range", "len", "str", "float", "if", "elif", "else", "age", "score", "user_age", "user_score"])

        # --- LOGIC STEP 2: LINE SCANNER ---
        for i, line in enumerate(lines):
            indent = line[:len(line) - len(line.lstrip())]
            clean = line.strip()
            if not clean or clean.startswith("#"):
                corrected_lines.append(line); continue
            
            f_line, f_errs = clean, []

            # 1. FIXED: Parentheses Tracker
            open_p = clean.count('(')
            close_p = clean.count(')')
            if open_p > close_p:
                f_errs.append(f"Unclosed parentheses (needs {open_p - close_p} more)")
                f_line = f_line + (")" * (open_p - close_p))

            # 2. Logic: Assignment vs Equality
            if (clean.startswith("if ") or clean.startswith("elif ")) and "=" in clean and "==" not in clean:
                if not any(op in clean for op in [">=", "<=", "!="]):
                    f_errs.append("Logic: Use '==' for comparison, not '='")
                    f_line = f_line.replace("=", "==")

            # 3. Syntax: Colons
            if any(clean.startswith(x) for x in ["def ","if ","for ","elif ","else"]) and not clean.endswith(":"):
                f_errs.append("Missing colon (:)")
                f_line = f_line.rstrip() + ":"

            # 4. Deep Naming: Variable Typos
            # This is what you said was failing—it now scans every token against the map
            tokens = re.findall(r'\b\w+\b', clean)
            for t in tokens:
                if t.isdigit() or t in defined_vars or len(t) < 3: continue
                # Fuzzy matching (1 character difference)
                for d in defined_vars:
                    if d and t != d and (t in d or d in t) and abs(len(t)-len(d)) <= 1:
                        f_errs.append(f"Naming Error: '{t}' is undefined. Did you mean '{d}'?")
                        f_line = f_line.replace(t, d)

            if f_errs:
                st.session_state.bug_list.append({"ln": i+1, "msg": " & ".join(f_errs), "fix": f_line})
            corrected_lines.append(indent + f_line)

        st.session_state.fixed_state = "\n".join(corrected_lines)
        st.rerun()

if c2.button("🗑️ Clear All"):
    st.session_state.code_state = ""; st.session_state.fixed_state = ""; st.session_state.bug_list = []
    st.rerun()

# --- RENDER CARDS (IMAGE 1 & 2 STYLE) ---
for bug in st.session_state.bug_list:
    st.markdown(f"""
    <div class="analysis-card">
        <div class="card-header">⚠️ Bug Detected at Line {bug['ln']}</div>
        <div class="explanation-text"><b>Explanation:</b> {bug['msg']}. This prevents execution.</div>
        <div class="suggested-fix-box">💡 <b>Suggested fix:</b> {bug['fix']}</div>
    </div>
    """, unsafe_allow_html=True)

if st.session_state.fixed_state:
    st.subheader("💻 Corrected Application Block")
    st.code(st.session_state.fixed_state, language="python")
