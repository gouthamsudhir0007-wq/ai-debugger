import streamlit as st
import time
import sys
from io import StringIO

# 1. Page Configuration
st.set_page_config(page_title="Python Enterprise Debugger", layout="wide", initial_sidebar_state="expanded")

# 2. CSS - TRIPLE CHECKED: NO RED / HIDE HINTS / TEAL FOCUS
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    [data-testid="stSidebar"] { background-color: #000000 !important; }
    
    /* HIDE THE "Press Ctrl+Enter" HINT */
    .stTextArea div[data-baseweb="textarea"] + div { display: none !important; }

    /* Terminal Styling - PURE TEAL FOCUS */
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

    /* Enterprise Result Cards */
    .error-card {
        background-color: #1E1E1E;
        border: 1px solid #444444;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
    }
    .card-header { color: #FFA500; font-weight: bold; margin-bottom: 8px; font-size: 1.1em; }
    
    /* Green Fix Box */
    .fix-box {
        background-color: #142E1F;
        border-left: 5px solid #2ECC71;
        padding: 12px;
        border-radius: 6px;
        color: #D1FFD6;
        font-family: monospace;
    }
    
    /* Console Output Styling */
    .console-box {
        background-color: #000000;
        border: 1px solid #00d4ff;
        color: #00ff00;
        padding: 15px;
        font-family: 'Courier New', monospace;
        border-radius: 8px;
        margin-top: 10px;
        white-space: pre-wrap;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. State Management
if "last_fixed_code" not in st.session_state:
    st.session_state.last_fixed_code = ""

# --- MAIN UI ---
st.title("🤖 Python Enterprise Debugger & Runner")
code_input = st.text_area("Input Terminal:", height=300, placeholder="Paste your Python code here...")

# Action Buttons
col1, col2, col3 = st.columns([1, 1, 4])

with col1:
    analyze_btn = st.button("🚀 Analyze & Fix")
with col2:
    run_btn = st.button("▶️ Run Code")
with col3:
    if st.button("🗑️ Clear"):
        st.rerun()

# --- LOGIC ENGINE ---
if analyze_btn:
    if not code_input:
        st.warning("Please enter code first.")
    else:
        with st.spinner("Analyzing Every Line..."):
            time.sleep(0.5)
            lines = code_input.split('\n')
            full_corrected_list = []
            analysis_cards = []

            for i in range(len(lines)):
                line = lines[i]
                indent = line[:len(line) - len(line.lstrip())]
                clean = line.strip()
                ln = i + 1
                
                if not clean:
                    full_corrected_list.append("")
                    continue

                errors = []
                fixed = clean

                # Check 1: Colons
                if any(clean.startswith(x) for x in ["def ","if ","for ","while ","elif ","else"]) and not clean.endswith(":"):
                    errors.append("Missing colon (:)")
                    fixed = fixed.rstrip() + ":"
                
                # Check 2: Print Quotes
                if "print(" in clean and not ("'" in clean or '"' in clean):
                    errors.append("Missing string quotes")
                    try:
                        content = clean.split('(', 1)[1].rsplit(')', 1)[0]
                        fixed = f"print('{content}')"
                    except: pass

                if errors:
                    analysis_cards.append({"line": ln, "msg": " & ".join(errors), "fix": fixed})
                
                full_corrected_list.append(indent + fixed)

            # Display Enterprise Cards
            if analysis_cards:
                st.subheader("🔍 Detailed Analysis")
                for card in analysis_cards:
                    st.markdown(f"""
                    <div class="error-card">
                        <div class="card-header">Line {card['line']}: {card['msg']}</div>
                        <div class="fix-box">💡 Suggested fix: {card['fix']}</div>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Display Full Block
            st.subheader("💻 Full Corrected Code")
            final_code = "\n".join(full_corrected_list)
            st.code(final_code, language="python")
            st.session_state.last_fixed_code = final_code
            st.success("Analysis complete. You can now 'Run' the code.")

if run_btn:
    if not st.session_state.last_fixed_code:
        st.error("Please click 'Analyze & Fix' before running.")
    else:
        st.subheader("🖥️ Console Output")
        # Capturing stdout
        old_stdout = sys.stdout
        redirected_output = sys.stdout = StringIO()
        
        try:
            # Running the fixed code
            exec(st.session_state.last_fixed_code)
            sys.stdout = old_stdout
            output = redirected_output.getvalue()
            result = output if output else "Process finished with no output."
            st.markdown(f'<div class="console-box">{result}</div>', unsafe_allow_html=True)
        except Exception as e:
            sys.stdout = old_stdout
            st.error(f"Logic/Runtime Error: {e}")
