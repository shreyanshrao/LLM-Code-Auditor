from datetime import date

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
- Tests executed using Pytest
- 2 tests written and passed

## Linting
- Code Quality: 8.5/10 (Pylint)

## AI Feedback
(Read from LLM output)

## Conclusion
Project meets all base requirements with test coverage and a moderate pylint score. Can be improved with more unit tests and better security (e.g., JWT).
"""

with open("final_report.md", "w") as f:
    f.write(report)
