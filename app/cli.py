import argparse

from app.ai.client import create_ai_client
from app.ai.prompts import build_prompt
from app.git_repository import GitRepository


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
        default="gpt-4.1-nano",
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

    repository = GitRepository()

    if not repository.has_changes():
        print("변경 사항이 없습니다.")
        return

    status = repository.get_status()
    diff = repository.get_diff()

    prompt = build_prompt(
        status=status,
        diff=diff,
        prompt_type=args.command,
    )

    client = create_ai_client(
        model=args.model,
        temperature=args.temperature,
        max_tokens=args.max_tokens,
    )

    result = client.generate(prompt)

    print(result)
