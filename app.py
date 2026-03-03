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

# 2. Page Configuration & Styling
st.set_page_config(page_title="AI Debugger Ultra", layout="wide")

# Custom CSS for a modern look
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 10px; height: 3em; }
    .stTextArea>div>div>textarea { border-radius: 10px; }
    [data-testid="stSidebar"] { background-color: #f0f2f6; }
    </style>
    """, unsafe_allow_html=True)

# Initialize Session State
if "history" not in st.session_state:
    st.session_state.history = []

# --- SIDEBAR: HISTORY & DEV MODE ---
with st.sidebar:
    st.title("📂 Project Lab")
    dev_mode = st.toggle("🛠️ Developer Mode")
    
    st.divider()
    st.subheader("Recent Fixes")
    if not st.session_state.history:
        st.info("No bugs analyzed yet.")
    else:
        for i, item in enumerate(reversed(st.session_state.history)):
            with st.expander(f"Bug {len(st.session_state.history) - i}: {item['type']}"):
                st.write(f"**Fix:** {item['fix']}")
                # Download button for this specific fix
                st.download_button(
                    label="💾 Download Fix",
                    data=f"Error: {item['type']}\nLine: {item['line']}\nFix: {item['fix']}\n\nFull Code:\n{item['full_code']}",
                    file_name=f"fix_{i}.txt",
                    key=f"dl_{i}"
                )
    
    if st.button("🗑️ Clear History"):
        st.session_state.history = []
        st.rerun()

# --- MAIN UI ---
st.title("🤖 AI Debugging Assistant")
st.caption("The professional way to squash bugs instantly.")

api_key = st.text_input("OpenAI API Key", type="password", help="Your key is never stored on our servers.")

code_input = st.text_area("Paste your code here:", height=250, placeholder="def my_function():\n    print('Hello World'...")

col1, col2 = st.columns(2)

if col1.button("🚀 Analyze & Fix") and code_input:
    if not api_key:
        st.error("Please provide an API Key.")
    else:
        try:
            client = OpenAI(api_key=api_key)
            with st.spinner("AI is inspecting your code..."):
                completion = client.beta.chat.completions.parse(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are a senior developer. Analyze code and return JSON."},
                        {"role": "user", "content": code_input},
                    ],
                    response_format=DebugResult,
                )
                
                res = completion.choices[0].message.parsed

                # Add to History
                st.session_state.history.append({
                    "type": res.error_type,
                    "fix": res.quick_fix,
                    "line": res.line_number,
                    "full_code": res.fix_snippet
                })

                # Display Results
                st.success(f"Found it! This looks like a **{res.error_type}**.")
                
                t1, t2 = st.tabs(["💡 Explanation", "💻 Fixed Code"])
                with t1:
                    st.write(res.explanation)
                    st.info(f"**Target Line:** {res.line_number}")
                with t2:
                    st.code(res.fix_snippet, language="python")

                if dev_mode:
                    st.divider()
                    st.subheader("Raw AI Response (JSON)")
                    st.json(res.model_dump())

        except Exception as e:
            st.error(f"Error: {e}")

if col2.button("🗑️ Clear Input"):
    st.rerun()
