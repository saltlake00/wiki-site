---
title: OpenViking HANDOFF
created: 2026-08-19
updated: 2026-08-19
type: guide
status: active
tags: [LLM, 개발, 도구]
sources:
  - projects/llm/openviking/openviking-개요.md
---

# OpenViking HANDOFF

> 새 세션에서 OpenViking 작업 시 **이 파일부터 읽고 시작**하라.
> 상세 내용은 [[openviking-개요]] 참고.

## 핵심 경로

| 항목 | 경로 |
|------|------|
| 프로젝트 소스 | `C:\Users\KGA01\OpenViking` |
| venv 실행파일 | `C:/c/Users/KGA01/.openviking-venv/Scripts/` |
| 서버 실행파일 | `C:/c/Users/KGA01/.openviking-venv/Scripts/openviking-server.exe` |
| ov CLI | `C:/c/Users/KGA01/.openviking-venv/Scripts/ov.exe` |
| 서버 로그 | `~/.openviking/server.log` |
| 데이터 | `~/.openviking/data/` |
| ov CLI config | `~/.openviking/ovcli.conf.local` (활성: `ovcli.conf`) |
| Hermes config | `~/.hermes/config.yaml` (provider: openviking) |

## 복사-붙여넣기용 핵심 명령어

```bash
export OV_BIN="C:/c/Users/KGA01/.openviking-venv/Scripts"

# 서버 시작 (백그라운드)
"$OV_BIN/openviking-server.exe" > ~/.openviking/server.log 2>&1 &

# 서버 상태 확인
curl -s http://127.0.0.1:1933/health

# ov CLI 상태/리소스
"$OV_BIN/ov.exe" status
"$OV_BIN/ov.exe" tree viking://resources/ -L 2

# 리소스 추가 (작은 것부터! --wait 없이 백그라운드)
"$OV_BIN/ov.exe" add-resource <url>

# 작업 목록/취소
"$OV_BIN/ov.exe" task list
"$OV_BIN/ov.exe" task cancel <task_id>   # ⚠️ ROOT는 불가
```

## 현재 상태 (2026-08-19)

- ✅ OpenViking 0.4.15 설치, 서버 실행 중 (`127.0.0.1:1933`)
- ✅ Hermes 연동 완료 (`provider: openviking`) — **새 세션부터 활성화**
- ✅ 테스트 리소스(OpenViking 저장소 3683개 파일)는 **취소/삭제됨** — 데이터 깨끗한 상태
- ⚠️ 리소스 처리: 로컬 4b VLM이라 큰 저장소는 수십 분~수 시간 걸림 → **작은 리소스부터 테스트**

## 다음 작업 후보

- [ ] 새 Hermes 세션에서 OpenViking 메모리가 실제로 동작하는지 확인
- [ ] 작은 리소스(위키 문서 몇 개, 작은 저장소)로 처리 속도 확인
- [ ] 실제 사용 시 리소스 추가 → 검색(`ov find`) → 세션 메모리 커밋 흐름 테스트

## 주의사항

- **Windows Store Python(MSIX) pip 경로 문제** → uv venv로 설치 (이미 완료)
- **venv 경로 꼬임**: `/c/c/Users/...`로 생성됨 → 실제 Windows 경로 `C:/c/Users/...`로 접근
- **ROOT 계정 제약**: task cancel/처리중 리소스 삭제 불가 → 서버 내리고 `~/.openviking/data/` 직접 정리
- **Hermes 연동은 새 세션부터** — 현재 세션은 `Status: not available` 정상
