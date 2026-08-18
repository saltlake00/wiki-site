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

## 📋 전체 워크플로우

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

## 🛠️ 도구 비교표

| 도구 | 용도 | 가격 | 장점 | 단점 |
|------|------|------|------|------|
| **True Pixel** | 자동 변환 | $49 일회성 | 비디오→시트 자동화, 팔레트 고정, 안정화 | 유료 |
| **Aseprite** | 수동 편집 | $19.99 | 정밀 제어, 애니메이션 도구 | 수동 작업 필요 |
| **ComfyUI** | 로컬 파이프라인 | 무료 | 오픈소스, 커스터마이징 | 설정 복잡 |
| **PixelLab** | AI 생성 | $12/월~ | 텍스트→애니메이션, 회전뷰 | 구독제 |
| **Piskel** | 온라인 편집 | 무료 | 웹 기반, 접근성 | 기능 제한 |

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

## 🚀 권장 워크플로우 (초보자용)

### 빠른 프로토타입
```
GPT 이미지 생성 
  ↓
True Pixel 자동 변환 ($49 일회성)
  ↓
Unity 임포트 (Filter Mode: Point)
```

### 고품질 제작
```
GPT 이미지 생성 (고해상도)
  ↓
비디오 생성 또는 프레임 연속 생성
  ↓
True Pixel 자동 변환
  ↓
Aseprite 수동 정리 (픽셀 보정)
  ↓
Unity 애니메이션 클립
```

### 무료 오픈소스
```
GPT 이미지 생성
  ↓
ComfyUI + Pixel Art LoRA
  ↓
Piskel 온라인 정리
  ↓
Unity 임포트
```

---

## 📚 참고 자료

### 도구 링크
- **True Pixel**: https://sorceress.games/pages/true-pixel
- **Aseprite**: https://www.aseprite.org
- **PixelLab**: https://www.pixellab.ai
- **Piskel**: https://www.piskelapp.com
- **Spritesheet Generator**: https://spritesheetgenerator.online

### 색상 팔레트
- **Lospec**: https://lospec.com/palette-list (픽셀아트 팔레트 DB)
- **PICO-8**: 16색 제한 팔레트
- **NES**: 54색 클래식 팔레트
- **Game Boy**: 4색 모노크롬

### 튜토리얼
- **Aseprite Animation Tutorial**: YouTube - Saultoons
- **Pixel Art Workflow**: DevDude.Unreal 채널
- **Unity Pixel Perfect**: Unity Learn

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
