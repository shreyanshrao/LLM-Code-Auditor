# 🧠 LLM Code Auditor

An automated pipeline that transforms software requirements into code, tests it, analyzes quality, and generates an intelligent LLM-based feedback report.

## 🚀 Overview

This project simulates a **mini software development lifecycle**. Given a set of software requirements, it:
1. Converts them into user stories.
2. Designs modules and database schemas.
3. Auto-generates executable Python code.
4. Runs tests using `pytest` and performs static analysis with `pylint`.
5. Generates an LLM-based feedback report evaluating code quality and test coverage.

## 🛠️ Technologies Used

- Python 3.10+
- `pytest` – for test case execution
- `pylint` – for static code analysis
- `openai` – for LLM-based review and feedback
- OS & subprocess – to automate code execution

---

## 📁 Folder Structure

LLM-Code-Auditor/
│
├── requirements/ # Raw requirement and user story files
│ ├── requirement.txt
│ └── user_stories.txt
│
├── design/ # Design documents
│ ├── module_design.txt
│ └── db_design.txt
│
├── src/ # Auto-generated source code
│ └── module_code.py
│
├── tests/ # Test cases for modules
│ └── test_module_code.py
│
├── reports/ # Auto-generated reports
│ ├── pylint_report.txt
│ ├── test_results.txt
│ └── llm_feedback.txt
│
├── generate_code.py # Converts designs into source code
├── run_tests.py # Executes test cases and saves output
├── run_pylint.py # Executes pylint and saves output
├── generate_feedback.py # Generates LLM feedback from test + lint
└── README.md # Project explanation
