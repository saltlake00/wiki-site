---
title: AI 이미지 → 도트 스프라이트 워크플로우
description: Unity 2D 플랫포머용 도트 감성 스프라이트 제작 파이프라인
created: 2026-08-18
updated: 2026-08-18
tags:
  - gamedev
  - unity
  - pixel-art
  - sprite
  - workflow
card_title: 🎮 도트 스프라이트 제작
card_description: GPT 이미지 생성부터 Unity 애니메이션까지
card_icon: 🎨
card_color: "#8B5CF6"
---

# AI 이미지 → 도트 스프라이트 워크플로우

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

## 📋 워크플로우 B: 3D 모델 → 픽셀아트 (던파 방식)

**던전앤파이터 실제 워크플로우 분석**

> 던파는 완전 자동 3D→도트 변환을 사용하지 않습니다. 3D 뼈대를 **참고 가이드로만** 사용하고, 디자이너가 한 프레임씩 수작업으로 도트를 직접 찍습니다.

### 방법 1: Blender 자동 렌더 (프로토타입용)

**장점**: 빠르고, 회전/애니메이션 자동 생성, 일관성 최고  
**단점**: AI 느낌 적음, 수작업 디테일 부족

#### Blender 설정

```
1. Render Engine: Eevee (빠른 렌더)
   - Samples: 1 (안티앨리어싱 제거)
   - Pixel Filter Size: 0.0 (픽셀 경계 선명)

2. Camera: Orthographic 모드
   - Perspective 왜곡 제거 (탑다운/사이드뷰 필수)
   - Orthographic Scale: 모델 크기에 맞춤

3. Film: Transparent 체크 (투명 배경)

4. Output Resolution: 매우 낮게 설정
   - 32x32, 64x64, 128x128 등
   - 이후 업스케일하지 말 것!

5. Shading: Toon Shader
   - Diffuse BSDF → Shader to RGB → Color Ramp (Constant)
   - Color Ramp Stops: 3-4개 (그라디언트 제거)
   - Freestyle 또는 Inverted Hull로 외곽선 추가

6. Texture Filtering: Closest/Nearest
```

#### 렌더 & 내보내기

```bash
# 애니메이션 렌더 (PNG 시퀀스)
1. Output Format: PNG (RGBA)
2. Frame Rate: 8-12 FPS (도트 감성)
3. Render > Animation

# FFmpeg로 스프라이트시트 생성
ffmpeg -i render_%04d.png -filter_complex tile=8x1 spritesheet.png
```

#### Blender 애드온

- **Sprytile**: 3D 공간에서 직접 픽셀 타일 편집
- **PixelOver**: 3D 렌더를 픽셀아트로 자동 변환
- **Mixamo**: 무료 리깅 애니메이션 (걷기, 달리기 등)

### 방법 2: 3D 가이드 + 수작업 (던파 방식 ⭐)

**장점**: 최고 품질, 도트 감성 살림, 디테일 제어  
**단점**: 시간 소요 큼

```
1. Blender에서 3D 뼈대 애니메이션 제작
   ↓
2. Orthographic 뷰로 저해상도 렌더 (참고용)
   ↓
3. Aseprite에 렌더 이미지 Import
   ↓
4. 렌더 이미지를 Tracing Layer로 설정
   ↓
5. 새 레이어에서 도트를 직접 찍음
   - 렌더는 가이드일 뿐, 직접 픽셀 배치
   - 도트 감성을 살리기 위해 의도적으로 생략/과장
   ↓
6. 모든 프레임 반복
```

#### 던파 그래픽팀 인터뷰 핵심

```
- 포토샵 + 자체 프로모션 툴 사용
- 각성기 등 복잡한 연출도 수작업
- 3D는 뼈대/가이드로만 활용
- 일러스트 느낌을 살리기 위해 전용 도트 프레임 별도 제작
```

---

## 📋 워크플로우 C: 로컬 오픈소스 픽셀 변환기

### 무료 오픈소스 도구 모음

#### 1. **Image-to-Pixel** (JavaScript/Web) ⭐⭐⭐
- **저장소**: https://github.com/Tezumie/Image-to-Pixel
- **라이브**: https://tezumie.github.io/Image-to-Pixel/
- **특징**:
  - 초고속 실시간 변환
  - 디더링: Floyd-Steinberg, Bayer 2x2/4x4, Ordered, Atkinson
  - Lospec 팔레트 API 연동
  - 커스텀 팔레트 저장/불러오기
  - JavaScript API 제공 (p5.js/q5.js 통합 가능)
  - **완전 무료, MIT 라이선스**

