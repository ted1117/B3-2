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

            print(f"[INFO] Git status 수집 완료: " f"{changed_files}개 파일 변경 감지")
            print(f"[INFO] Git diff 수집 완료: " f"{diff_lines}줄")

        case "pr":
            status = repository.get_status()
            diff = repository.get_diff()

            if not diff.strip():
                print(
                    "[INFO] develop 브랜치와의 변경 사항이 없습니다. "
                    "PR 초안을 생성하지 않고 종료합니다."
                )
                return

            diff_lines = len(diff.splitlines())

            print(f"[INFO] PR 변경 사항 수집 완료: " f"{diff_lines}줄")

    if args.safe_mode:
        status = mask_sensitive_data(status)
        diff = mask_sensitive_data(diff)
        print("[INFO] Safe Mode 적용: 민감정보를 마스킹했습니다.")

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
