---
title: 픽셀아트 스프라이트 파이프라인 - 세션 핸드오프
description: 새 세션 시작 시 이 파일부터 읽고 바로 작업을 재개하기 위한 진입점
created: 2026-08-19
updated: 2026-08-19
type: guide
status: active
tags:
  - gamedev
  - pixel-art
  - sprite
  - workflow
sources:
  - projects/gamedev/pixel-sprite-workflow/index.md
---

# 픽셀아트 스프라이트 파이프라인 — 세션 핸드오프

> **새 세션에서 이 프로젝트를 작업할 때 이 파일부터 읽어라.**
> 경로 찾는 시간 없이 바로 작업을 재개하도록, 모든 핵심 정보를 한 곳에 모았다.

## ⚡ 프로젝트 위치 (이거부터)

이 프로젝트는 홈 `C:\Users\KGA01` 이 아니라 **위키 폴더 안**에 있다.

| 항목 | 경로 |
|------|------|
| **프로젝트 루트** | `G:\내 드라이브\wiki\projects\gamedev\pixel-sprite-workflow\` |
| **스크립트** | `<루트>\scripts\` (pixel_converter.py, batch_converter.py, advanced_converter.py, web_gui.py 등) |
| **sprite-gen 도구** | `<루트>\sprite-gen\` (타사 오픈소스 파이프라인) |
| **sprite-gen venv** | `<루트>\sprite-gen\.venv\Scripts\python.exe` |
| **테스트 산출물** | `<루트>\test-assets\` |
| **위키 본문** | `<루트>\index.md` (24360자 상세 파이프라인 문서) |

## 🚀 핵심 명령어 (복사-붙여넣기용)

### 1. 픽셀아트 변환
```bash
cd "G:/내 드라이브/wiki/projects/gamedev/pixel-sprite-workflow/scripts"
python3 pixel_converter.py <input.png> -o <output.png> -w 64 -c 16
```

### 2. sprite-gen 배경 제거 (cutout)
```bash
SP="G:/내 드라이브/wiki/projects/gamedev/pixel-sprite-workflow/sprite-gen/.venv/Scripts/python"
"$SP" -m sprite_gen.cli cutout <input.png> --key auto --out <output.png>
```

### 3. sprite-gen 프레임 추출 (extract)
```bash
"$SP" -m sprite_gen.cli extract --run-dir <run-dir> --states walk
```

### 4. sprite-gen 스프라이트시트 (compose-atlas)
```bash
"$SP" -m sprite_gen.cli compose-atlas --run-dir <run-dir> --atlas sheet.png --manifest manifest.json
```

## 🔧 varco3d (3D/이미지 생성)

- **서버**: `https://3d.varco.ai/api/mcp` (config.yaml `varco-3d` 항목)
- **이미지 다운로드 base**: `https://3d.varco.ai` + `/api/objects/<hash>.png`
- **워크플로우 구축 순서** (MCP 도구):
  1. `list_workflow_sessions` → workflowId 확인
  2. `create_node` (TextInput + GenerateImage)
  3. `connect_edge` (TextInput.out → GenerateImage.prompt)
  4. `run_workflow` (scope에 GenerateImage nodeId)
  5. `get_workflow_graph` → 성공하면 출력 url
  6. `get_output_downloads` → download url
  7. curl로 다운로드
- **GenerateImage 모델**: gpt-image-1.5-medium (경제적 기본값), aspectRatio 3:4
- **스프라이트용 프롬프트 요령**: 마젠타 크로마키 배경(#FF00FF) 명시, 전신, 깨끗한 실루엣

## 🧪 테스트 상태 (2026-08-19)

### varco3 → 픽셀아트 end-to-end 테스트 ✅ (완료)
- **입력**: varco3에서 "검술 전사" 판타지 캐릭터 생성 (1024×1536, 마젠타 배경)
- **다운로드**: `test-assets/varco-fantasy/fantasy_warrior_raw.png`
- **변환**: pixel_converter → 64×96 RGBA (`warrior_64px.png`)
- **배경제거**: sprite-gen cutout → 투명 배경 69% (`warrior_cutout.png`)
- **결과**: AI 이미지 → 진짜 픽셀아트 → 투명 스프라이트까지 파이프라인 검증 완료

### sprite-gen 전체 기능 테스트 ✅ (이전 세션 완료, SPRITE_GEN_FULL_TEST.md 참조)
- cutout / extract / compose-atlas / curation 모두 동작 확인
- manifest.json (Unity/Godot 호환 프레임 좌표+애니메이션) 생성 확인

## 📋 다음 작업 후보
- [ ] 3D 리깅/애니메이션 경로 테스트 (Generate3D → Rig → Animate → 프레임 추출)
- [ ] 4방향(정면/후면/좌/우) 스프라이트 생성 및 compose-atlas로 시트 합치기
- [ ] 픽셀아트 웹 GUI(web_gui.py)에 sprite-gen cutout 통합 (Phase 1: 배경제거 버튼)

## 🔗 관련 위키
- [[픽셀아트 스프라이트 워크플로우]] — 상세 파이프라인 문서 (index.md)
- [[sprite-gen 통합 가이드]] — SPRITE_GEN_INTEGRATION.md