**사용법**:
```html
<script src="https://cdn.jsdelivr.net/gh/Tezumie/Image-to-Pixel@main/image-to-pixel.js"></script>
<script>
ditheredCanvas = await pixelate({
  image: myCanvas,
  width: 64,
  dither: 'Floyd-Steinberg',
  strength: 20,
  palette: ['#1b1b1e', '#f4f1de', '#e07a5f', '#3d405b'],
  resolution: 'pixel'
});
</script>
```

#### 2. **Pixel-Perfect-AI-Art-Converter** (Web) ⭐⭐⭐
- **저장소**: https://github.com/Void8Bit/Pixel-Perfect-AI-Art-Converter
- **특징**:
  - 그리드 기반 정밀 변환
  - 이미지 위치/줌 수동 조정
  - 4가지 변환 알고리즘:
    - Most Used Color (가장 많은 색)
    - Prioritize Light/Dark (명도 가중치)
    - Average Color (평균 색상)
    - Neighbor Color (이웃 영역 블렌딩)
  - 내장 픽셀 편집기 (Brush, Eraser, Magic Wand)
  - Ctrl+Z/Y 지원
  - **완전 무료, Apache-2.0**

**설치**:
```bash
# 다운로드 후 압축 해제
# index.html 더블클릭으로 브라우저에서 실행
```

#### 3. **wdot** (Web) - WPlace 전용
- **저장소**: https://github.com/noipung/wdot
- **라이브**: https://noipung.github.io/wdot/
- **특징**:
  - WPlace 팔레트 자동 매칭
  - 밝기/대비/채도 조정
  - 디더링 지원
  - 실시간 프리뷰
  - 한국어 UI

#### 4. **SpriteFusion Pixel Snapper** (Web/Desktop)
- **웹**: https://www.spritefusion.com/pixel-snapper
- **데스크톱**: $7.99 (한정 할인 중)
- **특징**:
  - AI 픽셀아트 정리 (mixel 제거)
  - 커스텀 팔레트 지원 (NES, SNES, Game Boy 등)
  - 디테일 보존 (디더링, 외곽선)
  - 웹 버전 무료, 데스크톱 버전 배치 처리

#### 5. **PixelAfterAll** ($18 일회성) ⭐⭐⭐⭐⭐
- **구매**: https://masuone.itch.io/pixel-after-all
- **제작자**: @masuone_ (트위터)
- **특징**:
  - **노드 기반 필터 시스템** (ComfyUI 스타일)
  - 비디오 입력 → GIF/스프라이트시트
  - 프레임 선택 애니메이션
  - 배치 변환 (폴더 일괄 처리)
  - 커스텀 필터 저장/로드 (JSON)
  - 디더링 지원
  - 라이트/다크 테마
  - **Windows/macOS/Linux**

**masuone 작가 워크플로우** (디시인사이드 게시글 기반):
```
1. ILXL 체크포인트 + 픽셀 LoRA로 AI 이미지 생성
2. ComfyUI에서 8배 다운스케일 (768x1344 → 96x168)
3. PixelAfterAll로 색상 제한 + 디더링
4. Aseprite에서 수동 리터칭
5. 캐릭터 LoRA 학습 (일관성 유지)
```

---

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

## 🎨 픽셀아트 품질 체크리스트

### ✅ 변환 품질 확인
- [ ] 명확한 픽셀 그리드 (흐릿한 경계 없음)
- [ ] 안티앨리어싱 제거 완료
- [ ] 일관된 색상 팔레트 (프레임 간 색상 통일)
- [ ] 투명 배경 깔끔함 (외곽선 노이즈 없음)
- [ ] 프레임 간 픽셀 깜빡임 최소화

### ✅ 애니메이션 품질
- [ ] 적절한 프레임 수 (걷기 6-8, idle 4-6)
- [ ] 루핑 자연스러움 (첫/마지막 프레임 연결)
- [ ] 캐릭터 중심 정렬 (발 위치 고정)
- [ ] 8-12 FPS 도트 감성

### ✅ Unity 통합
- [ ] Filter Mode: Point (필수!)
- [ ] Compression: None
- [ ] Pixel Perfect Camera 설정
- [ ] Sprite 크기 일관성

