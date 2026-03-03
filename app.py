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

# Modern Dark Sidebar CSS
st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        background-color: #1E1E1E;
        color: white;
    }
    [data-testid="stSidebar"] .stText, [data-testid="stSidebar"] p, 
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2 {
        color: white !important;
    }
    .stButton>button { width: 100%; border-radius: 10px; height: 3em; background-color: #4F4F4F; color: white; }
    .stTextArea>div>div>textarea { border-radius: 10px; background-color: #f9f9f9; }
    </style>
    """, unsafe_allow_html=True)

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
                st.write(item['fix'])
                st.download_button("💾 Save", item['full_code'], f"fix_{i}.py", key=f"dl_{i}")
    
    if st.button("🗑️ Clear History"):
        st.session_state.history = []
        st.rerun()

# --- MAIN UI ---
st.title("🤖 AI Debugging Assistant")
st.caption("Connected via Secure Secrets")

code_input = st.text_area("Paste your code here:", height=250)

col1, col2 = st.columns(2)

if col1.button("🚀 Analyze & Fix") and code_input:
    # Use the secret key automatically
    if "OPENAI_API_KEY" not in st.secrets:
        st.error("Missing API Key in Secrets! Go to Settings > Secrets.")
    else:
        try:
            client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
            with st.spinner("AI is inspecting..."):
                completion = client.beta.chat.completions.parse(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are a senior developer. Analyze code and return JSON."},
                        {"role": "user", "content": code_input},
                    ],
                    response_format=DebugResult,
                )
                res = completion.choices[0].message.parsed
                st.session_state.history.append({"type": res.error_type, "fix": res.quick_fix, "full_code": res.fix_snippet})

                st.success(f"Fixed: {res.error_type}")
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
