# 픽셀아트 변환기 웹 GUI 빠른 시작

## 🚀 실행 방법

```bash
cd "G:\내 드라이브\wiki\projects\gamedev\pixel-sprite-workflow\scripts"
python3 web_gui.py
```

브라우저에서 http://localhost:5000 접속

## ✨ 주요 기능

### 1️⃣ 파일 업로드
- **드래그앤드롭**: 이미지를 화면에 드롭
- **클릭 선택**: 파일 선택 영역 클릭

지원 형식: PNG, JPG, GIF, BMP, WebP (최대 16MB)

### 2️⃣ 기본 설정

| 옵션 | 설명 | 기본값 |
|------|------|--------|
| **픽셀 너비** | 출력 이미지 가로 크기 | 64px |
| **색상 수** | 사용할 색상 개수 | 16색 |
| **팔레트** | 프리셋 색상 팔레트 | 없음 (K-means) |

### 3️⃣ 팔레트 옵션

- **없음**: K-means 클러스터링 (자동 최적화)
- **PICO-8**: 레트로 판타지 콘솔 (16색)
- **NES**: 닌텐도 패미컴 (54색)
- **Game Boy**: 초록 모노크롬 (4색)
- **Sweetie-16**: 현대 픽셀아트 (16색)
- **CGA**: IBM CGA (16색)

### 4️⃣ 고급 설정

#### 다운스케일 방법
- **Nearest**: 가장 선명한 픽셀 경계 (권장)
- **Pixelate**: 그리드 기반 평균 색상
- **Lanczos + Nearest**: 고품질 다운 후 스냅

#### 디더링
- **Floyd-Steinberg**: 오차 확산 (부드러운 그라디언트)
- **Ordered (Bayer)**: 패턴 기반 (빠른 처리)
- **없음**: 디더링 없음

#### 이미지 조정
- **대비**: 0.5 ~ 2.0 (1.0 = 원본)
- **채도**: 0.5 ~ 2.0 (1.0 = 원본)

#### 특수 효과
- **외곽선 추가**: 검은 테두리 (만화 스타일)
- **CRT 스캔라인**: 레트로 모니터 효과

### 5️⃣ 변환 및 다운로드

1. **✨ 변환** 버튼 클릭
2. 원본 ↔ 결과 비교 확인
3. **💾 다운로드** 버튼으로 저장

## 🎨 추천 프리셋

### 레트로 게임 (PICO-8)
```
픽셀 너비: 64px
색상 수: 16
팔레트: PICO-8
디더링: Floyd-Steinberg
```

### 만화/애니메이션 (외곽선)
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

### 고품질 픽셀아트
```
픽셀 너비: 128px
색상 수: 64
다운스케일: Lanczos + Nearest
디더링: Floyd-Steinberg
```

## 🛠️ Unity 통합

변환된 이미지를 Unity에서 사용할 때:

```
Inspector 설정:
✓ Texture Type: Sprite (2D and UI)
✓ Filter Mode: Point (no filter) ← 필수!
✓ Compression: None
✓ Max Size: 원본 크기 유지
```

## 🚫 문제 해결

### 서버가 시작되지 않을 때
```bash
# Flask 재설치
pip install --user flask

# 포트가 사용 중이면
python3 web_gui.py  # 자동으로 다른 포트 선택
```

### 업로드가 안 될 때
- 파일 크기 16MB 이하 확인
- 지원 형식 확인: PNG, JPG, GIF, BMP, WebP

### 변환이 느릴 때
- 픽셀 너비를 낮춤 (32px, 48px)
- 색상 수를 줄임 (8색, 12색)
- 다운스케일: Nearest 선택

## 📝 서버 종료

터미널에서 `Ctrl+C` 또는 프로세스 종료
