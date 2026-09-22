from app.ai.validator import validate_commit_message, validate_pr_draft

from app.ai.client import create_ai_client
from app.ai.prompts import build_prompt
from app.cli import create_parser
from app.git_repository import GitRepository
from app.sanitizer import mask_sensitive_data


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

    print("[INFO] AI API 요청 중...")

    result = client.generate(prompt)

    match args.command:
        case "commit":
            errors = validate_commit_message(result)

            if errors:
                print("[ERROR] 생성된 커밋 메시지가 형식 규칙을 만족하지 않습니다.")
                for error in errors:
                    print(f"- {error}")
                return

            print("[DONE] 커밋 메시지 생성 완료")
            print()
            print("--- Commit Message ---")
            print(result)
            print("----------------------")

        case "pr":
            errors = validate_pr_draft(result)

            if errors:
                print("[ERROR] 생성된 PR 초안이 형식 규칙을 만족하지 않습니다.")
                for error in errors:
                    print(f"- {error}")
                return

            print("[DONE] PR 초안 생성 완료")
            print()
            print(result)


if __name__ == "__main__":
    main()
