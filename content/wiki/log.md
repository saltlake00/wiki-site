# Wiki Log

> Chronological record of all wiki actions. Append-only.
> Format: `## [YYYY-MM-DD] action | subject`
> Actions: ingest, update, query, lint, create, archive, delete
> When this file exceeds 500 entries, rotate: rename to log-YYYY.md, start fresh.

## [2026-08-18] create | Wiki initialized
- Domain: 개인 지식 베이스 (업무/취미/개발)
- Structure created with SCHEMA.md, index.md, log.md
- Location: G:\내 드라이브\wiki
- Sync: Google Drive (G:) + Git (예정)

## [2026-08-18] ingest | 링 스택 게임 프로젝트
- Source: C:\Users\KGA01\Documents\UnityProject\StackCopy\README.md
- Saved raw source to `raw/articles/링스택-게임-README.md`
- Created pages:
  - `entities/링스택-게임.md` — 프로젝트 개요, 기술 스택, 구조
  - `concepts/링스택-판정로직.md` — 720슬롯 AND 판정
  - `concepts/링스택-절차적-메시.md` — 쐐기 지오메트리 메시 생성
  - `concepts/링스택-셰이더.md` — ToonNPR + Unlit 셰이더
  - `concepts/링스택-색상-팔레트.md` — OKLCH 그라데이션
  - `concepts/링스택-카메라.md` — 아이소메트릭 카메라 + 리빌
  - `comparisons/링스택-vs-원본스택.md` — 원본 Stack 대비 차별점
- Updated `index.md` (Total pages: 7)

## [2026-08-18] restructure | 도메인별 폴더 재구성
- 사용자 요청: 프로젝트/유니티/링스택 3단계 구조로 재구성
- 링스택 페이지 7개를 `projects/unity/링스택/` 폴더로 이동
- 원본 자료를 `raw/projects/unity/링스택/` 로 이동
- `sources:` frontmatter 경로 일괄 수정
- SCHEMA.md에 "폴더 구조 (도메인별 분리)" 섹션 추가
- index.md를 Projects/Concepts/Comparisons/Queries 섹션으로 재구성
- `.obsidian/` 로컬 설정 gitignore 추가
- 빈 폴더(entities/, concepts/, comparisons/) 정리

## [2026-08-18] create | LLM 도메인 + GUIDE.md 추가
- 사용자 요청: LLM 사용 기록 관리 방식 + 다른 AI가 위키 쓰는 방법 검토
- `llm/` 도메인 신설 (LLM 사용 기록은 프로젝트와 분리된 횡단적 활동이므로 별도 도메인으로)
  - `llm/사용로그.md` — 날짜별 LLM 사용 기록 (append-only)
  - `llm/프롬프트-패턴.md` — 자주 쓰는 프롬프트/기법 모음
- `GUIDE.md` 신설 — AI 에이전트가 위키를 다루기 전에 먼저 읽는 온보딩 지침서
  - 폴더 구조, 오리엔테이션 절차, 페이지 추가/수정 규칙, 조회/점검 방법, 태그 분류 요약
  - 어떤 AI든 위키 폴더를 주면 "GUIDE.md 먼저 읽어"라고 하면 됨
- index.md에 LLM 섹션 추가, "AI 에이전트는 GUIDE.md 먼저 읽기" 안내 추가 (Total pages: 9)

## [2026-08-18] update | GUIDE.md에 다기기 사용/편집 안내 추가
- 사용자 요청: 다른 기기에서 편집 가능하게 위키 가이드에 추가
- GUIDE.md에 "다른 기기에서 사용/편집하기" 섹션 추가
  - 기기별 설정 표 (이 PC / 다른 PC / 모바일 / 다른 AI 에이전트)
  - 편집 시 충돌 방지 규칙 (한 번에 한 기기, Drive 동기화 대기, Git 백업, 이미지 규칙)
  - Hermes 자동 사용 (WIKI_PATH) 안내
