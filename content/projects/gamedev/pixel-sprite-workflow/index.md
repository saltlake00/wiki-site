---
title: AI 이미지 → 도트 스프라이트 워크플로우
description: Unity 2D 플랫포머용 도트 감성 스프라이트 제작 파이프라인
created: 2026-08-18
updated: 2026-08-21
type: guide
status: active
sources: []
tags: [개발, 게임, Unity, 도구, AI/ML]
card_title: 🎮 도트 스프라이트 제작
card_description: GPT 이미지 생성부터 Unity 애니메이션까지
card_icon: 🎨
card_color: "#8B5CF6"
---

# AI 이미지 → 도트 스프라이트 워크플로우

> **판단**: 세 경로(A: AI 이미지 / B: 3D 렌더 / C: 오픈소스 도구) 중 **A를 기본**으로 쓰고,
> 일관성이 중요한 캐릭터만 B를 섞는다. 변환은 직접 만든 로컬 Python 변환기를 쓴다.
> **다음**: 캐릭터 1종으로 A 경로를 끝까지(Unity 애니메이션까지) 통과시켜 파이프라인을 검증한다.

Unity 2D 플랫포머 게임용 도트 감성 캐릭터 스프라이트를 GPT 이미지 생성부터 최종 애니메이션까지 제작하는 전체 파이프라인.

## 🎯 핵심 원칙

**❌ 직접 도트 생성은 실패한다**
```
"픽셀아트 캐릭터 만들어줘" → 뭉개진 fake pixel 그림
```

**✅ 고해상도 → 변환 → 후처리 파이프라인**
```
고해상도 컨셉 생성 → 프레임 분할 → 픽셀 변환 → 수동 정리
```

---

## 🎮 워크플로우 선택

### 옵션 A: AI 이미지 → 픽셀아트 (추천 ⭐)
GPT/Stable Diffusion으로 고해상도 생성 → 픽셀 변환

### 옵션 B: 3D 모델 → 픽셀아트 (던파 방식)
Blender 3D 렌더 → 픽셀 변환 (일관성 최고)

### 옵션 C: 수작업 도트 (전통 방식)
Aseprite에서 처음부터 픽셀 단위로 직접 제작

---

## 📋 워크플로우 상세

각 경로의 단계별 내용은 하위 페이지로 분리했다.

- [[projects/gamedev/pixel-sprite-workflow/workflow-a-ai-image|워크플로우 A — AI 이미지 → 픽셀아트]] — Step 1~5 (생성 → 프레임 → 변환 → 시트 → Unity)
- [[projects/gamedev/pixel-sprite-workflow/workflow-b-3d-render|워크플로우 B — 3D 모델 → 픽셀아트]] — Blender 자동 렌더, 던파 방식
- [[projects/gamedev/pixel-sprite-workflow/workflow-c-opensource-tools|워크플로우 C — 오픈소스 변환 도구]] — 무료/유료 도구 5개 비교

## 🛠️ 도구 비교표 (업데이트)

| 도구 | 용도 | 가격 | 장점 | 단점 |
|------|------|------|------|------|
| **True Pixel** | 자동 변환 | $49 일회성 | 비디오→시트 자동화, 팔레트 고정, 안정화 | 유료 |
| **PixelAfterAll** ⭐ | 노드 기반 변환 | $18 일회성 | ComfyUI 스타일, 배치 처리, 비디오 지원 | 유료 (저렴) |
| **Image-to-Pixel** ⭐ | 웹 변환 | 무료 | 실시간, 디더링, API 제공, MIT | 웹 기반만 |
| **Pixel-Perfect** ⭐ | 그리드 변환 | 무료 | 정밀 제어, 내장 편집기, Ctrl+Z | 웹 기반만 |
| **Aseprite** | 수동 편집 | $19.99 | 정밀 제어, 애니메이션 도구 | 수동 작업 필요 |
| **Blender** | 3D→픽셀 | 무료 | 일관성, 회전뷰, 무료 리깅 | 설정 복잡 |
| **ComfyUI** | AI 파이프라인 | 무료 | 오픈소스, LoRA 학습 | GPU 필요, 진입장벽 |
| **PixelLab** | AI 생성 | $12/월~ | 텍스트→애니메이션, 회전뷰 | 구독제 |
| **Pixel Snapper** | AI 정리 | 무료/7.99 | mixel 제거, 팔레트 매칭 | 웹 버전 제한 |
| **wdot** | WPlace 변환 | 무료 | 한국어, 실시간, 팔레트 자동 | WPlace 전용 |

---

## 🐍 직접 만든 로컬 변환기

Python 변환기(웹 GUI / CLI / 배치 / 비디오→스프라이트시트)는 **스크립트와 같은 폴더에서
관리한다.** 설치·사용법·옵션은 아래를 보라 — 이 페이지에 중복해두면 둘이 갈라진다.

- [[projects/gamedev/pixel-sprite-workflow/scripts/README|스크립트 가이드]] — 설치, 웹 GUI, CLI, 배치, 옵션 상세, 프리셋
- [[projects/gamedev/pixel-sprite-workflow/scripts/ADVANCED|고급 기능 가이드]] — 다운스케일·디더링·외곽선 세부 옵션
- [[projects/gamedev/pixel-sprite-workflow/scripts/WEB_GUIDE|웹 GUI 가이드]] — 브라우저 변환기 사용법
- [[projects/gamedev/pixel-sprite-workflow/references/video-workflow|비디오→스프라이트 워크플로우]] — ComfyUI/SVD 경로

