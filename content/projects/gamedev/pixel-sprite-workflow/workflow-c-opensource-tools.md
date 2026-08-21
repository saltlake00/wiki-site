---
title: 워크플로우 C — 오픈소스 픽셀 변환 도구
description: Image-to-Pixel, Pixel-Perfect-AI-Art-Converter, wdot, SpriteFusion, PixelAfterAll 비교
created: 2026-08-18
updated: 2026-08-21
type: guide
status: active
sources: []
tags: [개발, 게임, Unity, 도구, AI/ML]
---

# 워크플로우 C — 오픈소스 픽셀 변환 도구

> **판단**: 직접 만든 로컬 변환기가 있으므로 **이 도구들은 결과 비교용 기준선**으로 쓴다. 유료인 PixelAfterAll만 품질 우위가 뚜렷하다.
> **다음**: 로컬 변환기 결과가 애매할 때 같은 원본을 여기 도구에 넣어 비교한다.

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

## 관련

- [[projects/gamedev/pixel-sprite-workflow/index|워크플로우 개요]] — 전체 파이프라인과 옵션 선택
- [[projects/gamedev/pixel-sprite-workflow/scripts/README|스크립트 가이드]] — 직접 만든 로컬 변환기
- [[projects/gamedev/pixel-sprite-workflow/scripts/ADVANCED|고급 기능 가이드]]