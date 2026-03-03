import streamlit as st
import time

# 1. Page Configuration
st.set_page_config(page_title="AI Debugger Pro", layout="wide", initial_sidebar_state="expanded")

# 2. CSS - NO RED / TEAL FOCUS / PITCH BLACK SIDEBAR
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    [data-testid="stSidebar"] { background-color: #000000 !important; }
    
    /* Input Box Styling - FORCED TEAL */
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
    .explanation { color: #BBBBBB; font-size: 0.95em; margin-bottom: 12px; }
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
st.title("🤖 Enterprise C & Python Debugger")
code_input = st.text_area("Input Terminal:", height=350, placeholder="Paste multiple lines of code here...")

if st.button("🚀 Run Full Analysis"):
    if not code_input:
        st.warning("Please enter code.")
    else:
        with st.spinner("Scanning all lines..."):
            time.sleep(1)
            lines = code_input.split('\n')
            found_any_error = False
            
            # --- GLOBAL MULTI-LINE SCANNER ---
            for i, line in enumerate(lines):
                clean = line.strip()
                ln = i + 1
                if not clean: continue

                # Language Detection
                is_c = ";" in code_input or "printf" in code_input or "#include" in code_input or "main" in code_input

                if is_c:
                    # C Fixes
                    if not clean.endswith(";") and not any(x in clean for x in ["{", "}", "#include", "main"]):
                        found_any_error = True
                        st.markdown(f"""<div class="error-card">
                            <div class="card-header">⚠️ C.SemicolonMissing (Line {ln})</div>
                            <div class="explanation">Statement on line {ln} is missing a semicolon.</div>
                            <div class="fix-box">💡 Suggested fix: {clean};</div>
                        </div>""", unsafe_allow_html=True)
                    
                    if "printf(" in clean and '"' not in clean:
                        found_any_error = True
                        st.markdown(f"""<div class="error-card">
                            <div class="card-header">⚠️ C.FormatStringError (Line {ln})</div>
                            <div class="explanation">printf on line {ln} needs double quotes for the string.</div>
                            <div class="fix-box">💡 Suggested fix: printf("{clean.split('(')[1].rstrip(')')}");</div>
                        </div>""", unsafe_allow_html=True)

                else:
                    # Python Fixes
                    if "print(" in clean and not ("'" in clean or '"' in clean):
                        found_any_error = True
                        st.markdown(f"""<div class="error-card">
                            <div class="card-header">⚠️ Py.StringLiteralError (Line {ln})</div>
                            <div class="explanation">The print statement on line {ln} is missing quotes.</div>
                            <div class="fix-box">💡 Suggested fix: print('{clean[6:].rstrip(')')}')</div>
                        </div>""", unsafe_allow_html=True)
                    
                    if any(clean.startswith(x) for x in ["if ", "def ", "for ", "while "]) and not clean.endswith(":"):
                        found_any_error = True
                        st.markdown(f"""<div class="error-card">
                            <div class="card-header">⚠️ Py.SyntaxError (Line {ln})</div>
                            <div class="explanation">Missing colon on line {ln} at the end of the block header.</div>
                            <div class="fix-box">💡 Suggested fix: {clean}:</div>
                        </div>""", unsafe_allow_html=True)

            if not found_any_error:
                st.success("Analysis Complete: No syntax errors detected on any line.")
            
            st.session_state.history.append(code_input)

if st.button("🗑️ Clear Input"):
    st.rerun()
