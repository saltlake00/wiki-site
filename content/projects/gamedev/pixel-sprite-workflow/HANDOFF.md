---
title: 픽셀아트 스프라이트 파이프라인 - 세션 핸드오프
description: 새 세션 시작 시 이 파일부터 읽고 바로 작업을 재개하기 위한 진입점
created: 2026-08-19
updated: 2026-08-20
type: guide
status: active
tags: [개발, 게임, 도구]
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
| **sprite-gen 도구** | `C:\Users\KGA01\Documents\위키-참고자료\sprite-gen\` (타사 오픈소스, 2026-08-20 위키 밖으로 이동 — .git/.venv를 위키 git 저장소에 넣지 않기 위함) |
| **sprite-gen venv** | `C:\Users\KGA01\Documents\위키-참고자료\sprite-gen\.venv\Scripts\python.exe` |
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
SP="C:/Users/KGA01/Documents/위키-참고자료/sprite-gen/.venv/Scripts/python"
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

### 5. sprite-gen curation (웹 편집기) — 배치 파일로 바로 실행 ✅
```bash
# 더블클릭 또는 명령줄에서 (기본 run-dir = test-assets/varco-fantasy/run):
G:/내 드라이브/wiki/projects/gamedev/pixel-sprite-workflow/spritegen-curation.bat
# 다른 run-dir 지정:
...\spritegen-curation.bat <run-dir 경로>
```
- 배치 파일: `spritegen-curation.bat` (cp949 인코딩, Windows cmd 호환 — UTF-8로 저장하면 경로가 깨지므로 주의)
- 실행하면 브라우저가 자동으로 열려 프레임 편집(순서/변환/미리보기) 가능

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

### varco3 → 픽셀아트 → 스프라이트시트 full end-to-end 테스트 ✅ (완료)
- **1단계 varco3 캐릭터 생성**: 검술 전사 정면 + reference로 3방향(뒤/좌/우) 생성 (1024×1536, 마젠타 배경)
  - 정면: `fantasy_warrior_raw.png` / 뒤·좌·우: `back_view.png` `left_view.png` `right_view.png`
- **2단계 픽셀 변환**: 4장 → 64×96 RGBA (`*_64px.png`)
- **3단계 배경제거**: sprite-gen cutout → 투명 배경 (`*_cutout.png`)
- **4단계 스프라이트 스트립**: 4방향을 256×96 가로 스트립으로 합성 (`four_direction_strip.png`)
- **5단계 extract**: `run/raw/four_dir.png` → 4개 투명 프레임 분리 (`run/frames/four_dir/frame-0~3.png`) ✅
- **6단계 compose-atlas**: `run/four_dir_atlas.png` (256×96) + `four_dir_manifest.json` 생성 ✅
  - manifest: 프레임 좌표(x,y,w,h), fps 4, loop, durations_ms 포함 — Unity/Godot 즉시 사용 가능

**파이프라인 전 과정 검증 완료**: varco3 AI 이미지 → 진짜 픽셀아트 → 스프라이트시트 + 게임엔진 메타데이터까지.

### 걷기 애니메이션 픽셀아트 ✅ (완료, 진짜 목표)
- 대표 정면 1장 → **4개 파생 GenerateImage 노드** (각각 gpt-image-2-medium + 정면 reference)로 걷기 4프레임 생성
- → 픽셀 변환(64×96) → cutout → 가로 스트립 → extract → compose-atlas
- **최종**: `walk_gpt2/run/walk_atlas.png`(256×96) + `walk_manifest.json`(fps 8) + `walk_animation.gif`
- **핵심 교훈**: 프레임별 노드 방식 + gpt-image-2-medium. 방향 일관성 위해 "facing RIGHT + same direction as frame 1" 명시(왼발/오른발로 설명하면 뒤섞임). 검증은 qwen3.5:cloud 비전.

### 달리기 애니메이션 픽셀아트 ✅ (완료)
- 걷기와 동일 방식, **6프레임** (달리기는 포즈 변화 커서 4보다 6이 부드러움)
- **최종**: `run_gpt2/run/run_atlas.png`(384×96) + `run_manifest.json`(fps 10) + `run_animation.gif`
- 방향 전부 우측 + 일관된 사이클(보폭→공중→착지) qwen 검증 완료

### sprite-gen 전체 기능 테스트 ✅ (이전 세션 완료, SPRITE_GEN_FULL_TEST.md 참조)
- cutout / extract / compose-atlas / curation 모두 동작 확인

## 📋 다음 작업 후보
- [ ] ~~4방향 스프라이트 시트 합치기~~ ✅ (완료: four_dir_atlas.png + manifest.json)
- [ ] ~~걷기 애니메이션 픽셀아트~~ ✅ (완료: walk_atlas.png + walk_manifest.json)
- [ ] ~~달리기 애니메이션 픽셀아트~~ ✅ (완료: run_atlas.png + run_manifest.json)
- [ ] 다른 상태 추가 (공격/점프) 또는 걷기/달리기를 한 시트에 합치기
- [ ] Unity에 걷기+달리기 아틀라스 실제 임포트 테스트 (Filter Mode: Point, Bottom-Center pivot)
- [ ] 픽셀아트 웹 GUI(web_gui.py)에 sprite-gen cutout 통합 (Phase 1: 배경제거 버튼)

## 🔗 관련 위키
- [[projects/gamedev/pixel-sprite-workflow/index|픽셀아트 스프라이트 워크플로우]] — 상세 파이프라인 문서 (index.md)
- [[projects/gamedev/pixel-sprite-workflow/SPRITE_GEN_INTEGRATION|sprite-gen 통합 가이드]] — SPRITE_GEN_INTEGRATION.md
