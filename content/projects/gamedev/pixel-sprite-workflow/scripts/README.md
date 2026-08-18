# 픽셀아트 변환기 (Pixel Art Converter)

AI 생성 이미지와 비디오를 True Pixel Art로 변환하는 Python 도구

## 설치

```bash
pip install -r requirements.txt
```

## 사용법

### 단일 이미지 변환

```bash
# 기본 변환 (64px, 16색)
python pixel_converter.py input.png

# 사이즈와 색상 지정
python pixel_converter.py input.png -w 32 -c 8

# PICO-8 팔레트 사용
python pixel_converter.py input.png -p pico8

# 디더링 적용
python pixel_converter.py input.png -p pico8 -d

# 출력 경로 지정
python pixel_converter.py input.png -o output.png -w 64 -p sweetie16
```

### 배치 변환

```bash
# 폴더 내 모든 이미지 변환
python batch_converter.py my_images/

# 출력 폴더 지정
python batch_converter.py my_images/ -o pixel_output/

# 병렬 처리 (8개 동시)
python batch_converter.py my_images/ -w 64 -p nes -j 8
```

## 옵션

### 공통 옵션

- `-w, --width`: 목표 너비 (픽셀) [기본: 64]
- `-c, --colors`: 색상 수 [기본: 16]
- `-p, --palette`: 프리셋 팔레트 (`pico8`, `nes`, `gameboy`, `sweetie16`)
- `-d, --dither`: Floyd-Steinberg 디더링 적용
- `-o, --output`: 출력 경로

### 배치 전용

- `-j, --jobs`: 병렬 처리 수 [기본: 4]

## 팔레트

### PICO-8 (16색)
레트로 판타지 콘솔 팔레트

### NES (54색)
닌텐도 패미컴 팔레트

### Game Boy (4색)
초록 모노크롬

### Sweetie-16 (16색)
현대적 픽셀아트 팔레트

### 비디오 → 스프라이트시트

```bash
# 기본 (8 FPS, 64px, 16색)
python video_to_spritesheet.py walk.mp4

# PICO-8 스타일 + 배경 제거
python video_to_spritesheet.py character.mp4 -fps 12 -w 64 -p pico8 --remove-bg

# 고해상도, 8x3 그리드
python video_to_spritesheet.py attack.mp4 -fps 10 -w 128 -c 32 --columns 8

# NES 팔레트 + 디더링, 최대 24프레임
python video_to_spritesheet.py jump.mp4 -p nes -d --max-frames 24
```

## 예제

```bash
# GPT 이미지 → 64x64 PICO-8 스타일
python pixel_converter.py character.png -w 64 -p pico8 -d

# 폴더 일괄 변환 (32px, Game Boy 스타일)
python batch_converter.py sprites/ -w 32 -p gameboy -j 8

# AI 비디오 → 픽셀 스프라이트시트 (자동 배경 제거)
python video_to_spritesheet.py walk_animation.mp4 -fps 8 -w 64 -p pico8 --remove-bg
```

## Unity 통합

변환된 이미지를 Unity에 임포트할 때:

```
Inspector 설정:
- Texture Type: Sprite (2D and UI)
- Filter Mode: Point (no filter) ← 필수!
- Compression: None
- Sprite Mode: Single 또는 Multiple
```

## 라이선스

MIT License
