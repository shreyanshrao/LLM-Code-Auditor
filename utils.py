import streamlit as st
import os
import tempfile
import openai
from pathlib import Path
from dotenv import load_dotenv
import subprocess
import re

# Load OpenAI API key from .env file
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = api_key


st.set_page_config(page_title="OpenAI Code Generator", layout="centered")
st.title("🧠 OpenAI-Powered Code Generator")
st.markdown("Upload your 4 input documents to generate and iteratively improve your code.")

uploaded_files = st.file_uploader("📂 Upload 4 files (Requirement, User Story, DB, Architecture)", type=["txt", "md", "docx"], accept_multiple_files=True)

if "attempt" not in st.session_state:
    st.session_state.attempt = 1
if "final_code" not in st.session_state:
    st.session_state.final_code = ""
if "feedback_given" not in st.session_state:
    st.session_state.feedback_given = False

def read_uploaded_files(files):
    content = ""
    for file in files:
        content += f"\n### {file.name}\n"
        content += file.read().decode("utf-8", errors="ignore") + "\n"
    return content

def call_openai(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4o",  # or gpt-3.5-turbo
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    text = response['choices'][0]['message'].get('content')
    if text:
        code = extract_python_code(text)
    else:
      st.error("No code was returned from OpenAI.")


def extract_python_code(text):
    if text is None:
        return ""  # or raise an error / return a default value
    match = re.findall(r"```(?:python)?\n(.*?)```", text, re.DOTALL)
    return match[0] if match else ""


def run_pylint(file_path):
    try:
        result = subprocess.run(
            ['pylint', file_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False  # Don’t raise exception on non-zero exit
        )
        output = result.stdout
        print("Pylint Output:\n", output)  # Debug print

        # Extract the score using regex
        match = re.search(r"Your code has been rated at ([\d\.]+)/10", output)
        if match:
            return float(match.group(1))
        else:
            return 0.0  # No score found
    except Exception as e:
        print(f"Error running pylint: {e}")
        return 0.0

def run_pytest(file_path):
    try:
        result = subprocess.run(["pytest", file_path], capture_output=True, text=True)
        return "failed" not in result.stdout.lower()
    except Exception:
        return False

def save_code(code:str, version:int):
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    file_path = output_dir / f"code_v{version}.py"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(code)
    print(f"[Saved] Code v{version} -> {file_path}")
    return file_path

if st.button("🚀 Generate and Evaluate Code") and len(uploaded_files) == 4:
    file_content = read_uploaded_files(uploaded_files)

    while st.session_state.attempt <= 3:
        with st.spinner(f"🔁 Attempt {st.session_state.attempt}: Generating code..."):
            prompt = f"Generate production-quality Python code based on these documents:\n\n{file_content}"
            if st.session_state.attempt > 1:
                prompt += "\n\n# Note: Fix previous issues with pylint or tests."

            response = call_openai(prompt)
            code = extract_python_code(response)

            with tempfile.NamedTemporaryFile(delete=False, suffix=".py", mode="w", encoding="utf-8") as tmp:
                tmp.write(code)
                tmp_path = tmp.name

        pylint_score = run_pylint(tmp_path)
        pytest_passed = run_pytest(tmp_path)

        st.code(code, language="python")
        st.write(f"**🧪 Pytest Passed:** {'✅ Yes' if pytest_passed else '❌ No'}")
        st.write(f"**🔍 Pylint Score:** `{pylint_score}/10`")

        save_code(st.session_state.attempt, code)

        if pylint_score <= 8.0 or st.session_state.attempt == 3:
            feedback = st.radio("📣 Are you satisfied with the generated code?", ["Yes", "No"])
            if feedback == "Yes":
                Path("final_output.py").write_text(code, encoding="utf-8")
                st.success("✅ Final code saved as `final_output.py`")
                st.download_button("⬇ Download Code", code, file_name="final_output.py")
                break
            else:
                suggestion = st.text_area("💡 Suggest improvements:")
                if suggestion:
                    file_content += f"\n\n# Human Feedback: {suggestion}"
        else:
            st.session_state.attempt += 1
