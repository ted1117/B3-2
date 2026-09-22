# 내가 고친 코드 설명을 AI가 대신 써주는 도우미

Git 변경 사항을 분석하여 AI API를 통해 커밋 메시지와 PR 초안을 생성하는 CLI 프로그램입니다.

## 설치 및 실행

Python 3.10 이상이 필요합니다.

`uv`를 사용하여 의존성을 설치합니다.

```bash
uv sync
```

프로그램은 Git 저장소의 루트에서 실행합니다.

```bash
uv run main.py --help
```

## API Key 및 지원 모델

현재 다음 두 모델을 지원합니다.

| 모델 | API 제공자 | 필요한 환경변수 |
| --- | --- | --- |
| `gpt-4.1-nano` | OpenAI | `OPENAI_API_KEY` |
| `gpt-5.4-mini` | Codyssey | `CODYSSEY_API_KEY` |

기본 모델은 `gpt-4.1-nano`입니다.

사용하려는 모델에 맞는 API Key를 환경변수로 설정해야 합니다.

## API Key 설정

사용할 AI 모델에 따라 API Key를 환경변수로 설정합니다.

### OpenAI

```bash
export OPENAI_API_KEY="YOUR_API_KEY"
```

### Codyssey

```bash
export CODYSSEY_API_KEY="YOUR_API_KEY"
```

## 사용 방법

### 커밋 메시지 생성

현재 Git working tree의 변경 사항을 분석하여 커밋 메시지 초안을 생성합니다.

```bash
uv run main.py commit
```

모델, temperature, max token 값을 지정할 수도 있습니다.

```bash
uv run main.py commit \
  --model gpt-4.1-nano \
  --temperature 0.3 \
  --max-tokens 500
```

Codyssey 모델을 사용하는 경우:

```bash
uv run main.py commit \
  --model gpt-5.4-mini \
  --temperature 0.3 \
  --max-tokens 500
```

### PR 초안 생성

`develop` 브랜치와 현재 브랜치의 변경 사항을 분석하여 PR 초안을 생성합니다.

```bash
uv run main.py pr
```

옵션을 지정할 수도 있습니다.

```bash
uv run main.py pr \
  --model gpt-4.1-nano \
  --temperature 0.3 \
  --max-tokens 500
```

Codyssey 모델을 사용하는 경우:

```bash
uv run main.py pr \
  --model gpt-5.4-mini \
  --temperature 0.3 \
  --max-tokens 500
```

## Safe Mode

Git 변경 사항에는 이메일이나 API Key 등의 민감정보가 포함될 수 있습니다.

`--safe-mode` 옵션을 사용하면 지원되는 민감정보를 마스킹한 후 AI API에 전달합니다.

```bash
uv run main.py commit --safe-mode
```

PR 생성에도 사용할 수 있습니다.

```bash
uv run main.py pr --safe-mode
```

현재 Safe Mode에서는 다음 정보를 마스킹합니다.

- 이메일 주소
- `sk-`로 시작하는 API Key

예:

```text
developer@example.com
→ *****@*****.***

sk-example-api-key
→ *****
```

민감정보가 포함될 가능성이 있는 경우 `--safe-mode` 옵션 사용을 권장합니다.

## 커밋 메시지 출력 예시

```text
[INFO] Git status 수집 완료: 2개 파일 변경 감지
[INFO] Git diff 수집 완료: 42줄
[INFO] AI API 요청 중...
[DONE] 커밋 메시지 생성 완료

--- Commit Message ---
feat: Safe Mode 기능 추가

- Git 변경 사항에 포함된 이메일 주소를 마스킹
- API Key를 마스킹한 후 AI API에 전달
----------------------
```

## PR 출력 예시

```text
[INFO] PR 변경 사항 수집 완료: 85줄
[INFO] AI API 요청 중...
[DONE] PR 초안 생성 완료

--- PR Title ---
feat: Safe Mode 기능 추가

--- PR Body ---
## Why
- Git 변경 사항에 민감정보가 포함될 가능성이 있습니다.

## What
- 이메일 주소 마스킹 기능을 추가했습니다.
- API Key 마스킹 기능을 추가했습니다.

## How to Test
- --safe-mode 옵션으로 실행하여 민감정보가 마스킹되는지 확인합니다.
```

## 주의사항

AI가 생성한 커밋 메시지와 PR 내용은 초안입니다.

실제 Git 작업에 적용하기 전에 생성된 내용을 직접 확인해야 합니다.