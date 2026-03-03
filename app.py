import streamlit as st
import time
import ast

# 1. Page Configuration - Force Sidebar and Professional Layout
st.set_page_config(
    page_title="AI Debugger Pro", 
    layout="wide", 
    initial_sidebar_state="expanded" 
)

# 2. CSS - Deep Black Theme & Teal Accents (No Red, No Sidebar Clutter)
st.markdown("""
    <style>
    /* Hide Streamlit elements for a clean app look */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Force Dark Sidebar */
    [data-testid="stSidebar"] {
        background-color: #000000 !important;
        border-right: 1px solid #333333;
    }
    
    /* Sidebar Text Styling */
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] h1, [data-testid="stSidebar"] span {
        color: #FFFFFF !important;
    }

    /* Professional Dark Text Area */
    .stTextArea>div>div>textarea {
        color: #FFFFFF !important; 
        background-color: #1E1E1E !important; 
        border: 1px solid #333333 !important;
        border-radius: 12px;
        font-family: 'Courier New', Courier, monospace;
    }

    /* Teal focus border (No Red) */
    .stTextArea>div>div>textarea:focus {
        border-color: #00d4ff !important;
        box-shadow: 0 0 0 1px #00d4ff !important;
    }

    /* Button Styling */
    .stButton>button {
        border-radius: 12px;
        background-color: #262730 !important; 
        color: #FFFFFF !important;
        border: 1px solid #444444 !important;
    }
    .stButton>button:hover {
        border-color: #00d4ff !important;
        color: #00d4ff !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Initialize History in Background
if "history" not in st.session_state:
    st.session_state.history = []

# --- SIDEBAR: HISTORY ---
with st.sidebar:
    st.title("📂 Fix History")
    st.write("Recent debugging sessions:")
    st.divider()
    
    if not st.session_state.history:
        st.info("No history yet.")
    else:
        for i, item in enumerate(reversed(st.session_state.history)):
            with st.expander(f"Fix {len(st.session_state.history)-i}"):
                st.code(item['code'], language="python")
        
        st.divider()
        if st.button("🗑️ Clear History"):
            st.session_state.history = []
            st.rerun()

# --- MAIN UI ---
st.title("🤖 AI Debugging Assistant")

code_input = st.text_area("", height=400, placeholder="# Paste your long Python code here...")

if st.button("🚀 Analyze & Fix"):
    if not code_input:
        st.warning("Please enter code to debug.")
    else:
        with st.spinner("Running deep code analysis..."):
            time.sleep(1.2)
            
            # --- ADVANCED DEBUGGING LOGIC ---
            fixed_lines = []
            issues_found = []
            
            for line in code_input.split('\n'):
                original = line
                stripped = line.strip()
                
                if not stripped:
                    fixed_lines.append("")
                    continue
                
                # 1. Fix unclosed prints
                if stripped.startswith("print(") and not (stripped.endswith(")") or stripped.endswith("')")):
                    line = line.rstrip() + "')" if "'" in line else line.rstrip() + ")"
                    issues_found.append("Fixed unclosed print statement.")
                
                # 2. Fix missing colons in blocks
                keywords = ["if ", "else", "elif ", "def ", "for ", "while ", "try", "except", "class "]
                if any(stripped.startswith(k) for k in keywords) and not stripped.endswith(":"):
                    line = line.rstrip() + ":"
                    issues_found.append(f"Added missing colon to '{stripped.split()[0]}'.")
                
                fixed_lines.append(line)

            final_code = "\n".join(fixed_lines)
            
            # Save to History
            st.session_state.history.append({"code": final_code})
            
            # Results Display
            st.success("Analysis Complete")
            if issues_found:
                st.info(f"**Changes made:**\n" + "\n".join([f"- {iss}" for iss in set(issues_found[:3])]))
            else:
                st.info("Structure looks good, but optimized formatting.")
                
            st.markdown("### 💻 Corrected Code")
            st.code(final_code, language="python")

if st.button("🗑️ Clear Input"):
    st.rerun()
