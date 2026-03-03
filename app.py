import streamlit as st
import time

# 1. Page Configuration
st.set_page_config(page_title="AI Debugger Pro", layout="wide", initial_sidebar_state="expanded")

# 2. CSS - HIDE HINTS / TEAL FOCUS / NO RED
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    [data-testid="stSidebar"] { background-color: #000000 !important; }
    
    /* HIDE THE "Press Ctrl+Enter" HINT */
    .stTextArea div[data-baseweb="textarea"] + div {
        display: none !important;
    }

    /* Terminal Styling - NO RED */
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
    .card-header { color: #FFA500; font-weight: bold; margin-bottom: 8px; font-size: 1.1em; }
    .explanation-item { color: #BBBBBB; font-size: 0.92em; margin-bottom: 4px; padding-left: 10px; border-left: 2px solid #FFA500; }
    .fix-box {
        background-color: #142E1F;
        border-left: 5px solid #2ECC71;
        padding: 12px;
        border-radius: 6px;
        color: #D1FFD6;
        font-family: monospace;
        margin-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

if "history" not in st.session_state: st.session_state.history = []

# --- MAIN UI ---
st.title("🤖 Precision C & Python Debugger")
code_input = st.text_area("Input Terminal:", height=400, placeholder="Paste your code here...")

if st.button("🚀 Run Deep Scan"):
    if not code_input:
        st.warning("Please enter code.")
    else:
        with st.spinner("Analyzing code structure..."):
            time.sleep(0.5)
            lines = code_input.split('\n')
            
            # --- STEP 1: SMART LANGUAGE DETECTION ---
            # Determine if we are in C mode or Python mode
            is_c_mode = any(x in code_input for x in ["#include", "int main", "printf", "scanf", "float ", "char "])
            
            for i in range(len(lines)):
                line = lines[i]
                clean = line.strip()
                ln = i + 1
                
                if not clean: continue

                line_errors = []
                fixed_line = clean

                # --- STEP 2: APPLY LANGUAGE-SPECIFIC RULES ---
                if is_c_mode:
                    # C RULES ONLY
                    if not clean.endswith(";") and not any(x in clean for x in ["{", "}", "#", "main", "if", "for", "while", "else"]):
                        line_errors.append("Missing semicolon (;)")
                        fixed_line = fixed_line + ";"
                    
                    if "printf(" in clean and '"' not in clean:
                        line_errors.append("Missing double quotes (\" \")")
                        try:
                            content = clean.split('(', 1)[1].rsplit(')', 1)[0]
                            fixed_line = f'printf("{content}");'
                        except: pass
                else:
                    # PYTHON RULES ONLY
                    if any(clean.startswith(x) for x in ["if ", "def ", "for ", "while ", "elif ", "else"]) and not clean.endswith(":"):
                        line_errors.append("Missing colon (:)")
                        fixed_line = fixed_line.rstrip() + ":"
                    
                    if "print(" in clean and not ("'" in clean or '"' in clean):
                        line_errors.append("Missing string quotes")
                        try:
                            content = clean.split('(', 1)[1].rsplit(')', 1)[0]
                            fixed_line = f"print('{content}')"
                        except: pass

                # --- STEP 3: RENDER RESULTS ---
                if line_errors:
                    error_html = "".join([f'<div class="explanation-item">⚠️ {err}</div>' for err in line_errors])
                    st.markdown(f"""
                    <div class="error-card">
                        <div class="card-header">Line {ln}: Syntax Analysis</div>
                        {error_html}
                        <div class="fix-box"><b>Corrected Version:</b><br>{fixed_line}</div>
                    </div>
                    """, unsafe_allow_html=True)

            st.session_state.history.append(code_input)

if st.button("🗑️ Clear Input"):
    st.rerun()

