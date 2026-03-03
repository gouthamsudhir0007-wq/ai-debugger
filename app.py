import streamlit as st
import time

# 1. Page Configuration
st.set_page_config(page_title="AI Debugger Pro", layout="wide", initial_sidebar_state="expanded")

# 2. CSS - PURE DARK / TEAL FOCUS / NO RED
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    [data-testid="stSidebar"] { background-color: #000000 !important; }
    
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

    .error-card {
        background-color: #1E1E1E;
        border: 1px solid #444444;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
    }
    .card-header { color: #FFA500; font-weight: bold; margin-bottom: 8px; font-size: 1.1em; }
    .explanation-item { color: #BBBBBB; font-size: 0.95em; margin-bottom: 5px; padding-left: 10px; border-left: 2px solid #FFA500; }
    .fix-box {
        background-color: #142E1F;
        border-left: 5px solid #2ECC71;
        padding: 12px;
        border-radius: 6px;
        color: #D1FFD6;
        font-family: 'Courier New', monospace;
        margin-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

if "history" not in st.session_state: st.session_state.history = []

# --- MAIN UI ---
st.title("🤖 Advanced C & Python Debugger")
code_input = st.text_area("Input Terminal:", height=350, placeholder="Paste code here...")

if st.button("🚀 Run Smart Analysis"):
    if not code_input:
        st.warning("Please enter code.")
    else:
        with st.spinner("Analyzing line-by-line..."):
            time.sleep(1)
            lines = code_input.split('\n')
            
            for i, line in enumerate(lines):
                clean = line.strip()
                ln = i + 1
                if not clean: continue

                # Containers for this specific line
                line_errors = []
                fixed_line = clean

                # --- MULTI-BUG DETECTION (C & Python) ---
                
                # Check 1: Semicolons (C)
                if ";" in code_input or "printf" in clean:
                    if not clean.endswith(";") and not any(x in clean for x in ["{", "}", "#", "main"]):
                        line_errors.append("Missing terminating semicolon (;)")
                        fixed_line = fixed_line + ";"
                
                # Check 2: Quotes/Strings (C & Py)
                if ("printf(" in clean or "print(" in clean) and '"' not in clean and "'" not in clean:
                    line_errors.append("Missing string delimiters (quotes)")
                    if "printf(" in clean:
                        content = clean.split('(')[1].split(')')[0]
                        fixed_line = f'printf("{content}");'
                    else:
                        content = clean.split('(')[1].split(')')[0]
                        fixed_line = f"print('{content}')"

                # Check 3: Python Colons
                if any(clean.startswith(x) for x in ["if ", "def ", "for "]) and not clean.endswith(":"):
                    line_errors.append("Missing block colon (:)")
                    fixed_line = fixed_line + ":"

                # --- DISPLAY SINGLE CARD FOR MULTIPLE BUGS ---
                if line_errors:
                    error_list_html = "".join([f'<div class="explanation-item">⚠️ {err}</div>' for err in line_errors])
                    st.markdown(f"""
                    <div class="error-card">
                        <div class="card-header">Line {ln}: Multiple Issues Detected</div>
                        {error_list_html}
                        <div class="fix-box"><b>Suggested Fix:</b><br>{fixed_line}</div>
                    </div>
                    """, unsafe_allow_html=True)
            
            st.session_state.history.append(code_input)

if st.button("🗑️ Clear Input"):
    st.rerun()
