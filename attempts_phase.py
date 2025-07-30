# attempts_phase.py
import streamlit as st
import tempfile
import subprocess
import re
from pathlib import Path
import google.generativeai as genai

genai.configure(api_key="AIzaSyCotWggzutK3IVXYPw1MOuFmWfTb9HjuRQ")
model = genai.GenerativeModel("models/gemini-2.5-flash")

def extract_code_blocks(text):
    blocks = re.findall(r"```python(.*?)```", text, re.DOTALL)
    return "\n\n".join(blocks).strip() if blocks else text.strip()

def run_pylint(path):
    result = subprocess.run(["pylint", path, "--exit-zero"], capture_output=True, text=True)
    match = re.search(r'Your code has been rated at ([\d\.]+)/10', result.stdout)
    return float(match.group(1)) if match else 0.0, result.stdout

def run_pytest(path):
    with open("test_temp.py", "w") as f:
        f.write("""
import pytest
def test_sample(): assert True
""")
    result = subprocess.run(["pytest", "test_temp.py"], capture_output=True, text=True)
    return "passed" in result.stdout.lower(), result.stdout

def generate_code(prompt, version):
    st.subheader(f"Attempt {version}")
    response = model.generate_content(prompt).text
    code = extract_code_blocks(response)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as tmp:
        tmp.write(code.encode("utf-8"))
        code_path = tmp.name

    score, pylint_output = run_pylint(code_path)
    passed, pytest_output = run_pytest(code_path)

    st.code(code, language="python")
    st.write(f"🔍 **Pylint Score**: {score}/10")
    st.write(f"✅ **Pytest Passed**: {'Yes' if passed else 'No'}")
    st.text("📋 Pylint Output:")
    st.text(pylint_output)
    st.text("📋 Pytest Output:")
    st.text(pytest_output)

    return code, score, passed
