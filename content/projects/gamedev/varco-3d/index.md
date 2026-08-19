---
title: VARCO 3D MCP
description: VARCO 3D 브라우저 워크플로우를 MCP로 제어 — AI 캐릭터/3D 이미지 생성
created: 2026-08-19
updated: 2026-08-19
type: entity
status: active
tags:
  - gamedev
  - unity
  - ai-tools
  - mcp
  - workflow
  - image-generation
card_title: 🧊 VARCO 3D 캐릭터 생성
card_description: VARCO 3D MCP로 브라우저 워크플로우에서 AI 캐릭터 생성
card_icon: 🧊
card_color: "#3B82F6"
---

# VARCO 3D MCP

VARCO 3D는 **브라우저 기반 3D/이미지 생성 도구**로, 사용자가 브라우저에 띄워둔 커스텀 워크플로우를 **MCP(remote)로 에이전트가 제어**할 수 있게 한다. 판타지 캐릭터 이미지 생성 등에 사용.

## 🔑 핵심 개념

- **Remote MCP server** — Streamable HTTP, `/api/mcp` 엔드포인트
- **OAuth 2.1 (PKCE)** — MCP 클라이언트가 자체적으로 OAuth 처리. curl로 직접 호출하거나 토큰을 수동으로 다루면 **안 됨**
- **동작 전제**: 서버는 각 도구 호출을 **사용자 브라우저에 열려 있는 커스텀 워크플로우에 전달**한다. → **워크플로우가 브라우저에 열려 있어야만 동작**함

## 🔧 Hermes에 MCP 설정 (완료)

```bash
hermes mcp add varco-3d --url https://3d.varco.ai/api/mcp --auth oauth
```

- OAuth 승인 URL이 나오면 **사용자에게 보여주고 승인 기다림** (대신 열지 말 것, 토큰 확인하지 말 것, 수동 처리 금지)
- 승인 후 13개 도구 발견 → `hermes mcp test varco-3d`로 연결 검증 완료
- **주의**: MCP 도구는 **새 세션에서만 로드**된다. 설정 후 새 대화를 시작해야 함

## 🛠️ 도구 13개

| 도구 | 기능 |
|------|------|
| `upload_image` | 이미지 업로드 → URL 반환 |
| `get_account_and_pricing` | 구독 등급 조회 |
| `list_workflow_sessions` | 열린 워크플로우 에디터 목록 |
| `get_node_catalog` | 생성 가능한 노드 종류 카탈로그 |
| `get_animation_catalog` | 애니메이션 키 목록 |
| `get_workflow_graph` | 현재 노드/엣지/값 조회 |
| `create_node` / `connect_edge` / `move_node` / `delete_node` | 워크플로우 편집 |
| `set_node_input` | 노드 값 설정 |
| `run_workflow` | 실행 (scope = action 노드 id 배열) |
| `get_output_downloads` | 이미지/3D 출력 다운로드 URL |

## ✅ 실제 테스트 (2026-08-19, 검증 완료)

varco3로 판타지 캐릭터 생성 → 픽셀아트 스프라이트 파이프라인 end-to-end 검증 성공.

**버전 2 — 걷기 애니메이션 (gpt-image-2-medium)**:
- 대표 정면 이미지 1장 → **4개 파생 GenerateImage 노드**로 걷기 4프레임 생성 (각각 정면 reference, gpt-image-2-medium, 3:4)
- → 픽셀 변환(64×96) → cutout 배경제거 → 가로 스트립 → extract → compose-atlas
- **최종**: `walk_gpt2/run/walk_atlas.png`(256×96) + `walk_manifest.json`(fps 8, 4프레임, 좌표)
- **주의(겪은 실수)**: 프롬프트에서 "left leg/right leg"로 포즈 설명 시 방향이 뒤섞임. "facing RIGHT + same direction as frame 1" 명시 필수. 방향 검증은 로컬 qwen3.5:cloud 비전.

**버전 3 — 달리기 애니메이션 (gpt-image-2-medium)**:
- 걷기와 동일 방식으로 달리기 6프레임 생성 (파생 노드, 정면 reference, gpt-image-2-medium)
- 방향 전부 우측 + 일관된 사이클(보폭→공중→착지) qwen 검증 완료
- **최종**: `run_gpt2/run/run_atlas.png`(384×96) + `run_manifest.json`(fps 10) + `run_animation.gif`

**실행한 워크플로우** (모두 MCP로 브라우저 워크플로우 제어):
1. `list_workflow_sessions` → workflowId `d2056c31-...` (빈 "Untitled" 워크플로우)
2. `create_node` TextInput (프롬프트) + GenerateImage
3. `connect_edge` TextInput.out → GenerateImage.prompt
4. GenerateImage 설정: `model=gpt-image-1.5-medium`(경제적 기본), `aspectRatio=3:4`, `count=1`
5. `run_workflow` scope=[GenerateImage nodeId] → `get_workflow_graph` 폴링 (약 50초 소요)
6. `get_output_downloads` → `/api/objects/<hash>.png`
7. `curl -L https://3d.varco.ai/api/objects/<hash>.png` 로 다운로드

**산출물**: `projects/gamedev/pixel-sprite-workflow/test-assets/varco-fantasy/`
- `fantasy_warrior_raw.png` — 1024×1536, 마젠타 크로마키 배경 (검술 전사)
- `warrior_64px.png` — pixel_converter로 64×96 픽셀아트
- `warrior_cutout.png` — sprite-gen cutout으로 배경 제거 (투명 69%)

**프롬프트 요령 (스프라이트용)**: 전신 정면, 마젠타 크로마키(#FF00FF) 배경 명시, 깨끗한 실루엣, 최소 그라데이션. 그러면 cutout이 정확히 배경만 제거함.

## 관련

- [[pixel-sprite-workflow]] — 생성된 캐릭터를 픽셀아트로 후처리
- [[링스택-게임]] — Unity 게임 (캐릭터 에셋에 사용 예정)

## 배포

`python sync_wiki.py` 실행 → 홈 카드 자동 생성 + content 복사 + git push + GitHub Pages 재배포
