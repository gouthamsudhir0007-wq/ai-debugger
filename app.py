import streamlit as st
import time

# 1. Page Configuration
st.set_page_config(page_title="AI Debugger Pro", layout="wide", initial_sidebar_state="expanded")

# 2. CSS - HIDE HINTS / TEAL FOCUS / PITCH BLACK SIDEBAR
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
st.title("🤖 Universal Line-by-Line Debugger")
code_input = st.text_area("Input Terminal:", height=400, placeholder="int x = 10\nprint(Hello)\nif x > 5")

if st.button("🚀 Execute Deep Scan"):
    if not code_input:
        st.warning("Please enter code.")
    else:
        with st.spinner("Processing every line..."):
            time.sleep(0.8)
            lines = code_input.split('\n')
            
            # This loop forces the AI to look at EVERY line index
            for i in range(len(lines)):
                line = lines[i]
                clean = line.strip()
                ln = i + 1
                
                if not clean:
                    continue

                line_errors = []
                fixed_line = clean

                # --- 1. C-STYLE SEMICOLON CHECK (Applied to all non-block lines) ---
                # Checks if line looks like a C statement but lacks ';'
                if not clean.endswith(";") and not any(x in clean for x in ["{", "}", "#", "main", "if", "for", "while", "def "]):
                    # If it's not a Python block, it's likely a C statement needing a ';'
                    line_errors.append("Missing terminating semicolon (;)")
                    fixed_line = fixed_line + ";"

                # --- 2. PRINT/PRINTF QUOTE CHECK ---
                if ("print(" in clean or "printf(" in clean) and '"' not in clean and "'" not in clean:
                    line_errors.append("Missing string delimiters (quotes)")
                    try:
                        content = clean.split('(', 1)[1].rsplit(')', 1)[0]
                        if "printf" in clean:
                            fixed_line = f'printf("{content}");'
                        else:
                            fixed_line = f"print('{content}')"
                    except:
                        pass

                # --- 3. PYTHON BLOCK COLON CHECK ---
                if any(clean.startswith(x) for x in ["if ", "def ", "for ", "while ", "elif ", "else"]) and not clean.endswith(":"):
                    line_errors.append("Missing block colon (:)")
                    fixed_line = fixed_line.rstrip() + ":"

                # --- 4. RENDER IF BUGS FOUND ---
                if line_errors:
                    # Remove duplicates and format
                    error_html = "".join([f'<div class="explanation-item">⚠️ {err}</div>' for err in set(line_errors)])
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
