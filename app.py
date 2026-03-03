import streamlit as st
from openai import OpenAI
from pydantic import BaseModel

# AI Output Structure
class DebugResult(BaseModel):
    error_type: str
    line_number: str
    explanation: str
    fix_snippet: str
    quick_fix: str

# Page Configuration
st.set_page_config(page_title="AI Debugger Pro", layout="wide")

# CUSTOM CSS - KILLING ALL RED
st.markdown("""
    <style>
    /* 1. Dark Sidebar */
    [data-testid="stSidebar"] {
        background-color: #111111;
        color: white;
    }
    
    /* 2. DARK TEXT AREA + DARK BORDER (Removing the Red Border) */
    .stTextArea>div>div>textarea {
        color: #FFFFFF !important; 
        background-color: #1E1E1E !important; 
        border: 1px solid #444444 !important; /* Dark border instead of red */
        border-radius: 8px;
    }
    
    /* Fix for when you click inside the text box */
    .stTextArea>div>div>textarea:focus {
        border-color: #00FFCC !important; /* Sleek teal glow instead of red */
        box-shadow: 0 0 0 1px #00FFCC !important;
    }

    /* 3. DARK BUTTONS (Forcing Gray/Black) */
    .stButton>button {
        border-radius: 8px;
        height: 3em;
        background-color: #333333 !important; 
        color: white !important;
        border: 1px solid #444444 !important;
        font-weight: 500;
    }
    
    /* Hover state - No Red */
    .stButton>button:hover {
        background-color: #444444 !important;
        border: 1px solid #00FFCC !important;
        color: #00FFCC !important;
    }

    /* Sidebar text colors */
    [data-testid="stSidebar"] .stText, [data-testid="stSidebar"] p, 
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2 {
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize History
if "history" not in st.session_state:
    st.session_state.history = []

# --- SIDEBAR ---
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
                st.write(f"**Fix:** {item['fix']}")
                st.download_button("💾 Save", item['full_code'], f"fix_{i}.py", key=f"dl_{i}")
    
    if st.button("🗑️ Clear History"):
        st.session_state.history = []
        st.rerun()

# --- MAIN UI ---
st.title("🤖 AI Debugging Assistant")
st.caption("Securely connected via Streamlit Secrets")

code_input = st.text_area("Paste your broken code here:", height=300, placeholder="Enter your Python code...")

col1, col2 = st.columns([1, 1])

if col1.button("🚀 Analyze & Fix") and code_input:
    # Uses the Secure Secret Key
    if "OPENAI_API_KEY" not in st.secrets:
        st.error("Missing API Key! Please add it to 'Secrets' in the Manage App menu.")
    else:
        try:
            client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
            with st.spinner("Analyzing..."):
                completion = client.beta.chat.completions.parse(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are a senior developer. Analyze code and return JSON."},
                        {"role": "user", "content": code_input},
                    ],
                    response_format=DebugResult,
                )
                res = completion.choices[0].message.parsed
                
                st.session_state.history.append({
                    "type": res.error_type, 
                    "fix": res.quick_fix, 
                    "full_code": res.fix_snippet
                })

                st.success(f"Error Identified: {res.error_type}")
                t1, t2 = st.tabs(["💡 Explanation", "💻 Fixed Code"])
                with t1:
                    st.write(res.explanation)
                with t2:
                    st.code(res.fix_snippet, language="python")

                if dev_mode:
                    st.json(res.model_dump())
        except Exception as e:
            st.error(f"Error: {e}")

if col2.button("🗑️ Clear Input"):
    st.rerun()
