import streamlit as st
from openai import OpenAI
from pydantic import BaseModel

# 1. Define the AI's "Brain" structure
class DebugResult(BaseModel):
    error_type: str
    line_number: str
    explanation: str
    fix_snippet: str
    quick_fix: str

# 2. Page Setup
st.set_page_config(page_title="AI Debugger Pro", layout="wide")

# 3. Custom CSS (Fixes Sidebar color and Input Text visibility)
st.markdown("""
    <style>
    /* Dark Sidebar Style */
    [data-testid="stSidebar"] {
        background-color: #1E1E1E;
        color: white;
    }
    [data-testid="stSidebar"] .stText, [data-testid="stSidebar"] p, 
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2 {
        color: white !important;
    }
    
    /* Fix: Makes typed text dark so it's visible in the white box */
    .stTextArea>div>div>textarea {
        color: #1E1E1E !important; 
        background-color: #FFFFFF !important;
        border-radius: 10px;
    }

    /* Button Styling */
    .stButton>button {
        border-radius: 10px;
        height: 3em;
        background-color: #4F4F4F;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# 4. Initialize History
if "history" not in st.session_state:
    st.session_state.history = []

# --- SIDEBAR SECTION ---
with st.sidebar:
    st.title("📂 Project Lab")
    dev_mode = st.toggle("🛠️ Developer Mode")
    st.divider()
    st.subheader("Recent Fixes")
    
    if not st.session_state.history:
        st.info("No history yet.")
    else:
        for i, item in enumerate(reversed(st.session_state.history)):
            with st.expander(f"Bug: {item['type']}"):
                st.write(f"**Quick Fix:** {item['fix']}")
                st.download_button("💾 Save Fix", item['full_code'], f"fix_{i}.py", key=f"dl_{i}")
    
    if st.button("🗑️ Clear History"):
        st.session_state.history = []
        st.rerun()

# --- MAIN INTERFACE ---
st.title("🤖 AI Debugging Assistant")
st.caption("Connected via Secure Secrets")

# The main input box
code_input = st.text_area("Paste your broken code here:", height=250, placeholder="e.g., print('Hello' (missing parenthesis)")

col1, col2 = st.columns(2)

if col1.button("🚀 Analyze & Fix") and code_input:
    # Check if the Secret Key is set in Streamlit Cloud Settings
    if "OPENAI_API_KEY" not in st.secrets:
        st.error("Missing API Key! Please add 'OPENAI_API_KEY' to your Streamlit Secrets.")
    else:
        try:
            client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
            with st.spinner("AI is inspecting your code..."):
                # Call OpenAI with the specific DebugResult format
                completion = client.beta.chat.completions.parse(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are a senior developer. Analyze code and return JSON."},
                        {"role": "user", "content": code_input},
                    ],
                    response_format=DebugResult,
                )
                res = completion.choices[0].message.parsed
                
                # Save to history list
                st.session_state.history.append({
                    "type": res.error_type, 
                    "fix": res.quick_fix, 
                    "full_code": res.fix_snippet
                })

                # Display Results
                st.success(f"Found it! Error Type: {res.error_type}")
                
                tab_expl, tab_code = st.tabs(["💡 Explanation", "💻 Fixed Code"])
                with tab_expl:
                    st.write(res.explanation)
                    st.info(f"**Line Number:** {res.line_number}")
                with tab_code:
                    st.code(res.fix_snippet, language="python")

                # If Dev Mode is on, show the raw data
                if dev_mode:
                    st.divider()
                    st.subheader("Raw AI Response")
                    st.json(res.model_dump())
                    
        except Exception as e:
            st.error(f"Something went wrong: {e}")

if col2.button("🗑️ Clear Input"):
    st.rerun()
