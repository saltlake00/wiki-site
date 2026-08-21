---
title: 픽셀아트 변환기 스크립트 가이드
created: 2026-08-18
updated: 2026-08-21
type: guide
status: active
tags: [개발, 도구]
sources:
  - projects/gamedev/pixel-sprite-workflow/index.md
---

# 픽셀아트 변환기 (Pixel Art Converter)

AI 생성 이미지와 비디오를 True Pixel Art로 변환하는 Python 도구

## 🌐 **웹 GUI** (권장 ⭐⭐⭐)

브라우저 기반 픽셀아트 변환기 - 설치 없이 바로 사용!

```bash
cd scripts
python3 web_gui.py
```

브라우저에서 **http://localhost:5000** 접속

### ✨ 주요 기능

- 🌐 **브라우저 기반 UI** (모든 OS 지원)
- 🖱️ **드래그앤드롭** 업로드
- 👁️ **실시간 미리보기** (원본 ↔ 결과 비교)
- 🎬 **GIF 애니메이션 지원** (모든 프레임 자동 변환)
- 💾 **즉시 다운로드**
- ⚙️ **모든 고급 설정 지원**
  - 8가지 다운스케일 방법
  - 6종 프리셋 팔레트 (PICO-8, NES, Game Boy 등)
  - Floyd-Steinberg / Ordered 디더링
  - 대비/채도 조정
  - CRT 스캔라인 효과

### 📸 스크린샷

**이미지 업로드 시 즉시 미리보기**:
- 드롭존이 업로드한 이미지로 변경
- 파일 정보 자동 표시 (원본 크기, 예상 출력)
- 변환/초기화 버튼 바로 표시

**변환 결과**:
- 원본 ↔ 픽셀아트 나란히 비교
- GIF는 애니메이션으로 재생
- 한 번의 클릭으로 다운로드

---

## 📦 설치

```bash
pip install -r requirements.txt
```

**의존성**:
- Pillow >= 10.0.0
- NumPy >= 1.24.0
- scikit-learn >= 1.3.0
- opencv-python >= 4.8.0
- scipy >= 1.10.0
- flask >= 3.0.0 (웹 GUI)

---

## 🎨 사용법

### 웹 GUI (권장)

```bash
python3 web_gui.py
```

### 데스크톱 GUI (Tkinter)

```bash
python3 pixel_converter_gui.py
```

### CLI 버전

#### 단일 이미지 변환

```bash
# 기본 변환 (64px, 16색)
python3 pixel_converter.py input.png

# 사이즈와 색상 지정
python3 pixel_converter.py input.png -w 32 -c 8

# PICO-8 팔레트 사용
python3 pixel_converter.py input.png -p pico8

# 출력 경로 지정
python3 pixel_converter.py input.png -o output.png -w 64 -p sweetie16
```

#### 고급 옵션

```bash
python3 advanced_converter.py input.png \
  -w 64 -c 16 -p pico8 \
  --downscale pixelate \
  --dither floyd-steinberg \
  --outline \
  --contrast 1.2 \
  --crt
```

### 배치 변환

```bash
# 폴더 내 모든 이미지 변환
python3 batch_converter.py my_images/

# 병렬 처리 (8개 동시)
python3 batch_converter.py my_images/ -w 64 -p nes -j 8
```

---

## 🎮 옵션 상세

### 픽셀 너비
출력 이미지의 **가로 픽셀 개수** (비율 유지)
- 예: 64 = 64×? 픽셀 이미지
- 원본 1024×768 → 64×48

### 색상 수
사용할 색상 개수 (K-means 클러스터링)
- 4~256색
- 기본값: 16색

### 팔레트

| 팔레트 | 설명 | 색상 수 |
|--------|------|---------|
| **없음** | K-means 자동 최적화 | 사용자 지정 |
| **PICO-8** | 레트로 판타지 콘솔 | 16색 |
| **NES** | 닌텐도 패미컴 | 54색 |
| **Game Boy** | 초록 모노크롬 | 4색 |
| **Sweetie-16** | 현대 픽셀아트 | 16색 |
| **CGA** | IBM CGA | 16색 |

### 다운스케일 방법

- **Nearest**: 가장 선명한 픽셀 경계 (권장)
- **Pixelate**: 그리드 기반 평균 색상 (PAC 스타일)
- **Lanczos + Nearest**: 고품질 다운 후 픽셀 스냅

### 디더링

- **Floyd-Steinberg**: 오차 확산 (부드러운 그라디언트)
- **Ordered (Bayer)**: 패턴 기반 (빠른 처리)
- **없음**: 디더링 없음

---

## 🎬 GIF 애니메이션 지원

웹 GUI는 **모든 프레임을 자동으로 변환**합니다:

