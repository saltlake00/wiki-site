---
title: 픽셀아트 변환기 고급 기능 가이드
created: 2026-08-18
updated: 2026-08-20
type: guide
status: active
tags: [개발, 도구]
sources:
  - projects/gamedev/pixel-sprite-workflow/scripts/README.md
---

# 픽셀아트 변환기 고급 기능 가이드

## 🚀 고급 기능

### 다운스케일 방법

#### nearest (기본)
- 가장 선명한 픽셀 경계
- 전통적인 픽셀아트 스타일

#### pixelate
- 그리드 기반 평균 색상
- 부드러운 그라디언트 보존

#### lanczos_then_nearest
- 고품질 다운스케일 후 픽셀 스냅
- 디테일과 선명도 균형

#### xbr
- 엣지 보존 알고리즘
- 부드러운 곡선 유지

### 디더링 방법

#### Floyd-Steinberg
- 오차 확산 디더링
- 자연스러운 그라디언트

#### Ordered (Bayer)
- 체크무늬 패턴
- 레트로 느낌

#### None
- 디더링 없음
- 깔끔한 색상 블록

### 외곽선

```bash
python advanced_converter.py character.png \
  --outline --outline-thickness 2
```

- 캐릭터 윤곽 강조
- 배경과 구분 명확

### 스무딩

```bash
python advanced_converter.py noisy.png \
  --smooth 2
```

- 노이즈 제거
- 부드러운 색상 전환

### 대비/채도 향상

```bash
python advanced_converter.py faded.png \
  --contrast 1.5 --saturation 1.3
```

- 뚜렷한 색상
- 선명한 이미지

### CRT 효과

```bash
python advanced_converter.py retro.png \
  --crt
```

- 스캔라인 추가
- 레트로 모니터 느낌

## 📋 사용 예제

### 완벽한 도트 캐릭터

```bash
python advanced_converter.py character.png \
  -w 64 -p pico8 \
  --downscale pixelate \
  --dither floyd-steinberg \
  --outline --outline-thickness 1 \
  --contrast 1.2 \
  --saturation 1.1
```

### 깔끔한 UI 아이콘

```bash
python advanced_converter.py icon.png \
  -w 32 -c 8 \
  --downscale nearest \
  --dither none \
  --smooth 1
```

### 레트로 게임 스타일

```bash
python advanced_converter.py scene.png \
  -w 128 -p nes \
  --downscale xbr \
  --dither ordered \
  --crt
```

### 고품질 스프라이트

```bash
python advanced_converter.py sprite.png \
  -w 96 -p sweetie16 \
  --downscale lanczos_then_nearest \
  --dither floyd-steinberg \
  --outline --outline-thickness 1 \
  --smooth 1 \
  --contrast 1.15
```

## 🎨 GUI 고급 설정

GUI 버전에서는 모든 고급 기능을 슬라이더와 체크박스로 제어:

- ✅ 실시간 미리보기
- ✅ 설정 초기화 버튼
- ✅ 드래그앤드롭 지원 (예정)
- ✅ 프리셋 저장/불러오기 (예정)

## 🔬 알고리즘 비교

### 다운스케일 속도

| 방법 | 속도 | 품질 | 용도 |
|------|------|------|------|
| nearest | ⚡⚡⚡ | 선명 | 전통 픽셀아트 |
| pixelate | ⚡⚡ | 균형 | 일반 이미지 |
| lanczos_then_nearest | ⚡ | 고품질 | 스프라이트 |
| xbr | ⚡ | 부드러움 | 곡선 많은 이미지 |

### 디더링 품질

| 방법 | 품질 | 속도 | 패턴 |
|------|------|------|------|
| floyd-steinberg | 최고 | 느림 | 자연스러움 |
| ordered | 중간 | 빠름 | 체크무늬 |
| none | - | 최고속 | 없음 |

## 💡 프로 팁

### 1. 계층별 처리

```bash
# 배경
python advanced_converter.py bg.png -w 256 -c 32 --smooth 2

# 캐릭터
python advanced_converter.py char.png -w 64 -p pico8 --outline

# Unity에서 레이어 합성
```

### 2. 테스트 워크플로우

```bash
# 빠른 테스트 (nearest + none)
python advanced_converter.py test.png -w 32 --dither none

# 최종 (고품질)
python advanced_converter.py test.png -w 64 -p pico8 \
  --downscale pixelate --dither floyd-steinberg --outline
```

### 3. 배치 스크립트

```bash
# 폴더 전체 고급 변환
for f in sprites/*.png; do
  python advanced_converter.py "$f" \
    -w 64 -p pico8 \
    --downscale pixelate \
    --outline --contrast 1.2
done
```

## 🐛 트러블슈팅

### 문제: 외곽선이 너무 두꺼움
```bash
--outline-thickness 1  # 기본값 낮춤
```

### 문제: 색상이 너무 어두움
```bash
--contrast 1.3  # 대비 높임
```

### 문제: 노이즈 많음
```bash
--smooth 2  # 스무딩 강화
```

### 문제: 디테일 손실
```bash
--downscale lanczos_then_nearest  # 고품질 다운스케일
--smooth 0  # 스무딩 끄기
```
