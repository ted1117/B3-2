import argparse


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

    parser.add_argument(
        "--safe-mode",
        action="store_true",
        help="API Key와 이메일 등 민감정보를 마스킹하여 전송",
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
