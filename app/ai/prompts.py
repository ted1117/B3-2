from typing import Literal

PromptType = Literal["commit", "pr"]


def build_prompt(
    status: str,
    diff: str,
    prompt_type: PromptType,
) -> str:
    match prompt_type:
        case "commit":
            format_rules = """
- 출력에는 커밋 메시지 자체만 포함하세요.
- "커밋 메시지 초안:", "결과:", "아래와 같습니다." 등의 설명을 작성하지 마세요.
- Markdown 코드 블록(```)을 사용하지 마세요.
- 커밋 제목은 반드시 다음 형식을 따르세요:
  <type>: <한국어 설명>
- type은 변경 사항에 따라 다음 중 하나를 사용하세요.
  - feat: 새로운 기능
  - fix: 버그 수정
  - refactor: 기능 변경 없는 코드 개선
  - docs: 문서 변경
  - test: 테스트 코드 변경
  - chore: 설정, 의존성 등 기타 변경
- 제목은 가능하면 50자 이내로 작성하고 최대 72자를 넘지 마세요.
- 본문은 필요한 경우에만 작성하세요.
- 본문을 작성하는 경우 핵심 변경 사항을 1~3개의 bullet로 작성하세요.

출력 예시:

feat: AI 클라이언트 생성 기능 추가

- 모델에 따라 적절한 AI 클라이언트를 생성하도록 구현
- 환경변수에서 API Key를 가져오도록 구성
"""

        case "pr":
            format_rules = """
- 출력에는 PR 초안 자체만 포함하세요.
- "PR 초안:", "결과:", "아래와 같습니다." 등의 설명을 작성하지 마세요.
- Markdown 코드 블록(```)을 사용하지 마세요.
- 반드시 다음 형식으로 작성하세요.

--- PR Title ---
<PR 제목>

--- PR Body ---
## Why
- 변경이 필요한 이유

## What
- 변경한 내용

## How to Test
- 변경 사항을 테스트하는 방법

- PR 제목은 한 줄로 작성하고 80자를 넘지 마세요.
- PR 본문에는 반드시 Why, What, How to Test 섹션을 포함하세요.
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

[작성 규칙]
{format_rules}

중요:
- 모든 설명은 한국어로 작성하세요.
- 코드, 파일명, 클래스명, 함수명은 원래 표기를 유지하세요.
- 지정된 출력 형식을 정확히 따르세요.
- 초안 이외의 부가 설명은 절대 출력하지 마세요.
""".strip()
