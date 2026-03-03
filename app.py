import streamlit as st
from openai import OpenAI
from pydantic import BaseModel
import json

# 1. Define the Structure (JSON Schema)
class DebugResult(BaseModel):
    error_type: str
    line_number: str
    explanation: str
    fix_snippet: str
    quick_fix: str

# 2. Setup Page Config
st.set_page_config(page_title="AI Debugging Assistant", layout="wide")
st.title("🤖 AI Debugging Assistant")
st.caption("Paste your code below to find and fix bugs in real-time.")

# Sidebar for API Key & Model Config
with st.sidebar:
    api_key = st.text_input("OpenAI API Key", type="password")
    model = st.selectbox("Model", ["gpt-4o", "gpt-4o-mini"], index=1)
    st.info("Tip: Use 'gpt-4o-mini' for speed and 'gpt-4o' for complex logic.")

# 3. Code Input
code_input = st.text_area("Paste your code here:", height=250, placeholder="def hello_world():\n    print('Hello' + 123) # Example bug")

if st.button("Analyze Code") and code_input:
    if not api_key:
        st.error("Please enter your OpenAI API Key in the sidebar.")
    else:
        try:
            client = OpenAI(api_key=api_key)
            
            with st.spinner("Analyzing code..."):
                # 4. The AI Call with Structured Output
                completion = client.beta.chat.completions.parse(
                    model=model,
                    messages=[
                        {"role": "system", "content": "You are a professional debugging assistant. Analyze the code provided, identify the bug, and return a structured JSON response."},
                        {"role": "user", "content": code_input},
                    ],
                    response_format=DebugResult,
                )
                
                result = completion.choices[0].message.parsed

                # 5. Render Results in the UI
                st.subheader("🔍 Analysis Results")
                
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    st.error(f"**Error Type:** {result.error_type}")
                    st.warning(f"**Line Number:** {result.line_number}")
                    st.info(f"**Quick Fix:** {result.quick_fix}")
                
                with col2:
                    st.markdown("### 📝 Explanation")
                    st.write(result.explanation)
                    
                    st.markdown("### 🛠️ Suggested Fix")
                    st.code(result.fix_snippet, language="python")

        except Exception as e:
            st.error(f"An error occurred: {e}")

# 6. Footer
st.divider()
st.markdown("Built with Streamlit & OpenAI Structured Outputs")
