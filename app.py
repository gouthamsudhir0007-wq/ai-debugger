import streamlit as st
import re
import difflib

# 1. Page Configuration
st.set_page_config(page_title="Teal Logic Debugger", layout="wide")

# 2. CSS - TEAL THEME & ENTERPRISE CARDS (No Red)
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    
    /* Teal Terminal Styling */
    .stTextArea textarea { 
        background-color: #0b0b0b !important; 
        color: #00ffcc !important; 
        border: 1px solid #008080 !important;
        font-family: 'Fira Code', monospace; 
    }
    .stTextArea textarea:focus { border-color: #00ffff !important; box-shadow: 0 0 10px #008080; }

    /* Analysis Cards */
    .analysis-card {
        background-color: #0d1a1a; 
        border: 1px solid #004d4d;
        border-radius: 12px; 
        padding: 22px; 
        margin-bottom: 20px;
    }
    /* Orange Header stays for visibility as per Image 1 */
    .card-header { color: #ffa657; font-weight: 800; font-size: 1.2em; margin-bottom: 8px; }
    .explanation-text { color: #a0baba; font-size: 0.95em; line-height: 1.5; margin-bottom: 12px; }
    
    /* Green Suggested Fix Box */
    .suggested-fix-box {
        background-color: #050f0f; 
        border: 1px solid #238636;
        border-left: 8px solid #238636; 
        padding: 15px;
        border-radius: 8px; 
        color: #3fb950; 
        font-family: 'Fira Code', monospace;
    }
    
    /* Teal Buttons */
    .stButton>button {
        background-color: #004d4d !important;
        color: #00ffcc !important;
        border: 1px solid #008080 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Logic Engine [Two-Pass Scanner]
if "code" not in st.session_state: st.session_state.code = ""
if "fixed" not in st.session_state: st.session_state.fixed = ""
if "bugs" not in st.session_state: st.session_state.bugs = []

st.title("🤖 Teal Enterprise Logic Debugger")
user_input = st.text_area("Input Terminal:", height=400, value=st.session_state.code)

col1, col2 = st.columns([1, 5])

if col1.button("🚀 Analyze & Fix"):
    if not user_input:
        st.warning("Input is empty.")
    else:
        st.session_state.code = user_input
        lines = user_input.split('\n')
        corrected_lines = []
        st.session_state.bugs = []
        
        # --- PASS 1: BUILD GLOBAL VARIABLE MAP ---
        # We look for ALL assignments in the whole file first
        all_defined = set(re.findall(r'\b(\w+)\b\s*=', user_input))
        # Add function names
        all_defined.update(re.findall(r'def\s+(\w+)', user_input))
        # Add function arguments from all 'def' lines
        for params in re.findall(r'def\s+\w+\((.*?)\)', user_input):
            for p in params.split(','):
                all_defined.add(p.strip())
        # Built-ins
        all_defined.update(["print", "int", "input", "range", "len", "str", "if", "elif", "else", "age", "score"])

        # --- PASS 2: LINE-BY-LINE DEBUGGING ---
        for i, line in enumerate(lines):
            indent = line[:len(line) - len(line.lstrip())]
            clean = line.strip()
            if not clean or clean.startswith("#"):
                corrected_lines.append(line); continue
            
            f_line, f_errs = clean, []

            # 1. SPELLING/NAMING (Fuzzy Logic) - Catches 'scorre' vs 'score'
            words = re.findall(r'\b\w+\b', clean)
            for w in words:
                # If word is not defined and looks like a typo of a defined variable
                if w.isdigit() or w in all_defined or len(w) < 3: continue
                
                # Check for close matches in our global map
                matches = difflib.get_close_matches(w, list(all_defined), n=1, cutoff=0.6)
                if matches:
                    suggestion = matches[0]
                    f_errs.append(f"Typo: '{w}' corrected to '{suggestion}'")
                    f_line = re.sub(r'\b' + w + r'\b', suggestion, f_line)

            # 2. LOGIC: Assignment vs Equality (= vs ==)
            if (clean.startswith("if ") or clean.startswith("elif ")) and "=" in clean and "==" not in clean:
                if not any(op in clean for op in [">=", "<=", "!="]):
                    f_errs.append("Logic: Changed '=' to '==' for comparison")
                    f_line = f_line.replace("=", "==")

            # 3. SYNTAX: Missing Colon & Parentheses
            if any(clean.startswith(x) for x in ["def ","if ","for ","elif ","else"]) and not clean.endswith(":"):
                f_errs.append("Syntax: Added missing colon (:)")
                f_line = f_line.rstrip() + ":"
            
            # Parentheses Balancer
            if f_line.count('(') > f_line.count(')'):
                f_errs.append("Syntax: Closed missing parentheses")
                f_line += ")" * (f_line.count('(') - f_line.count(')'))

            # 4. PRINT QUOTES
            if "print(" in f_line and not (re.search(r"['\"].*['\"]", f_line) or "," in f_line):
                f_errs.append("Syntax: Added missing quotes in print")
                content = f_line.split('(', 1)[1].rsplit(')', 1)[0]
                f_line = f_line.replace(content, f"'{content}'")

            if f_errs:
                st.session_state.bugs.append({"ln": i+1, "msg": " & ".join(f_errs), "fix": f_line})
            corrected_lines.append(indent + f_line)

        st.session_state.fixed = "\n".join(corrected_lines)
        st.rerun()

if col2.button("🧹 Clear All"):
    st.session_state.code = ""; st.session_state.fixed = ""; st.session_state.bugs = []
    st.rerun()

# --- RENDER ANALYSIS CARDS ---
for bug in st.session_state.bugs:
    st.markdown(f"""
    <div class="analysis-card">
        <div class="card-header">⚠️ Bug Detected at Line {bug['ln']}</div>
        <div class="explanation-text"><b>Explanation:</b> {bug['msg']}. This fix ensures Python logic flows correctly.</div>
        <div class="suggested-fix-box">💡 <b>Suggested fix:</b> {bug['fix']}</div>
    </div>
    """, unsafe_allow_html=True)

if st.session_state.fixed:
    st.subheader("💻 Corrected Application Block")
    st.code(st.session_state.fixed, language="python")
