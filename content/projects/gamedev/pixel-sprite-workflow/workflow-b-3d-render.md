---
title: 워크플로우 B — 3D 모델 → 픽셀아트 (던파 방식)
description: Blender 자동 렌더로 프로토타입, 3D 가이드 + 수작업으로 고품질. 던파 그래픽팀 방식
created: 2026-08-18
updated: 2026-08-21
type: guide
status: active
sources: []
tags: [개발, 게임, Unity, 도구, AI/ML]
---

# 워크플로우 B — 3D 모델 → 픽셀아트

> **판단**: **프레임 간 일관성이 가장 좋은 경로.** 대신 3D 셋업 비용이 든다. 자동 렌더는 프로토타입까지, 최종 품질은 3D를 가이드로만 쓰고 수작업으로 마무리하는 던파 방식이다.
> **다음**: 캐릭터 하나로 자동 렌더를 먼저 시험해 일관성 이득이 셋업 비용을 넘는지 확인한다.

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

## 관련

- [[projects/gamedev/pixel-sprite-workflow/index|워크플로우 개요]] — 전체 파이프라인과 옵션 선택
- [[projects/gamedev/pixel-sprite-workflow/workflow-a-ai-image|워크플로우 A]] — 진입 비용이 낮은 기본 경로
- [[projects/gamedev/pixel-sprite-workflow/troubleshooting|품질·트러블슈팅]]