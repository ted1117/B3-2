import httpx

from app.ai.client import AIClient, create_ai_client
from app.ai.prompts import build_prompt
from app.ai.validator import validate_commit_message, validate_pr_draft
from app.cli import create_parser
from app.git_repository import GitRepository
from app.sanitizer import mask_sensitive_data


def request_ai(client: AIClient, prompt: str) -> str | None:
    try:
        return client.generate(prompt)

    except httpx.TimeoutException:
        print("[ERROR] AI API 요청 시간이 초과되었습니다.")

    except httpx.HTTPStatusError as error:
        status_code = error.response.status_code

        if status_code in (401, 403):
            print("[ERROR] AI API 인증에 실패했습니다. API Key를 확인하세요.")
        else:
            print(f"[ERROR] AI API 요청에 실패했습니다. HTTP {status_code}")

    except httpx.RequestError as error:
        print(f"[ERROR] AI API 서버 연결에 실패했습니다: {error}")

    except (KeyError, IndexError, TypeError, ValueError):
        print("[ERROR] AI API 응답을 처리할 수 없습니다.")

    return None


def main() -> None:
    parser = create_parser()
    args = parser.parse_args()

    repository = GitRepository()

    match args.command:
        case "commit":
            if not repository.has_changes():
                print(
                    "[INFO] 변경 사항이 없습니다. "
                    "커밋 메시지를 생성하지 않고 종료합니다."
                )
                return

            status = repository.get_status()
            diff = repository.get_diff()

            changed_files = len(status.splitlines())
            diff_lines = len(diff.splitlines())

            print(f"[INFO] Git status 수집 완료: {changed_files}개 파일 변경 감지")
            print(f"[INFO] Git diff 수집 완료: {diff_lines}줄")

        case "pr":
            status = repository.get_status()
            diff = repository.get_pr_diff()

            if not diff.strip():
                print(
                    "[INFO] develop 브랜치와의 변경 사항이 없습니다. "
                    "PR 초안을 생성하지 않고 종료합니다."
                )
                return

            diff_lines = len(diff.splitlines())

            print(f"[INFO] PR 변경 사항 수집 완료: {diff_lines}줄")

    if args.safe_mode:
        status, status_emails, status_keys = mask_sensitive_data(status)
        diff, diff_emails, diff_keys = mask_sensitive_data(diff)

        email_count = status_emails + diff_emails
        api_key_count = status_keys + diff_keys

        print("[INFO] Safe Mode 활성화")
        print(
            f"[INFO] 민감정보 마스킹 완료: "
            f"이메일 {email_count}건, "
            f"API Key {api_key_count}건"
        )

    prompt = build_prompt(
        status=status,
        diff=diff,
        prompt_type=args.command,
    )

    try:
        client = create_ai_client(
            model=args.model,
            temperature=args.temperature,
            max_tokens=args.max_tokens,
        )
    except ValueError as error:
        print(f"[ERROR] {error}")
        return

    match args.command:
        case "commit":
            validator = validate_commit_message
        case "pr":
            validator = validate_pr_draft

    print("[INFO] AI API 요청 중...")

    result = request_ai(client, prompt)

    if result is None:
        return

    errors = validator(result)

    if errors:
        print("[WARN] 생성 결과가 형식 규칙을 만족하지 않습니다.")

        for error in errors:
            print(f"- {error}")

        print("[INFO] 형식 오류를 수정하기 위해 1회 재생성합니다.")

        retry_prompt = (
            f"{prompt}\n\n"
            "[이전 생성 결과의 형식 오류]\n"
            + "\n".join(f"- {error}" for error in errors)
            + "\n위 오류를 모두 수정하여 다시 생성하세요."
        )

        result = request_ai(client, retry_prompt)

        if result is None:
            return

        errors = validator(result)

        if errors:
            print("[ERROR] 재생성된 결과도 형식 규칙을 만족하지 않습니다.")

            for error in errors:
                print(f"- {error}")

            return

    match args.command:
        case "commit":
            print("[DONE] 커밋 메시지 생성 완료")
            print()
            print("--- Commit Message ---")
            print(result)
            print("----------------------")

        case "pr":
            print("[DONE] PR 초안 생성 완료")
            print()
            print(result)


if __name__ == "__main__":
    main()
