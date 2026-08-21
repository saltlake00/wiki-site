---
title: 워크플로우 A — AI 이미지 → 픽셀아트
description: GPT 이미지 생성 → 프레임 추출 → 픽셀 변환 → 스프라이트시트 → Unity 통합 (Step 1~5)
created: 2026-08-18
updated: 2026-08-21
type: guide
status: active
sources: []
tags: [개발, 게임, Unity, 도구, AI/ML]
---

# 워크플로우 A — AI 이미지 → 픽셀아트

> **판단**: 세 옵션 중 **기본으로 택한 경로**다. 손으로 도트를 찍지 않고도 결과가 나오고, 3D 파이프라인보다 진입 비용이 낮다.
> **다음**: Step 3 변환 품질이 부족하면 [[projects/gamedev/pixel-sprite-workflow/workflow-b-3d-render|워크플로우 B]]의 3D 가이드 방식을 섞는다.

## 📋 워크플로우 A: AI 이미지 → 픽셀아트

### Step 1: 고해상도 컨셉 생성 (GPT-4 Image Generation)

**목표**: 깨끗한 고해상도 캐릭터 컨셉 이미지 생성

#### 프롬프트 전략
```
- Full-body character concept
- Clean solid background (black/white/green)
- High contrast for easy background removal
- Side view / 4-direction views
- Consistent lighting
- Clear silhouette
```

#### 프롬프트 예시
```
A full-body side-view character concept art of a fantasy knight 
with clear silhouette, standing pose, solid white background, 
high contrast, clean edges, concept art style, no shading gradients
```

#### ⚠️ 주의사항
- **단색 배경 필수**: 크로마키 제거 용이
- **그라디언트 최소화**: 픽셀 변환 시 색상 폭발 방지
- **명확한 실루엣**: 작은 사이즈에서도 인식 가능
- **풀바디 구도**: 게임 스프라이트는 전신 필요

---

### Step 2: 애니메이션 프레임 생성

**옵션 A: GPT 비디오 생성 + 프레임 추출**
```bash
# 짧은 애니메이션 비디오 생성 (걷기, 점프, 공격)
# FFmpeg로 프레임 추출
ffmpeg -i animation.mp4 -vf fps=8 frame_%04d.png
```

**옵션 B: 이미지 연속 생성**
- GPT로 같은 캐릭터의 포즈 시퀀스 생성
- 시드/스타일 참조 이미지로 일관성 유지
- 각 액션별 4-8프레임 권장

**옵션 C: AI 애니메이션 도구**
- **PixelLab** (pixellab.ai): 텍스트/스켈레톤 기반 애니메이션
- **Ludo.ai**: 픽셀 스프라이트 생성기
- **SpriteBrew** (GitHub): AI 기반 스프라이트시트 생성

---

### Step 3: 픽셀아트 변환 🎨

**목표**: 고해상도 프레임을 정확한 픽셀 그리드로 변환

#### 도구 선택

##### A) True Pixel (추천 ⭐)
- **사이트**: https://sorceress.games/pages/true-pixel
- **가격**: $49 일회성 (평생 사용)
- **특징**:
  - 비디오/이미지 → 픽셀 스프라이트시트 자동 변환
  - 배경 제거 (크로마키, CorridorKey)
  - 팔레트 고정 (자동 추출 또는 프리셋)
  - 디더링 (Ordered, Floyd-Steinberg)
  - 시간적 안정화 (프레임 간 픽셀 깜빡임 감소)
  - PNG 스프라이트시트 + 개별 프레임 ZIP

**워크플로우**:
```
1. 비디오/이미지 업로드
2. 프레임 선택 (30 FPS 자동 추출)
3. 배경 제거 + 크로마 클리닝
4. 팔레트 선택:
   - 자동 추출
   - PICO-8 (16색)
   - NES (54색)
   - Game Boy (4색)
   - Sweetie-16
5. 픽셀 변환 + 디더링
6. 스프라이트시트 내보내기
```

##### B) Aseprite (수동 변환)
- **가격**: $19.99 (Steam) / 무료 (소스 컴파일)
- **용도**: 정밀한 수동 픽셀 편집 + 애니메이션

