---
title: OpenViking 개요
created: 2026-08-19
updated: 2026-08-21
type: entity
status: active
tags: [AI/ML, 도구, 개발]
sources: []
---

# OpenViking 개요

> **판단**: Hermes 공식 파트너이고 LoCoMo 개선폭(33% → 83%)이 크다. 다만 이 PC에서는
> Windows Store Python 문제로 **uv venv 우회가 필요**했고, 로컬 올라마 구성에 모델 ~5GB가 든다.
> 라이선스가 **AGPLv3**(메인)라는 점도 쓰기 전에 고려할 것.
> **다음**: [[projects/llm/openviking/HANDOFF|HANDOFF]]의 테스트 상태를 보고 이어서 검증한다.

> AI 에이전트용 **컨텍스트 데이터베이스**. ByteDance(volcengine)가 만든 오픈소스.
> 에이전트의 메모리·리소스·스킬을 하나의 가상 파일시스템(`viking://`)으로 관리한다.

## 이게 뭔가

- **`viking://` 프로토콜** — 컨텍스트를 파일처럼 다룸. 에이전트가 벡터 DB를 블랙박스로 쓰는 대신 `ls`, `tree`, `find`로 자기 컨텍스트를 탐색
- **3단계 계층 로딩 (L0/L1/L2)** — 요약 → 개요 → 상세. 필요한 깊이만 로드해서 **토큰 절약**
- **디렉터리 재귀 검색** — 벡터 검색으로 최적 디렉터리를 찾고 계층별로 드릴다운
- **세션이 메모리가 됨** — 세션 커밋 후 사용자 선호/에이전트 경험을 비동기 추출해 장기 메모리로

## 기술 스택

| 구성 | 내용 |
|------|------|
| **Python** | 메인 서버(`openviking/`), CLI(`ov`), SDK |
| **Rust** | 고성능 코어 `ragfs`(가상 파일시스템), `ov_cli` |
| **C++** | `src/` — 인덱스/스토어 백엔드 |
| **배포** | Docker, docker-compose, Caddyfile |
| **라이선스** | AGPLv3 (메인) / Apache 2.0 (일부 크레이트) |

## 벤치마크 성과

- **LoCoMo(사용자 메모리)**: Hermes 네이티브 33.38% → OpenViking 적용 시 82.86%, 입력 토큰 34~91% 절감
- **tau2-bench(에이전트 경험)**: 경험 메모리로 태스크 성공률 +6.87pp(리테일), +11.87pp(항공)
- **Hermes 공식 파트너**로 등록됨

## 설치 & 설정 (이 PC)

- **설치**: `uv venv ~/.openviking-venv --python 3.12` + `uv pip install --python ~/.openviking-venv/Scripts/python.exe openviking`
  - ⚠️ Windows Store Python(MSIX)은 pip 경로 문제로 설치 실패 → **uv venv로 우회**
  - ⚠️ **venv가 실제로 `C:/c/Users/KGA01/.openviking-venv`에 만들어졌다.** Git Bash에서 `~`가
    `/c/Users/...`로 풀린 채 Windows 도구에 넘어가 드라이브 뒤에 `c/Users/...`가 덧붙은 결과다.
    **오타가 아니라 실제 경로다** — 2026-08-21 원본 PC에서 확인:
    `C:/c/Users/KGA01/.openviking-venv/Scripts/`에 `openviking-server.exe`·`ov.exe`가 있고
    `C:/Users/KGA01/.openviking-venv`는 **없다**. (2026-08-21 1차 점검에서 "오기로 보임"이라고
    표시했던 것을 정정한다 — 다른 PC라 검증을 못 한 상태의 추측이었다)
  - 재설치할 일이 생기면 `~` 대신 **절대경로**를 주고, 그때 `C:/c/` 트리를 정리한다
- **실행 파일**: `C:/c/Users/KGA01/.openviking-venv/Scripts/openviking-server.exe`, `ov.exe`
- **설정**: `openviking-server init` → 로컬 올라마 기반 선택
  - embedding `qwen3-embedding:0.6b` + VLM `qwen3.5:4b` + query planner (총 ~5GB)
- **서버 실행**: `openviking-server` → `127.0.0.1:1933`
- **ov CLI 연결**: `ov config add custom --name local --url http://127.0.0.1:1933 --activate`

## Hermes 연동

- `hermes memory setup openviking` → `local` 프로필 연결
- config.yaml에 `provider: openviking` + `use_ovcli_config: true` 저장
- ⚠️ **새 세션부터 활성화** — 연동 설정 전에 시작된 세션은 `Status: not available`로 뜸

## LLM 호환성

**Embedding provider (13종)**: openai, azure, volcengine, vikingdb, ollama, jina, voyage, minimax, cohere, gemini, dashscope, litellm, local

**VLM provider (6종)**: volcengine, openai, openai-codex, kimi, glm, litellm

→ **provider-agnostic**. 특히 `litellm` provider로 ollama/OpenAI/Anthropic/Bedrock/Vertex 등 수십 개 모델을 하나의 설정으로 라우팅 가능.

## 참고사항

- **리소스 처리 속도**: 로컬 4b VLM으로 큰 저장소(3683개 파일) 처리 시 수십 분~수 시간 걸림. 작은 리소스부터 테스트 권장
- **ROOT 계정 제약**: `ov task cancel` 불가, 처리 중인 리소스 `ov rm` 불가 → 서버 내리고 데이터 직접 정리 필요
- **데이터 위치**: `~/.openviking/data/` (리소스 `viking/default/resources/`, 큐 `_system/queue/queue.db`, 벡터 `vectordb/`)

## 관련 페이지
- [[사용로그]] — LLM 도구 사용 기록
- [[프롬프트-패턴]] — LLM 사용 패턴
