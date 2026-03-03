import streamlit as st
import time

# 1. Page Configuration - Force Sidebar
st.set_page_config(page_title="AI Debugger Pro", layout="wide", initial_sidebar_state="expanded")

# 2. Enterprise CSS (No Red, Pure Black/Dark Grey/Teal)
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    [data-testid="stSidebar"] { background-color: #000000 !important; border-right: 1px solid #333333; }
    
    /* Input Box Styling - NO RED */
    .stTextArea>div>div>textarea {
        background-color: #111111 !important; 
        color: #FFFFFF !important; 
        border: 1px solid #333333 !important;
        border-radius: 12px;
    }
    .stTextArea>div>div>textarea:focus {
        border-color: #00d4ff !important;
        box-shadow: 0 0 0 1px #00d4ff !important;
    }

    /* Enterprise Error Cards */
    .error-card {
        background-color: #1E1E1E;
        border: 1px solid #333333;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
    }
    .card-header { color: #FFA500; font-weight: bold; margin-bottom: 5px; font-size: 1.1em; }
    .explanation { color: #CCCCCC; font-size: 0.95em; margin-bottom: 12px; }
    
    /* Suggested Fix Box */
    .fix-box {
        background-color: #142E1F;
        border-left: 5px solid #2ECC71;
        padding: 10px 15px;
        border-radius: 5px;
        color: #D1FFD6;
        font-family: 'Courier New', monospace;
    }
    
    .stButton>button { border-radius: 10px; background-color: #262730 !important; color: white !important; border: 1px solid #444444 !important; }
    .stButton>button:hover { border-color: #00d4ff !important; color: #00d4ff !important; }
    </style>
    """, unsafe_allow_html=True)

if "history" not in st.session_state:
    st.session_state.history = []

# --- SIDEBAR: HISTORY ---
with st.sidebar:
    st.title("📂 History")
    if not st.session_state.history:
        st.info("No activity yet.")
    else:
        for i, item in enumerate(reversed(st.session_state.history)):
            with st.expander(f"Session {len(st.session_state.history)-i}"):
                st.code(item['code'])
        if st.button("🗑️ Clear History"):
            st.session_state.history = []
            st.rerun()

# --- MAIN UI ---
st.title("🤖 Enterprise Multi-Lang Debugger")
code_input = st.text_area("Paste Python, C, Java, or JavaScript:", height=300)

if st.button("🚀 Analyze & Fix"):
    if not code_input:
        st.warning("Please enter code.")
    else:
        with st.spinner("Analyzing syntax structure..."):
            time.sleep(1)
            lines = code_input.split('\n')
            results = []
            
            for i, line in enumerate(lines):
                clean = line.strip()
                ln = i + 1
                if not clean: continue

                # --- MULTI-LANG LOGIC ---
                
                # 1. JAVA / JS (Semicolons & Brackets)
                if any(x in code_input for x in ["public class", "System.out", "let ", "const ", "function"]):
                    if not clean.endswith(";") and not clean.endswith("{") and not clean.endswith("}"):
                        results.append({
                            "title": f"⚠️ Missing Terminator (Line {ln})",
                            "desc": "Statement is missing a semicolon (;), which is required in Java/JavaScript.",
                            "fix": f"{clean};"
                        })
                
                # 2. C LANGUAGE (printf & main)
                if "printf" in clean and not ('"' in clean):
                    results.append({
                        "title": f"⚠️ Invalid Format String (Line {ln})",
                        "desc": "C printf functions require double quotes for strings.",
                        "fix": f'printf("your_message");'
                    })

                # 3. PYTHON (Colons & Print)
                if "print(" in clean and not ("'" in clean or '"' in clean) and ";" not in code_input:
                    results.append({
                        "title": f"⚠️ StringLiteral Error (Line {ln})",
                        "desc": "Python print requires quotes around the message.",
                        "fix": f"print('{clean[6:].rstrip(')')}')"
                    })
                
                if any(clean.startswith(x) for x in ["if ", "def ", "for "]) and not clean.endswith(":"):
                    results.append({
                        "title": f"⚠️ Block Suffix Error (Line {ln})",
                        "desc": "Python blocks must end with a colon (:).",
                        "fix": f"{clean}:"
                    })

            # DISPLAY CARDS
            if results:
                for res in results:
                    st.markdown(f"""
                    <div class="error-card">
                        <div class="card-header">{res['title']}</div>
                        <div class="explanation"><b>Explanation:</b> {res['desc']}</div>
                        <div class="fix-box">💡 Suggested fix: {res['fix']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                st.session_state.history.append({"code": code_input})
            else:
                st.success("Analysis Complete: No syntax violations found.")

# --- TEST EXAMPLES ---
with st.expander("📝 Click for Errored Code Examples"):
    st.write("**Python:** `print(hello` or `if x > 5` (Missing colon/quotes)")
    st.write("**C:** `printf(hello)` or `int x = 10` (Missing semicolon/quotes)")
    st.write("**Java:** `System.out.println(hi)` or `int y = 5` (Missing semicolon/quotes)")
    st.write("**JS:** `let x = 10` or `console.log(test)` (Missing semicolon/quotes)")

if st.button("🗑️ Clear Input"):
    st.rerun()
