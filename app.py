import streamlit as st
import re
import difflib

# 1. Page Configuration
st.set_page_config(page_title="Enterprise Python Logic Debugger", layout="wide")

# 2. CSS - NO RED / ENTERPRISE ORANGE & GREEN ONLY
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    
    /* Dark Terminal - No Red Borders */
    .stTextArea textarea { 
        background-color: #0b0b0b !important; color: #00ffcc !important; 
        border: 1px solid #333333 !important;
        font-family: 'Fira Code', monospace; 
    }
    .stTextArea textarea:focus { border-color: #00d4ff !important; }

    /* Orange Bug Cards from Image 1 & 2 */
    .analysis-card {
        background-color: #161b22; border: 1px solid #30363d;
        border-radius: 12px; padding: 22px; margin-bottom: 20px;
    }
    .card-header { color: #ffa657; font-weight: 800; font-size: 1.2em; margin-bottom: 8px; }
    .explanation-text { color: #8b949e; font-size: 0.95em; line-height: 1.5; margin-bottom: 12px; }
    
    /* Green Suggested Fix Box */
    .suggested-fix-box {
        background-color: #0d1117; border: 1px solid #238636;
        border-left: 8px solid #238636; padding: 15px;
        border-radius: 8px; color: #3fb950; font-family: 'Fira Code', monospace;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. State Setup
if "code" not in st.session_state: st.session_state.code = ""
if "fixed" not in st.session_state: st.session_state.fixed = ""
if "bugs" not in st.session_state: st.session_state.bugs = []

st.title("🤖 Master Logic & Spelling Debugger")
user_input = st.text_area("Input Terminal:", height=400, value=st.session_state.code)

col1, col2 = st.columns([1, 5])

if col1.button("🚀 Analyze & Fix All"):
    if not user_input:
        st.warning("Please enter code.")
    else:
        st.session_state.code = user_input
        lines = user_input.split('\n')
        corrected_lines = []
        st.session_state.bugs = []
        
        # --- PHASE 1: RECURSIVE VARIABLE MAPPING (The Spell-Check Brain) ---
        # We find every variable actually assigned or used in a 'def'
        valid_vars = set(re.findall(r'\b(\w+)\b\s*=', user_input))
        valid_vars.update(re.findall(r'def\s+(\w+)', user_input))
        for p in re.findall(r'def\s+\w+\((.*?)\)', user_input):
            for arg in p.split(','): valid_vars.add(arg.strip())
        # Python Essentials
        valid_vars.update(["print", "int", "input", "range", "len", "str", "float", "if", "elif", "else"])

        # --- PHASE 2: LINE-BY-LINE DEEP DEBUG ---
        for i, line in enumerate(lines):
            indent = line[:len(line) - len(line.lstrip())]
            clean = line.strip()
            if not clean or clean.startswith("#"):
                corrected_lines.append(line); continue
            
            f_line, f_errs = clean, []

            # 1. Spelling/Naming Error (Fuzzy Match)
            # This catches 'scorre' vs 'score' and 'usr_age' vs 'user_age'
            words = re.findall(r'\b\w+\b', clean)
            for w in words:
                if w.isdigit() or w in valid_vars or len(w) < 3: continue
                # Look for a 70% or higher similarity match in valid_vars
                matches = difflib.get_close_matches(w, list(valid_vars), n=1, cutoff=0.6)
                if matches:
                    suggestion = matches[0]
                    f_errs.append(f"Spelling Error: '{w}' is not defined. Did you mean '{suggestion}'?")
                    f_line = re.sub(r'\b' + w + r'\b', suggestion, f_line)

            # 2. Logic: Equality Error (= instead of ==)
            if (clean.startswith("if ") or clean.startswith("elif ")) and "=" in clean and "==" not in clean:
                if not any(op in clean for op in [">=", "<=", "!="]):
                    f_errs.append("Logic Error: Use '==' for checking values")
                    f_line = f_line.replace("=", "==")

            # 3. Syntax: Missing Colon
            if any(clean.startswith(x) for x in ["def ","if ","for ","elif ","else"]) and not clean.endswith(":"):
                f_errs.append("Syntax Error: Missing colon (:)")
                f_line = f_line.rstrip() + ":"

            # 4. Parentheses Tracker (Auto-Closing)
            open_p = f_line.count('(')
            close_p = f_line.count(')')
            if open_p > close_p:
                f_errs.append("Syntax Error: Unclosed parentheses")
                f_line += ")" * (open_p - close_p)

            # 5. Missing Quotes in Print
            if "print(" in f_line and not (re.search(r"['\"].*['\"]", f_line) or "," in f_line):
                f_errs.append("Syntax Error: Missing quotes for text")
                content = f_line.split('(', 1)[1].rsplit(')', 1)[0]
                f_line = f_line.replace(content, f"'{content}'")

            if f_errs:
                st.session_state.bugs.append({"ln": i+1, "msg": " & ".join(f_errs), "fix": f_line})
            corrected_lines.append(indent + f_line)

        st.session_state.fixed = "\n".join(corrected_lines)
        st.rerun()

if col2.button("🗑️ Clear All"):
    st.session_state.code = ""; st.session_state.fixed = ""; st.session_state.bugs = []
    st.rerun()

# --- RENDER ANALYSIS CARDS (EXACT MATCH TO YOUR IMAGES) ---
for bug in st.session_state.bugs:
    st.markdown(f"""
    <div class="analysis-card">
        <div class="card-header">⚠️ Bug Detected at Line {bug['ln']}</div>
        <div class="explanation-text"><b>Explanation:</b> {bug['msg']}. Python cannot process this line as written.</div>
        <div class="suggested-fix-box">💡 <b>Suggested fix:</b> {bug['fix']}</div>
    </div>
    """, unsafe_allow_html=True)

if st.session_state.fixed:
    st.subheader("💻 Corrected Application Block")
    st.code(st.session_state.fixed, language="python")
