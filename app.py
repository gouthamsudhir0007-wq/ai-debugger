import streamlit as st
import time

# 1. Page Configuration
st.set_page_config(page_title="AI Debugger Pro", layout="wide", initial_sidebar_state="expanded")

# 2. CSS - HIDE CTRL+ENTER / TEAL FOCUS / NO RED
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
    .card-header { color: #FFA500; font-weight: bold; margin-bottom: 8px; }
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
st.title("🤖 Multi-Bug C & Python Debugger")
code_input = st.text_area("Input Terminal:", height=350, placeholder="int x = 10\nprintf(Hello)")

if st.button("🚀 Run Analysis"):
    if not code_input:
        st.warning("Please enter code.")
    else:
        with st.spinner("Analyzing all lines..."):
            time.sleep(1)
            lines = code_input.split('\n')
            
            # Detect language context
            is_c = any(x in code_input for x in [";", "printf", "int ", "float ", "include", "main", "{"])

            for i, line in enumerate(lines):
                clean = line.strip()
                ln = i + 1
                if not clean: continue

                line_errors = []
                fixed_line = clean

                # --- AGGRESSIVE C DEBUGGING ---
                if is_c:
                    # 1. Check for missing semicolons on declarations and calls
                    if not clean.endswith(";") and not any(x in clean for x in ["{", "}", "#", "main", "if", "for", "while"]):
                        line_errors.append("Missing terminating semicolon (;)")
                        fixed_line = fixed_line + ";"
                    
                    # 2. Check for malformed printf
                    if "printf(" in clean and '"' not in clean:
                        line_errors.append("Missing string double-quotes (\" \")")
                        content = clean.split('(')[1].split(')')[0]
                        fixed_line = f'printf("{content}");'

                # --- AGGRESSIVE PYTHON DEBUGGING ---
                else:
                    if "print(" in clean and not ("'" in clean or '"' in clean):
                        line_errors.append("Missing string delimiters (quotes)")
                        content = clean.split('(')[1].split(')')[0]
                        fixed_line = f"print('{content}')"
                    
                    if any(clean.startswith(x) for x in ["if ", "def ", "for ", "while "]) and not clean.endswith(":"):
                        line_errors.append("Missing block colon (:)")
                        fixed_line = fixed_line + ":"

                # Render Integrated Card
                if line_errors:
                    error_html = "".join([f'<div class="explanation-item">⚠️ {err}</div>' for err in line_errors])
                    st.markdown(f"""
                    <div class="error-card">
                        <div class="card-header">Line {ln}: Syntax Issues Found</div>
                        {error_html}
                        <div class="fix-box"><b>Corrected Line:</b><br>{fixed_line}</div>
                    </div>
                    """, unsafe_allow_html=True)
            
            st.session_state.history.append(code_input)

if st.button("🗑️ Clear Input"):
    st.rerun()