## 🚀 권장 워크플로우 (업데이트)

### 빠른 프로토타입
```
GPT 이미지 생성 
  ↓
Image-to-Pixel 웹 (무료) 또는 Python 스크립트
  ↓
Unity 임포트 (Filter Mode: Point)
```

### 고품질 제작 (추천 ⭐)
```
GPT 이미지 생성 (고해상도)
  ↓
비디오 생성 또는 프레임 연속 생성
  ↓
PixelAfterAll 노드 변환 ($18)
  ↓
Aseprite 수동 정리 (픽셀 보정)
  ↓
Unity 애니메이션 클립
```

### 무료 오픈소스 (완전 로컬)
```
GPT 이미지 생성
  ↓
Python pixel_converter.py (배치 처리)
  ↓
Aseprite 정리 (선택)
  ↓
Unity 임포트
```

### 3D 파이프라인 (일관성 최고)
```
Blender 3D 모델 + Mixamo 애니메이션
  ↓
Orthographic 렌더 (Toon Shader, 저해상도)
  ↓
Python 배치 변환 또는 PixelAfterAll
  ↓
Aseprite 도트 감성 리터칭 (던파 방식)
  ↓
Unity 통합
```

### 던파 스타일 (최고 품질)
```
1. ComfyUI + Pixel LoRA로 고해상도 픽셀스타일 생성
2. 8배 다운스케일 (768x1344 → 96x168)
3. PixelAfterAll 색상 제한 + 디더링
4. Aseprite 수작업 리터칭 (핵심!)
5. 캐릭터 LoRA 학습 (일관성)
6. Unity 애니메이션
```

---

## 🎨 품질과 문제 해결

- [[projects/gamedev/pixel-sprite-workflow/troubleshooting|품질 체크리스트 · 트러블슈팅 · 프로 팁]]

## 📚 참고 자료

### 도구 링크
- **Image-to-Pixel**: https://tezumie.github.io/Image-to-Pixel/
- **Pixel-Perfect Converter**: https://github.com/Void8Bit/Pixel-Perfect-AI-Art-Converter
- **PixelAfterAll**: https://masuone.itch.io/pixel-after-all
- **True Pixel**: https://sorceress.games/pages/true-pixel
- **Pixel Snapper**: https://www.spritefusion.com/pixel-snapper
- **wdot**: https://noipung.github.io/wdot/
- **Aseprite**: https://www.aseprite.org
- **PixelLab**: https://www.pixellab.ai

### Blender 3D → 픽셀아트
- **Blender**: https://www.blender.org
- **Mixamo**: https://www.mixamo.com (무료 리깅/애니메이션)
- **Sprytile**: Blender 픽셀 타일 애드온

### 색상 팔레트
- **Lospec**: https://lospec.com/palette-list (픽셀아트 팔레트 DB)
- **PICO-8**: 16색 제한 팔레트
- **NES**: 54색 클래식 팔레트
- **Game Boy**: 4색 모노크롬

### 커뮤니티 & 튜토리얼
- **디시인사이드 게임 개발**: https://gall.dcinside.com/mgallery/board/lists/?id=game_dev
- **masuone 작가**: https://x.com/masuone_ (PixelAfterAll 제작자)
- **Reddit r/blender**: 3D → 픽셀아트 워크플로우
- **DevDude.Unreal**: YouTube - 픽셀아트 튜토리얼

### 공식 문서
- **Unity Pixel Perfect**: https://docs.unity3d.com/Packages/com.unity.2d.pixel-perfect
- **Aseprite Sprite Sheet**: https://www.aseprite.org/docs/sprite-sheet
- **Blender Orthographic Camera**: https://docs.blender.org/manual/en/latest/render/cameras.html

---

## 🎯 다음 단계

1. **배치 자동화**: Python 스크립트로 프레임 일괄 처리
2. **VFX 추가**: 공격 이펙트, 파티클도 같은 파이프라인
3. **다방향 스프라이트**: 4방향/8방향 뷰 생성
4. **장비 시스템**: 레이어 분리로 커스터마이징 가능

---

## 📝 작업 로그 템플릿

```markdown
### 캐릭터: [이름]
- 생성일: YYYY-MM-DD
- GPT 프롬프트: "..."
- 해상도: 원본 1024x1024 → 32x32 픽셀
- 팔레트: PICO-8 (16색)
- 프레임 수: Idle 6, Walk 8, Jump 4
- 도구: True Pixel → Aseprite 정리
- Unity 경로: Assets/Sprites/Characters/
- 이슈: 배경 제거 후 외곽선 노이즈 → Edge Cleanup으로 해결
```

---

**최종 업데이트**: 2026-08-18  
**작성자**: AI 어시스턴트  
**피드백**: 실제 제작 과정에서 발견한 이슈를 이 문서에 추가 바랍니다.

## 관련

- [[projects/gamedev/pixel-sprite-workflow/HANDOFF|세션 핸드오프]] — 경로·명령어·테스트 상태
- [[projects/gamedev/pixel-sprite-workflow/SPRITE_GEN_INTEGRATION|sprite-gen 통합 가이드]]
- [[projects/gamedev/index|게임 개발]]