---

## 🐍 Python 로컬 픽셀 변환기 (직접 제작)

위키 저장소에 포함된 완전 무료 Python 스크립트

### 특징
- ✅ 완전 오프라인 동작
- ✅ 배치 처리 (폴더 일괄 변환)
- ✅ 4가지 프리셋 팔레트 (PICO-8, NES, Game Boy, Sweetie-16)
- ✅ Floyd-Steinberg 디더링
- ✅ k-means 색상 축소
- ✅ 병렬 처리 지원

### 설치

```bash
cd scripts/
pip install -r requirements.txt
```

### 사용법

**단일 이미지 변환**:
```bash
# 기본 (64px, 16색)
python pixel_converter.py character.png

# PICO-8 팔레트 + 디더링
python pixel_converter.py character.png -w 64 -p pico8 -d

# 출력 경로 지정
python pixel_converter.py input.png -o output.png -w 32 -p gameboy
```

**배치 변환** (폴더 전체):
```bash
# 폴더 내 모든 이미지 변환
python batch_converter.py my_images/ -w 64 -p pico8

# 병렬 처리 8개
python batch_converter.py sprites/ -w 32 -p nes -j 8 -d
```

### 옵션

| 옵션 | 설명 | 기본값 |
|------|------|--------|
| `-w, --width` | 목표 너비 (픽셀) | 64 |
| `-c, --colors` | 색상 수 | 16 |
| `-p, --palette` | 프리셋 팔레트 (pico8/nes/gameboy/sweetie16) | - |
| `-d, --dither` | Floyd-Steinberg 디더링 | False |
| `-o, --output` | 출력 경로 | input_pixel.png |
| `-j, --jobs` | 병렬 처리 수 (배치 전용) | 4 |

### 내부 구조

```python
class PixelArtConverter:
    def convert(img, width, colors, palette, dither):
        # 1. Nearest Neighbor 리사이즈
        img = resize_nearest_neighbor(img, width)
        
        # 2-A. 팔레트 매핑 (프리셋 사용 시)
        if palette:
            img = apply_palette(img, palette_colors)
        
        # 2-B. k-means 색상 축소 (자동)
        else:
            img = quantize_colors_kmeans(img, colors)
        
        # 3. 디더링 (선택)
        if dither:
            img = floyd_steinberg_dither(img, palette)
        
        return img
```

---

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

## 🔧 트러블슈팅

### 문제: 픽셀이 흐릿하게 보임
**해결**:
```
Unity Inspector:
- Filter Mode: Point (no filter) ← 필수!
- Compression: None
- Generate Mip Maps: 체크 해제
```

### 문제: 프레임 간 색상이 다름
**해결**:
- True Pixel에서 "Shared Palette" 활성화
- Aseprite에서 팔레트 고정 후 Indexed Color 모드

### 문제: 애니메이션 떨림 (jitter)
**해결**:
- 스프라이트 Pivot을 캐릭터 발 위치로 통일
- Pixel Perfect Camera 사용
- 프레임별 중심점 정렬 (Aseprite에서 수동 조정)

### 문제: 배경 제거 후 외곽선 노이즈
**해결**:
- True Pixel "Edge Chroma Cleanup" 활성화
- 원본 생성 시 고대비 배경 사용 (순백/순흑)
- Aseprite에서 Magic Wand + Delete로 수동 정리

---

## 💡 프로 팁

### 1. 팔레트 일관성
```
첫 캐릭터 제작 시 팔레트를 정의하고 
모든 에셋에 재사용 → 통일된 비주얼
```

### 2. 참조 스프라이트
```
좋아하는 도트 게임 스프라이트를 
GPT 프롬프트에 스타일 참조로 첨부
```

### 3. 해상도 선택
- **16x16**: 초미니멀 (테라리아 스타일)
- **32x32**: 균형잡힌 디테일 (스타듀밸리)
- **64x64**: 고디테일 (하데스 2D)

### 4. 애니메이션 프레임 수
- **Idle**: 4-6 프레임
- **Walk**: 6-8 프레임
- **Run**: 6-8 프레임
- **Jump**: 3-4 프레임 (상승-최고점-하강)
- **Attack**: 4-6 프레임

### 5. Unity에서 FPS 조정
```csharp
// Animator에서 Speed 조정
animator.speed = 0.8f; // 느린 도트 감성
```

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