**Img2Pixel 변환 과정**:
```
1. Aseprite에서 File > Open > 고해상도 프레임
2. Sprite > Sprite Size:
   - Algorithm: Nearest Neighbor (필수!)
   - 목표 크기: 32x32, 64x64 등
3. Edit > Adjustments > Color Curve:
   - 색상 단순화
4. Mode > Indexed Color:
   - 팔레트 색상 수 제한 (8-32색)
```

##### C) ComfyUI + Stable Diffusion
**로컬 오픈소스 파이프라인**

**필요 구성요소**:
- SDXL 베이스 모델
- Pixel Art LoRA
- 커스텀 노드:
  - `comfyui-rmbg`: 배경 제거
  - `ComfyUI-spritefusion-pixel-snapper`: 픽셀 스냅
  - Color Quantization 노드

**프롬프트 설정**:
```
Positive: pixel art, 16-bit, side-scroller sprite, 
         solid background, crisp pixels, <LoRA trigger>
         
Negative: blurry, smooth shading, 3D render, 
         anti-aliasing, realistic, gradient
```

**워크플로우**:
```
1. SDXL + Pixel Art LoRA 로드
2. 512x512 생성 (Nearest Neighbor로 다운스케일)
3. 32x32 또는 64x64로 리사이즈
4. 색상 팔레트 제한 (16색)
5. 배경 제거
```

##### D) 기타 온라인 도구
- **PixelLab** (pixellab.ai): AI 픽셀 애니메이션 생성
- **Piskel** (piskelapp.com): 무료 온라인 픽셀 에디터
- **Lospec Pixel Editor**: 브라우저 기반 픽셀 편집

---

### Step 4: 스프라이트시트 생성

**목표**: 개별 프레임을 Unity가 읽을 수 있는 그리드 배열로 정리

#### Aseprite에서 스프라이트시트 생성

```
1. 모든 프레임 Aseprite에 로드
2. Frame Tags 생성:
   - 프레임 1-6 선택 → 우클릭 → New Tag
   - 이름: "walk", "idle", "jump", "attack"
3. File > Export Sprite Sheet:
   - Layout: Horizontal Strip / Grid
   - Constraints: Fixed Size / Max Size
   - Output: PNG + JSON/XML 메타데이터
4. 저장: character_spritesheet.png
```

#### 온라인 도구
- **Spritesheet Generator** (spritesheetgenerator.online)
  - 무료, 드래그앤드롭
  - 애니메이션 프리뷰
  - PNG + JSON 내보내기

---

### Step 5: Unity 통합

#### 스프라이트시트 임포트

```csharp
1. Unity에서 Assets에 PNG 드래그
2. Inspector 설정:
   - Texture Type: Sprite (2D and UI)
   - Sprite Mode: Multiple
   - Pixels Per Unit: 32 (스프라이트 크기에 따라)
   - Filter Mode: Point (no filter) ← 픽셀아트 필수!
   - Compression: None
3. Sprite Editor 열기:
   - Slice > Grid By Cell Count
   - Pixel Size: 32x32 (또는 실제 크기)
   - Apply
```

#### 애니메이션 클립 생성

```
1. Window > Animation > Animation
2. 캐릭터 선택 → Create New Clip
3. 스프라이트시트 프레임 드래그
4. Sample Rate: 8-12 FPS (도트 감성)
5. Animator Controller에 State 추가
```

#### Pixel Perfect Camera 설정

```csharp
1. Package Manager > 2D Pixel Perfect 설치
2. Main Camera > Add Component > Pixel Perfect Camera
3. 설정:
   - Assets Pixels Per Unit: 32
   - Reference Resolution: 320x180 (또는 원하는 해상도)
   - Upscale Render Texture: 체크
```

---

## 관련

- [[projects/gamedev/pixel-sprite-workflow/index|워크플로우 개요]] — 전체 파이프라인과 옵션 선택
- [[projects/gamedev/pixel-sprite-workflow/scripts/README|스크립트 가이드]] — Step 3에서 쓰는 로컬 변환기
- [[projects/gamedev/pixel-sprite-workflow/references/video-workflow|비디오→스프라이트]] — Step 2 프레임 생성 심화
- [[projects/gamedev/pixel-sprite-workflow/troubleshooting|품질·트러블슈팅]]