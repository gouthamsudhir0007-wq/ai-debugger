import streamlit as st
from openai import OpenAI
from pydantic import BaseModel

# 1. AI Output Structure
class DebugResult(BaseModel):
    error_type: str
    line_number: str
    explanation: str
    fix_snippet: str
    quick_fix: str

# 2. Page Configuration
st.set_page_config(page_title="AI Debugger Pro", layout="wide")

# 3. Custom CSS - COLOR MATCHED (No Red)
st.markdown("""
    <style>
    /* Global Background match */
    .main {
        background-color: #0E1117;
    }

    /* Dark Sidebar */
    [data-testid="stSidebar"] {
        background-color: #111111;
        border-right: 1px solid #333333;
    }
    
    /* DARK TEXT AREA - Removing Red Outlines */
    .stTextArea>div>div>textarea {
        color: #FFFFFF !important; 
        background-color: #1E1E1E !important; 
        border: 1px solid #333333 !important; /* Subtle gray border */
        border-radius: 8px;
    }
    
    /* Fix the border when typing/clicking (Turns Teal instead of Red) */
    .stTextArea>div>div>textarea:focus {
        border-color: #00d4ff !important; 
        box-shadow: 0 0 0 1px #00d4ff !important;
    }

    /* SLEEK BUTTONS - Dark with Teal hover */
    .stButton>button {
        border-radius: 8px;
        height: 3em;
        background-color: #262730 !important; 
        color: #FFFFFF !important;
        border: 1px solid #444444 !important;
        transition: 0.3s;
    }
    
    .stButton>button:hover {
        border-color: #00d4ff !important;
        color: #00d4ff !important;
        background-color: #1E1E1E !important;
    }

    /* Sidebar text colors */
    [data-testid="stSidebar"] .stText, [data-testid="stSidebar"] p, 
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] span {
        color: #E0E0E0 !important;
    }
    
    /* Style the tabs to match the dark theme */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #1E1E1E;
        border-radius: 4px 4px 0 0;
        color: white;
    }
    .stTabs [aria-selected="true"] {
        background-color: #00d4ff22 !important;
        border-bottom: 2px solid #00d4ff !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 4. Initialize History
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
