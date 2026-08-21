---
title: 픽셀아트 품질 체크리스트 · 트러블슈팅 · 프로 팁
description: 변환/애니메이션/Unity 품질 확인 항목, 흐림·색 흔들림·지터·외곽선 노이즈 해결, 실전 팁
created: 2026-08-18
updated: 2026-08-21
type: guide
status: active
sources: []
tags: [개발, 게임, Unity, 도구, AI/ML]
---

# 품질 체크리스트 · 트러블슈팅 · 프로 팁

> **판단**: 증상별 원인이 대부분 **팔레트 고정 / 정수 스케일 / 프레임 수** 세 가지로 수렴한다. 새 문제를 만나면 이 셋을 먼저 확인한다.
> **다음**: 새로 겪은 증상은 여기 "트러블슈팅"에 증상→원인→수정 순으로 덧붙인다.

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

## 관련

- [[projects/gamedev/pixel-sprite-workflow/index|워크플로우 개요]] — 전체 파이프라인과 옵션 선택
- [[projects/gamedev/pixel-sprite-workflow/workflow-a-ai-image|워크플로우 A]]
- [[projects/gamedev/pixel-sprite-workflow/scripts/ADVANCED|고급 기능 가이드]] — 디더링·다운스케일 세부 옵션