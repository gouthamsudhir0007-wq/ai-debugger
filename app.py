import streamlit as st
import time

# 1. Page Configuration - Force Sidebar
st.set_page_config(page_title="AI Debugger Pro", layout="wide", initial_sidebar_state="expanded")

# 2. CSS - PURE DARK FINISHING (Removes all Red)
st.markdown("""
    <style>
    /* Professional Dark Theme */
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    [data-testid="stSidebar"] { background-color: #000000 !important; }
    
    /* Input Box Styling (No Red) */
    .stTextArea>div>div>textarea {
        background-color: #111111 !important; 
        color: #FFFFFF !important; 
        border: 1px solid #333333 !important;
        border-radius: 10px;
        font-family: 'Courier New', monospace;
    }
    .stTextArea>div>div>textarea:focus {
        border-color: #00d4ff !important;
        box-shadow: 0 0 0 1px #00d4ff !important;
    }

    /* Enterprise Cards */
    .error-card {
        background-color: #1E1E1E;
        border: 1px solid #333333;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
    }
    .card-header { color: #FFA500; font-weight: bold; margin-bottom: 8px; font-size: 1.1em; }
    .explanation { color: #BBBBBB; font-size: 0.95em; margin-bottom: 12px; }
    
    /* Green Suggested Fix Box */
    .fix-box {
        background-color: #142E1F;
        border-left: 5px solid #2ECC71;
        padding: 12px;
        border-radius: 6px;
        color: #D1FFD6;
        font-family: 'Courier New', monospace;
    }

    /* Professional Buttons */
    .stButton>button {
        background-color: #262730 !important;
        color: white !important;
        border: 1px solid #444444 !important;
        border-radius: 8px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: HISTORY & EXAMPLE LAB ---
with st.sidebar:
    st.title("📂 Debugger Tools")
    
    tab1, tab2 = st.tabs(["History", "Example Lab"])
    
    with tab1:
        if "history" not in st.session_state: st.session_state.history = []
        for item in reversed(st.session_state.history):
            st.code(item, language="python")
            
    with tab2:
        st.subheader("Select a Buggy Example")
        ex_lang = st.selectbox("Language", ["Python", "C", "Java", "JavaScript"])
        
        examples = {
            "Python": "print(Hello World\nif x > 5",
            "C": "printf(Hello);\nint x = 10",
            "Java": "System.out.println(Hello)\npublic class Main",
            "JavaScript": "console.log(Hello\nconst x = 5"
        }
        
        if st.button("Load Example"):
            st.info(f"Copy this into the box:\n\n{examples[ex_lang]}")

# --- MAIN UI ---
st.title("🤖 Multi-Lang AI Debugger")
code_input = st.text_area("Input Terminal:", height=300, placeholder="Paste your code here...")

if st.button("🚀 Analyze & Fix"):
    if not code_input:
        st.warning("Please enter code.")
    else:
        with st.spinner("Analyzing syntax structure..."):
            time.sleep(1)
            lines = code_input.split('\n')
            
            for i, line in enumerate(lines):
                clean = line.strip()
                ln = i + 1
                if not clean: continue

                # Logic for each language
                title, desc, fix = "", "", ""

                # JAVA
                if "System.out" in clean or "public class" in clean:
                    if "(" in clean and not ('"' in clean):
                        title = "⚠️ Java.StringLiteralError"
                        desc = "Java requires double quotes for strings in System.out.println()."
                        fix = f"System.out.println(\"{clean.split('(')[1].rstrip(')')}\");"
                
                # JAVASCRIPT
                elif "console.log" in clean or "const " in clean or "let " in clean:
                    if "(" in clean and not (clean.endswith(")") or clean.endswith(");")):
                        title = "⚠️ JS.UnclosedParenthesis"
                        desc = "JavaScript function calls must be closed with a parenthesis."
                        fix = f"{clean});"

                # C LANGUAGE
                elif "printf" in clean or ";" in code_input:
                    if not clean.endswith(";") and "main" not in clean and "{" not in clean:
                        title = "⚠️ C.MissingSemicolon"
                        desc = "C statements must end with a semicolon (;) to compile."
                        fix = f"{clean};"

                # PYTHON
                else:
                    if "print(" in clean and not ("'" in clean or '"' in clean):
                        title = "⚠️ Py.NameError"
                        desc = "Missing quotes. Python treats unquoted text as a variable."
                        fix = f"print('{clean[6:].rstrip(')')}')"
                    elif any(clean.startswith(x) for x in ["if ", "def ", "for "]) and not clean.endswith(":"):
                        title = "⚠️ Py.SyntaxError"
                        desc = "Colon missing at the end of the block header."
                        fix = f"{clean}:"

                # Display the Enterprise Card if an error was found
                if title:
                    st.markdown(f"""
                    <div class="error-card">
                        <div class="card-header">{title} (Line {ln})</div>
                        <div class="explanation"><b>Explanation:</b> {desc}</div>
                        <div class="fix-box">💡 Suggested fix: {fix}</div>
                    </div>
                    """, unsafe_allow_html=True)

            st.session_state.history.append(code_input)

if st.button("🗑️ Clear Input"):
    st.rerun()
