import argparse


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Git 변경 사항을 분석하여 커밋 메시지와 PR 초안을 생성합니다."
    )

    parser.add_argument(
        "command",
        choices=["commit", "pr"],
    )

    parser.add_argument(
        "--model",
        default="gpt-5.6-luna",
    )

    parser.add_argument(
        "--temperature",
        type=float,
        default=0.3,
    )

    parser.add_argument(
        "--max-tokens",
        type=int,
        default=500,
    )

    return parser


def main() -> None:
    parser = create_parser()
    args = parser.parse_args()

    print(args)
