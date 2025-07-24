from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
def load_file_content(file_path):
    with open(file_path, 'r') as f:
        return f.read()

def generate_llm_feedback(pylint_text, test_results_text):
    prompt = f"""
You are a software quality reviewer.

Based on the following:

1. 🔍 Pylint Report:
{pylint_text}

2. ✅ Pytest Results:
{test_results_text}

Please provide a detailed quality review covering:

- Code structure and readability
- Testing completeness and edge case handling
- Suggestions for improvement (naming, logic, design)
- Summary score out of 10

Thank you!
"""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an expert Python code reviewer."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4,
        max_tokens=1000
    )

    return response.choices[0].message.content

if __name__ == "__main__":
    pylint_report = load_file_content("pylint_report.txt")
    test_results = load_file_content("test_results.txt")

    feedback = generate_llm_feedback(pylint_report, test_results)

    with open("llm_feedback.txt", "w") as f:
        f.write(feedback)

    print("✅ LLM Feedback saved to llm_feedback.txt")
