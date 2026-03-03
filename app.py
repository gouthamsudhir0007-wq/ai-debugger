import streamlit as st
import time

# 1. Page Configuration
st.set_page_config(page_title="Python AI Debugger Pro", layout="wide", initial_sidebar_state="expanded")

# 2. CSS - PURE DARK / TEAL FOCUS / HIDE HINTS / ENTERPRISE CARDS
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    [data-testid="stSidebar"] { background-color: #000000 !important; }
    
    /* HIDE THE "Press Ctrl+Enter" HINT */
    .stTextArea div[data-baseweb="textarea"] + div { display: none !important; }

    /* Terminal Styling - NO RED */
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

    /* Enterprise Result Cards from your Image */
    .error-card {
        background-color: #1E1E1E;
        border: 1px solid #444444;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
    }
    .card-header { color: #FFA500; font-weight: bold; margin-bottom: 8px; font-size: 1.1em; }
    .explanation { color: #BBBBBB; font-size: 0.92em; margin-bottom: 12px; }
    
    /* Green Suggested Fix Box from Image */
    .fix-box {
        background-color: #142E1F;
        border-left: 5px solid #2ECC71;
        padding: 12px;
        border-radius: 6px;
        color: #D1FFD6;
        font-family: monospace;
    }

    /* Section Header Styling */
    .section-title {
        color: #00d4ff;
        font-size: 1.5em;
        font-weight: bold;
        margin-top: 25px;
        margin-bottom: 15px;
        border-bottom: 1px solid #333;
        padding-bottom: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar History
if "history" not in st.session_state: st.session_state.history = []
with st.sidebar:
    st.title("📂 Python History")
    for item in reversed(st.session_state.history):
        st.code(item, language="python")

# --- MAIN UI ---
st.title("🤖 Python Enterprise Debugger")
code_input = st.text_area("Input Terminal:", height=300, placeholder="def my_function()\n  print(hello)")

if st.button("🚀 Analyze & Fix Python Code"):
    if not code_input:
        st.warning("Please enter some Python code.")
    else:
        with st.spinner("Analyzing code structure..."):
            time.sleep(0.8)
            lines = code_input.split('\n')
            
            full_corrected_lines = []
            analysis_results = []
            
            # --- LINE-BY-LINE ANALYSIS ENGINE ---
            for i in range(len(lines)):
                line = lines[i]
                original_indent = line[:len(line) - len(line.lstrip())]
                clean = line.strip()
                ln = i + 1
                
                if not clean:
                    full_corrected_lines.append("")
                    continue

                line_errors = []
                fixed_content = clean

                # Check 1: Colons for blocks
                if any(clean.startswith(x) for x in ["def ", "if ", "for ", "while ", "elif ", "else", "try", "except"]) and not clean.endswith(":"):
                    line_errors.append(f"Missing colon (:) after '{clean.split()[0]}'")
                    fixed_content = fixed_content.rstrip() + ":"

                # Check 2: Missing Quotes in print
                if "print(" in clean and not ("'" in clean or '"' in clean):
                    line_errors.append("Missing string delimiters (quotes)")
                    try:
                        content = clean.split('(', 1)[1].rsplit(')', 1)[0]
                        fixed_content = f"print('{content}')"
                    except: pass
                
                # Check 3: Unclosed Parenthesis
                if fixed_content.count('(') > fixed_content.count(')'):
                    line_errors.append("Unclosed parenthesis")
                    fixed_content += ")"

                # Store result for the card view
                if line_errors:
                    analysis_results.append({
                        "line": ln,
                        "errors": line_errors,
                        "fix": fixed_content
                    })
                
                # Add to the full block with original indent
                full_corrected_lines.append(original_indent + fixed_content)

            # --- DISPLAY OUTPUTS ---
            
            # 1. INDIVIDUAL CARDS (As requested in pic)
            if analysis_results:
                st.markdown('<div class="section-title">🔍 Detailed Analysis</div>', unsafe_allow_html=True)
                for res in analysis_results:
                    err_text = " & ".join(res['errors'])
                    st.markdown(f"""
                    <div class="error-card">
                        <div class="card-header">⚠️ {err_text} (Line {res['line']})</div>
                        <div class="explanation"><b>Explanation:</b> Python syntax rules require proper punctuation and string formatting for code to execute.</div>
                        <div class="fix-box">💡 Suggested fix: {res['fix']}</div>
                    </div>
                    """, unsafe_allow_html=True)
            
            # 2. FULL BLOCK CORRECTED VERSION
            st.markdown('<div class="section-title">💻 Full Corrected Code</div>', unsafe_allow_html=True)
            final_code_block = "\n".join(full_corrected_lines)
            st.code(final_code_block, language="python")
            
            # Copy-paste helpful hint (Streamlit's st.code has a built-in copy button at top right)
            st.info("💡 You can copy the full block above using the button in the top-right of the code box.")
            
            st.session_state.history.append(final_code_block)

if st.button("🗑️ Clear Input"):
    st.rerun()
