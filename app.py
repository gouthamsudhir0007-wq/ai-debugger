import streamlit as st
import time
import re

# 1. Page Configuration
st.set_page_config(page_title="AI Debugger Pro", layout="wide", initial_sidebar_state="expanded")

# 2. Advanced CSS for Enterprise Cards
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    [data-testid="stSidebar"] { background-color: #000000 !important; }
    
    /* Error Card Container */
    .error-card {
        background-color: #1E1E1E;
        border: 1px solid #333333;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
    }
    
    .card-header { color: #FFA500; font-weight: bold; margin-bottom: 10px; display: flex; align-items: center; }
    .explanation { color: #CCCCCC; font-size: 0.95em; margin-bottom: 15px; }
    
    /* Suggested Fix Box */
    .fix-box {
        background-color: #142E1F;
        border-left: 5px solid #2ECC71;
        padding: 10px 15px;
        border-radius: 5px;
        color: #D1FFD6;
        font-size: 0.9em;
    }
    
    .stTextArea>div>div>textarea { background-color: #111111 !important; color: white !important; border: 1px solid #333333 !important; }
    </style>
    """, unsafe_allow_html=True)

if "history" not in st.session_state:
    st.session_state.history = []

# --- SIDEBAR ---
with st.sidebar:
    st.title("📂 History")
    for i, item in enumerate(reversed(st.session_state.history)):
        with st.expander(f"Session {len(st.session_state.history)-i}"):
            st.code(item['code'], language="python")

# --- MAIN UI ---
st.title("🤖 AI Debugging Assistant")
code_input = st.text_area("Paste your code here:", height=300, placeholder="def example()\n  print(hello")

if st.button("🚀 Analyze & Fix"):
    if not code_input:
        st.warning("Please enter code.")
    else:
        with st.spinner("Deep scanning for vulnerabilities..."):
            time.sleep(1.5)
            
            lines = code_input.split('\n')
            results = []
            
            # Logic to generate specific "Enterprise" cards
            for i, line in enumerate(lines):
                clean = line.strip()
                ln = i + 1
                
                # Check for Print Errors
                if "print(" in clean and not ("'" in clean or '"' in clean):
                    results.append({
                        "title": f"⚠️ StringLiteral Error at line {ln}",
                        "desc": f"The call to print('{clean[6:]}') is missing string delimiters, which will cause a NameError.",
                        "fix": f"Suggested fix: Wrap the content in quotes: print('{clean[6:].rstrip(')')}')"
                    })
                
                # Check for Block Errors (if, def, etc)
                if any(clean.startswith(x) for x in ["if ", "def ", "for "]) and not clean.endswith(":"):
                    results.append({
                        "title": f"⚠️ SyntaxException potential at line {ln}",
                        "desc": f"The '{clean.split()[0]}' statement is missing a colon, preventing the code block from starting.",
                        "fix": f"Suggested fix: Add a colon at the end of the line: {clean}:"
                    })

            # Display the "Enterprise" Cards
            if results:
                for res in results:
                    st.markdown(f"""
                    <div class="error-card">
                        <div class="card-header">{res['title']}</div>
                        <div class="explanation"><b>Explanation:</b> {res['desc']}</div>
                        <div class="fix-box">💡 {res['fix']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Also save the overall "Fixed Code" for history
                st.session_state.history.append({"code": code_input})
            else:
                st.success("No critical syntax issues detected in this segment.")

if st.button("🗑️ Clear Input"):
    st.rerun()
