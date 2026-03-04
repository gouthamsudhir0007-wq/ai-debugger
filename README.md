🤖 LogicAI: Intelligent Python Debugger
A student-built diagnostic tool designed to bridge the gap between static code analysis and developer intent.
🔍 Overview
Standard compilers often provide intimidating or vague error messages. LogicAI was created to provide a human-centric approach to debugging, specifically focusing on logical inconsistencies and naming typos that often trip up learners.
🛠️ Key Features
• Fuzzy Naming Logic: Cross-references defined variables to catch typos (e.g., usr_age vs user_age).
• Syntax & Logic Audits: Automatically detects missing colons, unclosed parentheses, and assignment errors (= vs ==).
• Structured Feedback: Generates diagnostic cards with line-by-line explanations and suggested fixes.
• Teal Enterprise UI: A clean, responsive interface built with Streamlit.
🚀 Tech Stack
• Language: Python
• Frontend: Streamlit
• Pattern Matching: Regex & Difflib
📖 How to Run
1. Clone this repository.
2. Install dependencies: pip install streamlit.
3. Run the app: streamlit run app.py.
