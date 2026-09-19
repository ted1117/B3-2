import argparse

from app.ai.client import create_ai_client
from app.ai.prompts import build_prompt
from app.git_repository import GitRepository


def temperature_type(value: str) -> float:
    temperature = float(value)

    if not 0 <= temperature <= 2:
        raise argparse.ArgumentTypeError("temperature는 0~2 사이여야 합니다.")

    return temperature


def max_tokens_type(value: str) -> int:
    max_tokens = int(value)

    if not 1 <= max_tokens <= 32_768:
        raise argparse.ArgumentTypeError("max_tokens는 1~32768 사이여야 합니다.")

    return max_tokens


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=("Git 변경 사항을 분석하여 " "커밋 메시지와 PR 초안을 생성합니다.")
    )

    parser.add_argument(
        "command",
        choices=["commit", "pr"],
        help="생성할 초안 종류",
    )

    parser.add_argument(
        "--model",
        choices=[
            "gpt-4.1-nano",
            "gpt-5.4-mini",
        ],
        default="gpt-4.1-nano",
        help="사용할 AI 모델",
    )

    parser.add_argument(
        "--temperature",
        type=temperature_type,
        default=0.3,
        help="AI 응답의 temperature 값 (0~2)",
    )

    parser.add_argument(
        "--max-tokens",
        type=max_tokens_type,
        default=500,
        help="AI 응답의 최대 토큰 수 (1~32768)",
    )

    return parser


def print_commit_result(result: str) -> None:
    print("[DONE] 커밋 메시지 생성 완료")
    print()
    print("--- Commit Message ---")
    print(result)
    print("----------------------")


def print_pr_result(result: str) -> None:
    print("[DONE] PR 초안 생성 완료")
    print()
    print(result)


def main() -> None:
    parser = create_parser()
    args = parser.parse_args()

    repository = GitRepository()

    if not repository.has_changes():
        print("[INFO] 변경 사항이 없습니다. " "초안을 생성하지 않고 종료합니다.")
        return

    status = repository.get_status()
    diff = repository.get_diff()

    changed_files = len(status.splitlines())
    diff_lines = len(diff.splitlines())

    print(f"[INFO] Git status 수집 완료: " f"{changed_files}개 파일 변경 감지")
    print(f"[INFO] Git diff 수집 완료: " f"{diff_lines}줄")

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
            print_commit_result(result)

        case "pr":
            print_pr_result(result)
