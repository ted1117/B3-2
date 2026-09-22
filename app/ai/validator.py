def validate_commit_message(text: str) -> list[str]:
    errors = []

    title = text.splitlines()[0] if text else ""

    if len(title) > 72:
        errors.append("커밋 제목은 72자를 넘을 수 없습니다.")

    return errors


def validate_pr_draft(text: str) -> list[str]:
    errors = []

    required_sections = [
        "## Why",
        "## What",
        "## How to Test",
    ]

    for section in required_sections:
        if section not in text:
            errors.append(f"필수 섹션이 없습니다: {section}")

    return errors
