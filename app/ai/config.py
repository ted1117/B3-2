import os
from dataclasses import dataclass, field
from typing import Self


@dataclass(frozen=True)
class AIConfig:
    api_key: str = field(repr=False)
    model: str = "gpt-5.6-luna"
    temperature: float = 0.3
    max_tokens: int = 500

    @classmethod
    def from_env(
        cls,
        env_name: str,
        *,
        model: str = "gpt-5.6-luna",
        temperature: float = 0.3,
        max_tokens: int = 500,
    ) -> Self:
        api_key = os.getenv(env_name)

        if not api_key:
            raise ValueError(f"{env_name} 환경변수가 설정되지 않았습니다.")

        return cls(
            api_key=api_key,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
        )
