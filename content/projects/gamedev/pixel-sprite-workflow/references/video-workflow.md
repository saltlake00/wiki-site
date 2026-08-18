# AI 비디오 → 픽셀 스프라이트 워크플로우

ComfyUI/Stable Video Diffusion으로 이미지에서 애니메이션 비디오 생성 → 픽셀 스프라이트시트 변환

## 전체 파이프라인

```
1. AI 이미지 생성 (GPT/Stable Diffusion)
   ↓
2. 이미지 → 비디오 (Stable Video Diffusion)
   ↓
3. 비디오 → 픽셀 스프라이트시트 (Python 스크립트)
   ↓
4. Unity 통합
```

---

## Step 1: AI 비디오 생성 (로컬)

### ComfyUI + Stable Video Diffusion (SVD)

#### 필요 사양
- NVIDIA GPU: 8GB+ VRAM 권장
- VRAM 부족 시: 해상도/프레임 수 감소

#### 설치

```bash
# ComfyUI 설치 (기본)
git clone https://github.com/comfyanonymous/ComfyUI
cd ComfyUI
pip install -r requirements.txt

# ComfyUI Manager 설치 (필수)
cd custom_nodes
git clone https://github.com/ltdrdata/ComfyUI-Manager
```

#### 모델 다운로드

**Stable Video Diffusion**:
- **SVD**: 14프레임, 1024x576
- **SVD-XT**: 25프레임, 1024x576 (긴 애니메이션)

다운로드: https://huggingface.co/stabilityai/stable-video-diffusion-img2vid-xt

```bash
# 모델 저장 위치
ComfyUI/models/checkpoints/svd_xt.safetensors
```

#### 워크플로우

1. ComfyUI 실행
2. SVD img2vid 워크플로우 로드 (JSON 드래그앤드롭)
3. 캐릭터 이미지 업로드
4. 파라미터 조정:
   - **Motion Bucket ID**: 100-150 (움직임 강도)
   - **Augmentation Level**: 0.0-0.1 (노이즈 편차)
   - **Frame Count**: 14 또는 25
   - **FPS**: 6-12 (도트 감성)
5. Queue Prompt → 비디오 생성

---

## Step 2: 비디오 → 픽셀 스프라이트시트

### Python 스크립트 사용

```bash
# 기본 변환
python video_to_spritesheet.py walk.mp4

# 밝은 배경 자동 제거 + PICO-8 팔레트
python video_to_spritesheet.py character.mp4 \
  -fps 8 -w 64 -p pico8 --remove-bg

# 최대 16프레임만, 8열 그리드
python video_to_spritesheet.py jump.mp4 \
  -fps 12 -w 64 -p nes \
  --max-frames 16 --columns 8 -d
```

### 자동 처리 내용

1. ✅ FPS에 따라 프레임 자동 추출
2. ✅ 배경 자동 제거 (선택)
3. ✅ 프레임 크기 정규화 (발 위치 고정)
4. ✅ 각 프레임 픽셀아트 변환
5. ✅ 스프라이트시트 그리드 생성

---

## Step 3: Unity 통합

```
1. 생성된 PNG를 Unity Assets에 드래그
2. Inspector 설정:
   - Texture Type: Sprite (2D and UI)
   - Sprite Mode: Multiple
   - Filter Mode: Point (no filter) ← 필수!
   - Compression: None
3. Sprite Editor > Slice:
   - Type: Grid By Cell Size
   - Pixel Size: 64x64 (스크립트 -w 값과 동일)
4. Animation 생성
```

---

## 완전 자동화 예제

### 배치 스크립트 (Windows)

```batch
@echo off
REM AI 이미지들을 비디오로 변환하고 스프라이트시트 생성

echo === Step 1: ComfyUI로 비디오 생성 (수동) ===
echo 1. ComfyUI에서 images/ 폴더의 이미지들을 SVD로 비디오 생성
echo 2. videos/ 폴더에 저장
pause

echo.
echo === Step 2: 비디오를 스프라이트시트로 변환 ===
for %%f in (videos\*.mp4) do (
    echo 변환 중: %%f
    python video_to_spritesheet.py "%%f" ^
        -fps 8 -w 64 -p pico8 --remove-bg ^
        -o sprites\%%~nf_sprite.png
)

echo.
echo === 완료! ===
echo sprites/ 폴더 확인
pause
```

### Bash 스크립트 (Linux/Mac)

```bash
#!/bin/bash
# AI 이미지 → 비디오 → 스프라이트시트 자동화

echo "=== Step 1: ComfyUI로 비디오 생성 (수동) ==="
echo "1. ComfyUI에서 images/ 폴더의 이미지들을 SVD로 비디오 생성"
echo "2. videos/ 폴더에 저장"
read -p "완료 후 Enter..."

echo ""
echo "=== Step 2: 비디오 → 스프라이트시트 변환 ==="
mkdir -p sprites

for video in videos/*.mp4; do
    filename=$(basename "$video" .mp4)
    echo "변환 중: $video"
    python video_to_spritesheet.py "$video" \
        -fps 8 -w 64 -p pico8 --remove-bg \
        -o "sprites/${filename}_sprite.png"
done

echo ""
echo "=== 완료! sprites/ 폴더 확인 ==="
```

---

## 파라미터 가이드

### FPS 선택

| FPS | 용도 | 프레임 수 (1초) |
|-----|------|-----------------|
| 6 | 느린 도트 애니메이션 | 6 |
| 8 | 도트 게임 표준 | 8 |
| 12 | 부드러운 움직임 | 12 |
| 24 | 영화 품질 (비추천) | 24 |

### 배경 제거 임계값

```bash
# 밝은 배경 (흰색, 하늘색)
--bg-threshold 240

# 중간 밝기 배경
--bg-threshold 180

# 어두운 배경은 수동 제거 권장
```

### 그리드 레이아웃

```bash
# 자동 (정사각형에 가깝게)
# 16프레임 → 4x4

# 수평 스트립
--columns 16  # 16x1

# 8열 그리드
--columns 8   # 8x2, 8x3 등
```

---

## 트러블슈팅

### SVD 비디오 생성 실패

**문제**: VRAM 부족
```
해결:
1. 해상도 낮추기 (1024x576 → 512x288)
2. 프레임 수 감소 (25 → 14)
3. Batch Size: 1
```

**문제**: 움직임이 너무 많음/적음
```
해결:
- Motion Bucket ID 조정
  - 너무 많음: 150 → 80
  - 너무 적음: 100 → 200
```

### 배경 제거 실패

**문제**: 캐릭터 일부가 투명해짐
```
해결:
--bg-threshold 값 낮추기 (240 → 200)
또는 수동 배경 제거:
1. 비디오 편집 프로그램에서 크로마키
2. 투명 배경 비디오로 Export
```

### 프레임 떨림

**문제**: 스프라이트 크기가 프레임마다 다름
```
해결:
스크립트가 자동으로 bottom-center 정렬 처리
Unity에서 Pivot: Bottom (0.5, 0.0) 확인
```

---

## 참고 자료

### 비디오 생성
- **Stable Video Diffusion**: https://huggingface.co/stabilityai/stable-video-diffusion-img2vid-xt
- **ComfyUI**: https://github.com/comfyanonymous/ComfyUI
- **ComfyUI Manager**: https://github.com/ltdrdata/ComfyUI-Manager

### 튜토리얼
- **SVD 설정 가이드**: YouTube - MDMZ
- **ComfyUI 한국어**: YouTube - soy.lab
