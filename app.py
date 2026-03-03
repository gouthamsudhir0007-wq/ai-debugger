import streamlit as st
import time

# 1. Page Configuration
st.set_page_config(page_title="AI Debugger Pro", layout="wide", initial_sidebar_state="expanded")

# 2. CSS - Zero Red / Pure Enterprise Finishing
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    [data-testid="stSidebar"] { background-color: #000000 !important; }
    
    /* Terminal Styling - NO RED */
    .stTextArea>div>div>textarea {
        background-color: #111111 !important; 
        color: #FFFFFF !important; 
        border: 1px solid #333333 !important;
        border-radius: 10px;
    }
    .stTextArea>div>div>textarea:focus {
        border-color: #00d4ff !important; /* Teal Focus */
        box-shadow: 0 0 0 1px #00d4ff !important;
    }

    /* Enterprise Result Cards */
    .error-card {
        background-color: #1E1E1E;
        border: 1px solid #333333;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
    }
    .card-header { color: #FFA500; font-weight: bold; margin-bottom: 8px; }
    .fix-box {
        background-color: #142E1F;
        border-left: 5px solid #2ECC71;
        padding: 12px;
        border-radius: 6px;
        color: #D1FFD6;
        font-family: monospace;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar History
if "history" not in st.session_state: st.session_state.history = []
with st.sidebar:
    st.title("📂 History")
    for item in reversed(st.session_state.history):
        st.code(item, language="python")

# --- MAIN UI ---
st.title("🤖 C & Python AI Debugger")
code_input = st.text_area("Input Terminal:", height=300, placeholder="Paste code here...")

if st.button("🚀 Analyze & Fix"):
    if not code_input:
        st.warning("Please enter code.")
    else:
        with st.spinner("Deep scanning..."):
            time.sleep(1)
            lines = code_input.split('\n')
            
            for i, line in enumerate(lines):
                clean = line.strip()
                ln = i + 1
                if not clean: continue

                # --- C LANGUAGE DEBUGGING (Aggressive) ---
                # Detects C by semicolons, printf, include, or main
                if ";" in code_input or "printf" in clean or "#include" in clean or "main" in clean:
                    # Fix 1: Missing Semicolon
                    if not clean.endswith(";") and not any(x in clean for x in ["{", "}", "#include", "main"]):
                        st.markdown(f"""<div class="error-card">
                            <div class="card-header">⚠️ C.SemicolonMissing (Line {ln})</div>
                            <div class="explanation">C statements require a <b>;</b> to terminate.</div>
                            <div class="fix-box">💡 Suggested fix: {clean};</div>
                        </div>""", unsafe_allow_html=True)
                    
                    # Fix 2: Printf Format Errors
                    if "printf(" in clean and '"' not in clean:
                        st.markdown(f"""<div class="error-card">
                            <div class="card-header">⚠️ C.FormatStringError (Line {ln})</div>
                            <div class="explanation">printf requires double quotes <b>" "</b> for strings.</div>
                            <div class="fix-box">💡 Suggested fix: printf("{clean.split('(')[1].rstrip(')')}");</div>
                        </div>""", unsafe_allow_html=True)

                # --- PYTHON DEBUGGING (Aggressive) ---
                else:
                    # Fix 1: Missing quotes in print
                    if "print(" in clean and not ("'" in clean or '"' in clean):
                        st.markdown(f"""<div class="error-card">
                            <div class="card-header">⚠️ Py.StringLiteralError (Line {ln})</div>
                            <div class="explanation">Python print() requires quotes for text.</div>
                            <div class="fix-box">💡 Suggested fix: print('{clean[6:].rstrip(')')}')</div>
                        </div>""", unsafe_allow_html=True)
                    
                    # Fix 2: Missing Colons
                    if any(clean.startswith(x) for x in ["if ", "def ", "for ", "while "]) and not clean.endswith(":"):
                        st.markdown(f"""<div class="error-card">
                            <div class="card-header">⚠️ Py.SyntaxError (Line {ln})</div>
                            <div class="explanation">Missing colon <b>:</b> at the end of the block.</div>
                            <div class="fix-box">💡 Suggested fix: {clean}:</div>
                        </div>""", unsafe_allow_html=True)

            st.session_state.history.append(code_input)

if st.button("🗑️ Clear Input"):
    st.rerun()
