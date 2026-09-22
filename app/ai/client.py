from typing import Protocol

import httpx

from app.ai.config import AIConfig


class AIClient(Protocol):
    """AI 클라이언트 인터페이스"""

    def generate(self, prompt: str) -> str:
        """AI에 프롬프트를 전달하고 생성된 텍스트를 반환"""
        ...


class OpenAIClient:
    BASE_URL = "https://api.openai.com/v1/responses"

    def __init__(self, config: AIConfig):
        self._config = config

    def generate(self, prompt: str) -> str:
        headers = {
            "Authorization": f"Bearer {self._config.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": self._config.model,
            "input": prompt,
            "temperature": self._config.temperature,
            "max_output_tokens": self._config.max_tokens,
        }

        response = httpx.post(
            self.BASE_URL,
            headers=headers,
            json=payload,
            timeout=30.0,
        )

        response.raise_for_status()

        data = response.json()

        texts = []

        for output in data.get("output", []):
            if output.get("type") != "message":
                continue

            for content in output.get("content", []):
                if content.get("type") == "output_text":
                    texts.append(content["text"])

        return "\n".join(texts)


class CodysseyAIClient:
    BASE_URL = "https://copa.codyssey.kr/v1/chat/completions"

    def __init__(self, config: AIConfig):
        self._config = config

    def generate(self, prompt: str) -> str:
        headers = {"Authorization": f"Bearer {self._config.api_key}"}
        payload = {
            "model": self._config.model,
            "messages": [{"role": "user", "content": prompt}],
            "max_completion_tokens": self._config.max_tokens,
        }

        response = httpx.post(
            self.BASE_URL,
            headers=headers,
            json=payload,
            timeout=30.0,
        )

        response.raise_for_status()

        output = response.json()["choices"][0]["message"]["content"]

        return output


def create_ai_client(
    model: str,
    temperature: float,
    max_tokens: int,
) -> AIClient:
    match model:
        case "gpt-4.1-nano":
            config = AIConfig.from_env(
                "OPENAI_API_KEY",
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            return OpenAIClient(config)

        case "gpt-5.4-mini":
            config = AIConfig.from_env(
                "CODYSSEY_API_KEY",
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            return CodysseyAIClient(config)

        case _:
            raise ValueError(f"지원하지 않는 모델입니다: {model}")
