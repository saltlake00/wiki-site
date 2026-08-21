---
title: OmniRoute 개요
created: 2026-08-19
updated: 2026-08-21
type: entity
status: active
tags: [AI/ML, 도구, 개발]
sources: [https://github.com/diegosouzapw/OmniRoute]
---

# OmniRoute 개요

> **판단**: 무료 티어 집계 + 제로 설정이 장점이고 설치·기동·`auto` chat completion까지는 검증됐다. 다만 `models list`가 비어 있고 로컬 ollama / Claude OAuth 연동이 미완이라 **아직 상시 경로로 쓸 단계는 아니다.**
> **다음**: provider 설정을 채워 `models list`를 살린다. Claude OAuth 연동을 할지 말지 결정한다.

> **무료 AI 게이트웨이**. 하나의 엔드포인트로 340+ provider(90+ 무료), 1200+ 모델을 라우팅.
> Claude Code, Codex, Cursor, OpenCode, Cline, Copilot 등과 호환.

## 핵심 기능

- **무료 티어 집계**: 42개 provider 풀 / 495개 모델의 무료 티어를 집계해 대시보드에 실시간 표시 (~1.51B 무료 토큰/월)
- **쿼터 인식 자동 폴백**: 무료 티어 소진 시 자동으로 다른 provider로 전환
- **토큰 압축**: RTK + Caveman 압축으로 토큰 15-95% 절감
- **MCP/A2A 지원**: `claude mcp add-server omniroute --type http --url http://localhost:20128/api/mcp/stream`
- **제로 설정**: 설치 직후 `auto` 모델로 바로 동작 (키/설정 불필요)
- **CLI 통합**: `omniroute run claude/codex/aider/goose/opencode/qwen/gemini` 등

## 설치 & 실행 (이 PC)

```bash
# 설치 (네이티브 바이너리 필요 → allow-scripts 필수)
npm install -g --allow-scripts=omniroute,keytar,tls-client-node,onnxruntime-node,sharp,core-js,@parcel/watcher,@swc/core,protobufjs,koffi,esbuild omniroute

# 실행
omniroute   # 게이트웨이 + 대시보드 (포트 20128)
```

- **대시보드**: http://localhost:20128
- **API Base**: http://localhost:20128/v1
- **모델**: `auto` (제로 설정 스마트 라우팅) 또는 provider/model 지정

## 적용 상태 (2026-08-19)

- ✅ 설치 완료 (v3.8.49)
- ✅ 서버 실행 중 (포트 20128)
- ✅ `auto` 모델로 chat completion 동작 확인 (스트리밍 응답)
- ⚠️ `omniroute models list`가 비어있음 — provider 설정 필요
- ⚠️ 로컬 ollama / Claude OAuth 연동은 추가 설정 필요

## 주의사항

- **네이티브 바이너리**: better-sqlite3, sharp 등 설치 스크립트가 npm 기본 설정에서 차단됨 → `--allow-scripts` 필수
- **포트 충돌**: 이전 프로세스가 포트 20128 점유 시 `taskkill /PID <pid> /F`로 정리
- **시작 시간**: 첫 시작에 ~40초 걸림 (네이티브 모듈 로드)

## 관련 페이지
- [[openviking-개요]] — AI 에이전트용 컨텍스트 DB
- [[사용로그]] — LLM 도구 사용 기록
