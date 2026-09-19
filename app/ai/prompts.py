from typing import Literal

PromptType = Literal["commit", "pr"]


def build_prompt(status: str, diff: str, prompt_type: PromptType) -> str:
    match prompt_type:
        case "commit":
            format_rules = """
- 커밋 제목은 다음 형식을 따르세요: <type>: <한국어 설명>
- type은 다음 중 변경 사항에 적절한 것을 사용하세요.
  - feat: 새로운 기능
  - fix: 버그 수정
  - refactor: 기능 변경 없는 코드 개선
  - docs: 문서 변경
  - test: 테스트 코드 변경
  - chore: 설정, 의존성 등 기타 변경
- 예시: feat: AI 프롬프트 생성 기능 추가
- 제목은 가능하면 50자 이내로 작성하고, 최대 72자를 넘지 마세요.
"""

        case "pr":
            format_rules = """
- PR 제목은 한 줄로 작성하고 80자를 넘지 마세요.
- 본문에는 반드시 다음 섹션을 포함하세요.
  ## Why
  ## What
  ## How to Test
- 각 섹션에는 최소 하나 이상의 bullet 항목을 작성하세요.
"""

        case _:
            raise ValueError(f"지원하지 않는 프롬프트 유형입니다: {prompt_type}")

    return f"""
아래 Git 변경 사항을 분석하여 {prompt_type} 초안을 작성하세요.

[Git Status]
{status}

[Git Diff]
{diff}

작성 규칙:
{format_rules}
- 모든 설명은 한국어로 작성하세요.
- 코드, 파일명, 클래스명, 함수명 등은 원래 표기를 유지하세요.
- 초안 이외의 설명은 작성하지 마세요.
""".strip()
