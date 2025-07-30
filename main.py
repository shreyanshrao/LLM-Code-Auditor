import streamlit as st
import os
import tempfile
import openai
from pathlib import Path
import subprocess
import re
from dotenv import load_dotenv

# Load OpenAI API key from .env or env variable
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = api_key

st.set_page_config(page_title="OpenAI Code Generator", layout="centered")
st.title("🧠 OpenAI-Powered Code Generator")
st.markdown("Upload your 4 input documents to generate and iteratively improve your code with PyLint and Pytest feedback.")

def read_uploaded_files(files):
    content = ""
    for file in files:
        content += f"\n### {file.name}\n"
        content += file.read().decode("utf-8", errors="ignore") + "\n"
    return content

def call_openai(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )
    text = response['choices'][0]['message'].get('content')
    return text
def extract_python_code(text):
    blocks = re.findall(r"```python(.*?)```", text, re.DOTALL)
    return "\n\n".join(blocks).strip() if blocks else text.strip()

def run_pylint(file_path):
    result = subprocess.run(
        ['pylint', file_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )
    output = result.stdout
    match = re.search(r"Your code has been rated at ([\d\.]+)/10", output)
    score = float(match.group(1)) if match else 0.0
    return score, output

def run_pytest(file_path):
    result = subprocess.run(
        ["pytest", file_path, "--tb=short", "--disable-warnings"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return "failed" not in result.stdout.lower(), result.stdout

def save_code(code: str, version: int):
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    file_path = output_dir / f"code_v{version}.py"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(code)
    return file_path

uploaded_files = st.file_uploader(
    "📂 Upload exactly 4 files (Requirement, User Story, Database, Architecture)",
    type=["txt", "md", "docx"],
    accept_multiple_files=True
)

if uploaded_files and len(uploaded_files) == 4:
    file_content = read_uploaded_files(uploaded_files)
    if st.button("🚀 Generate and Evaluate Code"):
        feedback = ""
        for attempt in range(1, 4):
            st.write(f"## Attempt {attempt}")
            # Compose prompt with all previous feedback
            prompt = f"Generate production-quality Python code based on these documents:\n\n{file_content}"
            if feedback:
                prompt += f"\n# Human feedback from previous iteration:\n{feedback}"

            with st.spinner("Generating code..."):
                response_text = call_openai(prompt)
            code = extract_python_code(response_text)
            code_path = save_code(code, attempt)

            pylint_score, pylint_output = run_pylint(str(code_path))
            pytest_passed, pytest_output = run_pytest(str(code_path))

            st.code(code, language="python")
            st.write(f"**🧪 Pytest Passed:** {'✅ Yes' if pytest_passed else '❌ No'}")
            st.write(f"**🔍 Pylint Score:** `{pylint_score}/10`")
            with st.expander("See full PyLint output"):
                st.text(pylint_output)
            with st.expander("See full Pytest output"):
                st.text(pytest_output)

            # If code passes and score is sufficient, break
            if pylint_score >= 8.0 and pytest_passed:
                st.success(f"Perfect! Code meets quality checks after {attempt} attempt(s).")
                Path("final_output.py").write_text(code, encoding="utf-8")
                st.download_button("⬇ Download Final Code", code, file_name="final_output.py")
                break
            elif attempt == 3:
                st.warning("All attempts completed. Please enter feedback for further improvement below.")
                st.session_state.generated_code = code
                break

        # Feedback UI after auto attempts
        if 'generated_code' in st.session_state:
            user_feedback = st.text_area(
                "💡 Suggest further improvements or requirements for the code:",
                value="", key="feedback"
            )
            
            if st.button("Submit Feedback"):
                st.session_state.feedback = user_feedback
                st.info("Your feedback has been saved. Re-run to generate a new version using your feedback.")
if 'generated_code' in st.session_state:
    user_feedback = st.text_area(
        "💡 Suggest further improvements or requirements for the code:",
        value="", key="feedback"
    )
    
    if st.button("Submit Feedback"):
        st.session_state.feedback = user_feedback
        st.info("Your feedback has been saved. Re-run to generate a new version using your feedback.")
    
    if "waiting_for_feedback" not in st.session_state:
        st.session_state.waiting_for_feedback = False
    if "human_decision" not in st.session_state:
        st.session_state.human_decision = None
    if "human_feedback" not in st.session_state:
        st.session_state.human_feedback = ""

else:
    st.info("Please upload exactly 4 files to enable code generation.")

else:
    st.info("Please upload exactly 4 files to enable code generation.")
