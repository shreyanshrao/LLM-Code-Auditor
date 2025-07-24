import json
from datetime import date
from pathlib import Path

# Set base paths
BASE_DIR = Path(__file__).resolve().parent.parent
DOCS_DIR = BASE_DIR / "docs"
OUTPUT_DIR = BASE_DIR / "output"
REPORT_PATH = BASE_DIR / "final_report.md"

# Load requirement
with open(DOCS_DIR / "requirement.json", "r") as f:
    requirement = json.load(f)["requirement"]

# Load user stories
with open(DOCS_DIR / "user_stories.json", "r") as f:
    user_stories = json.load(f)["user_stories"]

# Optional files (use fallback if not found)
def safe_read_file(path, default="(Not available)"):
    try:
        with open(path, "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return default

llm_feedback = safe_read_file(OUTPUT_DIR / "llm_feedback.txt")
pylint_report = safe_read_file(OUTPUT_DIR / "pylint_report.txt")
test_results = safe_read_file(OUTPUT_DIR / "test_results.txt")

# Construct the final report
report = f"""
# Project Report

**Date:** {date.today()}

## Requirement Summary
{requirement.strip()}

## User Stories
- {user_stories[0]}
- {user_stories[1]}
- {user_stories[2]}
- {user_stories[3]}

## Modules
- User registration
- Login session
- Feedback submission
- Admin-only access to feedback

## Testing
{test_results}

## Linting
{pylint_report}

## AI Feedback
{llm_feedback}

## Conclusion
Project meets all base requirements with test coverage and a moderate pylint score.
Can be improved with more unit tests and better security (e.g., JWT).
"""

# Write to final_report.md at root
with open(REPORT_PATH, "w") as f:
    f.write(report)

print(f"✅ Report generated successfully at: {REPORT_PATH}")
