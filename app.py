import streamlit as st
from openai import OpenAI
from pydantic import BaseModel

# 1. Structure for the AI Output
class DebugResult(BaseModel):
    error_type: str
    line_number: str
    explanation: str
    fix_snippet: str
    quick_fix: str

# 2. Page Configuration
st.set_page_config(page_title="AI Debugger Pro", layout="wide")

# Initialize History in Session State
if "history" not in st.session_state:
    st.session_state.history = []

# --- SIDEBAR: HISTORY ---
with st.sidebar:
    st.title("📂 Debug History")
    if not st.session_state.history:
        st.info("No bugs analyzed yet.")
    else:
        for i, item in enumerate(reversed(st.session_state.history)):
            with st.expander(f"Bug {len(st.session_state.history) - i}: {item['type']}"):
                st.write(f"**Fix:** {item['fix']}")
                st.caption(f"Line: {item['line']}")
    
    st.divider()
    if st.button("Clear History"):
        st.session_state.history = []
        st.rerun()

# --- MAIN UI ---
st.title("🤖 AI Debugging Assistant")

# API Key Check (Use Secrets for permanent setup)
api_key = st.text_input("OpenAI API Key", type="password")

code_input = st.text_area("Paste your code here:", height=200)

col_run, col_clear = st.columns(2)

if col_run.button("🚀 Analyze Code") and code_input:
    if not api_key:
        st.error("Please provide an API Key.")
    else:
        try:
            client = OpenAI(api_key=api_key)
            with st.spinner("Thinking..."):
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
                    "line": res.line_number
                })

                # Show Results
                st.success(f"Fixed: {res.error_type}")
                st.markdown(f"### 💡 Explanation\n{res.explanation}")
                st.code(res.fix_snippet, language="python")
                st.rerun() # Refresh to update the sidebar history immediately

        except Exception as e:
            st.error(f"Error: {e}")

if col_clear.button("🗑️ Clear Input"):
    st.rerun()
