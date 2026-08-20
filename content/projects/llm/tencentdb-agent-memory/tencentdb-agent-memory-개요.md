---
title: TencentDB-Agent-Memory 개요
created: 2026-08-19
updated: 2026-08-19
type: entity
status: active
tags: [AI/ML, 도구, 개발]
sources: [https://github.com/TencentCloud/TencentDB-Agent-Memory]
---

# TencentDB-Agent-Memory 개요

> **팀 단위 AI 에이전트 메모리 허브**. 대화, 문서, 코드를 4가지 재사용 가능한 메모리 자산으로 변환.
> 우리 위키의 LLM-Wiki 개념과 정확히 일치하는 프로젝트.

## 핵심 개념

- **4가지 메모리 자산**:
  - **Chat Memory** — 대화 기억
  - **Skill** — 재사용 가능한 스킬
  - **LLM-Wiki** — 지식 베이스 (우리 위키와 동일 개념!)
  - **Code-Graph** — 코드 구조 그래프
- **팀 공유**: 에이전트/프레임워크 전반에 걸쳐 관리·공유·장착
- **제로 코드 통합**: 에이전트의 base URL을 Proxy로 지정하면 끝 (플러그인/훅/MCP 불필요)

## 설치

```bash
git clone https://github.com/Tencent/TencentDB-Agent-Memory.git
cd TencentDB-Agent-Memory/deploy/global-images
cp .env.example .env
$EDITOR .env       # LLM 파라미터 2세트 (memory group + proxy group)
./start-all.sh     # 한 번에 3개 서비스 시작 (memory-core + memory-hub + proxy)
```

- **패널**: http://localhost:8125
- **DeepSeek 등 지원**

## 우리 위키와의 관계

- 우리가 구축 중인 LLM 위키(GUIDE.md/SCHEMA.md/index.md 구조)와 **같은 개념**을 팀 단위로 확장한 것
- 참고할 점: Chat Memory / Skill / Code-Graph 자산 분리, 팀 공유, 제로 코드 통합 방식
- 우리 위키는 개인용이라 이 프로젝트의 팀 기능은 과할 수 있음 — **LLM-Wiki 자산 관리 방식만 참고**

## 관련 페이지
- [[openviking-개요]] — AI 에이전트용 컨텍스트 DB
- [[사용로그]] — LLM 도구 사용 기록
