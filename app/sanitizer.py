import re


def mask_sensitive_data(text: str) -> tuple[str, int, int]:
    email_pattern = r"\b[A-Za-z0-9._%+-]+@" r"[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
    api_key_pattern = r"\bsk-[A-Za-z0-9_-]+\b"

    text, email_count = re.subn(
        email_pattern,
        "*****@*****.***",
        text,
    )

    text, api_key_count = re.subn(
        api_key_pattern,
        "*****",
        text,
    )

    return text, email_count, api_key_count
