import re


def mask_sensitive_data(text: str) -> str:
    """민감정보를 마스킹하여 반환합니다."""

    # 이메일 주소 마스킹
    text = re.sub(
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
        "*****@*****.***",
        text,
    )

    # sk-로 시작하는 API Key 마스킹
    text = re.sub(
        r"\bsk-[A-Za-z0-9_-]+\b",
        "*****",
        text,
    )

    return text
