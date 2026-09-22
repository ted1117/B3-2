def validate_commit_message(text: str) -> list[str]:
    errors = []

    lines = text.strip().splitlines()

    if not lines:
        errors.append("커밋 제목이 없습니다.")
        return errors

    title = lines[0].strip()

    if not title:
        errors.append("커밋 제목이 없습니다.")

    # 커밋 제목은 72자를 넘길 수 없음
    if len(title) > 72:
        errors.append("커밋 제목은 72자를 넘을 수 없습니다.")

    return errors


def validate_pr_draft(text: str) -> list[str]:
    errors = []

    lines = text.strip().splitlines()

    title_header = "--- PR Title ---"
    body_header = "--- PR Body ---"

    # PR 제목 구분선 존재 확인
    if title_header not in lines:
        errors.append("PR Title 헤더가 없습니다.")
    else:
        title_index = lines.index(title_header)

        # 제목 헤더 다음 주에 제목이 존재하는지 확인
        if title_index + 1 >= len(lines):
            errors.append("PR 제목이 없습니다.")
        else:
            title = lines[title_index + 1].strip()

            if not title:
                errors.append("PR 제목이 없습니다.")
            elif len(title) > 80:
                errors.append("PR 제목은 80자를 넘을 수 없습니다.")

    if body_header not in lines:
        errors.append("PR Body 헤더가 없습니다.")

    required_sections = [
        "## Why",
        "## What",
        "## How to Test",
    ]

    for index, section in enumerate(required_sections):
        if section not in lines:
            errors.append(f"필수 섹션이 없습니다: {section}")
            continue

        section_index = lines.index(section)

        if index + 1 < len(required_sections):
            next_section = required_sections[index + 1]

            if next_section in lines:
                next_index = lines.index(next_section)
            else:
                next_index = len(lines)
        else:
            next_index = len(lines)

        # 섹션 내용 추출
        section_content = lines[section_index + 1 : next_index]

        # 각 섹션마다 '----'가 있어야 함
        has_bullet = any(line.strip().startswith("- ") for line in section_content)

        if not has_bullet:
            errors.append(f"{section} 섹션에는 최소 1개의 불릿이 필요합니다.")

    return errors
