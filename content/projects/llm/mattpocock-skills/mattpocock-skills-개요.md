---
title: mattpocock/skills 개요
created: 2026-08-19
updated: 2026-08-19
type: entity
status: active
tags: [AI/ML, 도구, 개발]
sources: [https://github.com/mattpocock/skills]
---

# mattpocock/skills 개요

> **실전 엔지니어용 AI 에이전트 스킬 모음**. Matt Pocock이 매일 쓰는 스킬.
> "vibe coding이 아닌 실제 엔지니어링"을 위한 스킬.

## 핵심 특징

- **작고, 적응하기 쉽고, 조합 가능** — GSD/BMAD/Spec-Kit 같은 프로세스 소유형 도구와 달리 제어권을 뺏지 않음
- **어떤 모델과도 호환** — 모델 무관
- **수십 년 엔지니어링 경험 기반**
- **222k+ 스타** — GitHub 트렌딩 1위급 인기

## 설치

```bash
# Claude Code (공식 마켓플레이스, 자동 업데이트)
claude plugins install mattpocock-skills
# 또는 세션 내에서
/plugin install mattpocock-skills

# Codex 및 기타 에이전트
npx skills@latest add mattpocock/skills
```

## Hermes와의 관계

- Hermes도 스킬 시스템(`~/AppData/Local/hermes/skills/`)을 사용
- 이 프로젝트의 스킬 작성 방식/구조를 Hermes 스킬 작성에 참고 가능
- 특히 "작고 조합 가능한 스킬" 철학은 Hermes 스킬 가이드와 일치

## 관련 페이지
- [[openviking-개요]] — AI 에이전트용 컨텍스트 DB
- [[사용로그]] — LLM 도구 사용 기록