```
원본 GIF (10프레임, 512×512)
    ↓
각 프레임을 픽셀아트로 변환
    ↓
결과 GIF (10프레임, 64×64, 16색)
```

**특징**:
- ✅ 프레임 속도 유지 (duration)
- ✅ 무한 루프 유지
- ✅ 실시간 진행 상태 표시
- ✅ 애니메이션 미리보기

---

## 🎯 추천 프리셋

### 레트로 게임 (PICO-8)
```
픽셀 너비: 64px
색상 수: 16
팔레트: PICO-8
디더링: Floyd-Steinberg
```

### 만화/애니메이션
```
픽셀 너비: 128px
색상 수: 32
팔레트: 없음
외곽선: 체크
대비: 1.2
```

### Game Boy 스타일
```
픽셀 너비: 64px
팔레트: Game Boy
디더링: Ordered
CRT: 체크
```

---

## 🔧 Unity 통합

변환된 이미지를 Unity에서 사용할 때:

```
Inspector 설정:
✓ Texture Type: Sprite (2D and UI)
✓ Filter Mode: Point (no filter) ← 필수!
✓ Compression: None
✓ Max Size: 원본 크기 유지
```

---

## 🚀 고급 기능 (sprite-gen 통합)

게임 개발자를 위한 추가 기능이 준비되어 있습니다:

- 🧹 **배경 제거** (자동 크로마 키)
- 📐 **백본 격자** (진짜 픽셀아트 스냅)
- 📋 **스프라이트시트 + manifest.json** (Unity/Godot 호환)
- 🎨 **팔레트 스왑** (색상 변형)

자세한 내용: `SPRITE_GEN_FULL_TEST.md` 참조

---

## 📁 프로젝트 구조

```
scripts/
├── web_gui.py                # ⭐⭐⭐ 웹 GUI (권장)
├── templates/
│   └── index.html            # 웹 UI
├── pixel_converter_gui.py    # 데스크톱 GUI (Tkinter)
├── pixel_converter.py         # CLI 단일 변환
├── batch_converter.py         # CLI 배치 변환
├── advanced_converter.py     # 핵심 변환 엔진
├── video_to_spritesheet.py   # 비디오 → 스프라이트시트
├── requirements.txt           # 의존성
├── README.md                  # 이 파일
└── WEB_GUIDE.md              # 웹 GUI 상세 가이드
```

---

## 🔬 처리 파이프라인 (내부 순서)

**이미지 변환**:
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

**비디오 → 스프라이트시트** 🆕:
```python
class VideoToSpriteSheet:
    def convert(video, fps, width, palette):
        # 1. 프레임 추출 (FPS 조절)
        frames = extract_frames(video, target_fps=fps)
        
        # 2. 배경 제거 (선택)
        if remove_bg:
            frames = remove_background(frames)
        
        # 3. 프레임 정규화 (동일 크기, bottom-center 정렬)
        frames = normalize_frame_size(frames, anchor='bottom-center')
        
        # 4. 각 프레임 픽셀아트 변환
        pixel_frames = [
            pixel_converter.convert(f, width, palette)
            for f in frames
        ]
        
        # 5. 스프라이트시트 생성 (그리드 배열)
        sprite_sheet = create_sprite_sheet(pixel_frames, columns)
        
        return sprite_sheet
```

> 이 의사코드는 2026-08-21 허브 페이지 분할 때 유일하게 갈 곳이 없던 부분이라 여기로 옮겼다.
> **실제 구현은 `pixel_converter.py` / `video_to_spritesheet.py`가 원천**이고, 이건 코드를
> 열지 않고 순서만 확인하려는 용도다. 구현이 바뀌면 여기도 같이 고친다.

---

## 📝 라이선스

MIT License

---

## 🙏 감사

- 픽셀아트 팔레트: [Lospec](https://lospec.com/palette-list)
- 크로마 키 알고리즘: [sprite-gen](https://github.com/aldegad/sprite-gen) (Apache-2.0)

---

## 📚 추가 문서

- [[projects/gamedev/pixel-sprite-workflow/scripts/WEB_GUIDE|웹 GUI 가이드]] — 브라우저 변환기 사용법
- [[projects/gamedev/pixel-sprite-workflow/scripts/ADVANCED|고급 기능 가이드]] — 다운스케일·디더링·외곽선 세부 옵션
- [[projects/gamedev/pixel-sprite-workflow/SPRITE_GEN_INTEGRATION|sprite-gen 통합 가이드]]
- [[projects/gamedev/pixel-sprite-workflow/SPRITE_GEN_FULL_TEST|sprite-gen 전체 기능 테스트]]
- [[projects/gamedev/pixel-sprite-workflow/index|워크플로우 허브]] — 이 도구를 파이프라인 어디에서 쓰는지
