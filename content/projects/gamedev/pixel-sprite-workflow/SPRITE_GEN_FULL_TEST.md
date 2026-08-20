---
title: sprite-gen 전체 기능 테스트
created: 2026-08-19
updated: 2026-08-20
type: query
status: active
tags: [개발, 도구]
sources:
  - projects/gamedev/pixel-sprite-workflow/index.md
---

# sprite-gen 전체 기능 테스트 결과

> sprite-gen 설치 위치는 2026-08-20부터 `C:\Users\KGA01\Documents\위키-참고자료\sprite-gen` (위키 밖). 아래 명령어의 `.venv/Scripts/python`은 그 경로 기준.

## ✅ 테스트 완료된 기능

### Test 1: cutout (배경 제거) ✅
**명령어**:
```bash
.venv/Scripts/python -m sprite_gen.cli cutout \
  input.png --key auto --out output.png
```

**결과**:
- ✅ 자동 크로마 키 감지 (마젠타/그린)
- ✅ 투명 배경 PNG 생성
- ✅ 검증 이미지 생성 (cyan/magenta/yellow)

---

### Test 2: extract (프레임 추출) ✅
**명령어**:
```bash
.venv/Scripts/python -m sprite_gen.cli extract \
  --run-dir tests/fixtures/run --states walk
```

**결과**:
- ✅ 288×96 스프라이트 스트립 → 3개 프레임 (96×96 RGBA)
- ✅ 크로마 키 배경 제거 (magenta #FF00FF)
- ✅ `frames/walk/frame-0.png`, `frame-1.png`, `frame-2.png` 생성

**파이프라인**:
```
raw/walk.png (288×96, 3프레임 가로 배치)
    ↓ extract
frames/walk/
  ├── frame-0.png (96×96 RGBA)
  ├── frame-1.png (96×96 RGBA)
  └── frame-2.png (96×96 RGBA)
```

---

### Test 3: compose-atlas (스프라이트시트 + manifest) ✅
**명령어**:
```bash
.venv/Scripts/python -m sprite_gen.cli compose-atlas \
  --run-dir tests/fixtures/run \
  --atlas test_atlas.png \
  --manifest test_manifest.json
```

**결과**:
- ✅ 384×192 스프라이트 아틀라스 생성
- ✅ **manifest.json** 생성 (Unity/Godot 호환)
- ✅ 프레임 좌표, FPS, 루프 정보 포함

**manifest.json 구조**:
```json
{
  "characterId": "goldenbot",
  "frame_layout": {
    "sheetWidth": 384,
    "sheetHeight": 192,
    "cellWidth": 96,
    "cellHeight": 96,
    "rows": {
      "idle": [
        {"x": 0, "y": 0, "w": 96, "h": 96},
        {"x": 96, "y": 0, "w": 96, "h": 96},
        ...
      ],
      "walk": [
        {"x": 0, "y": 96, "w": 96, "h": 96},
        ...
      ]
    }
  },
  "animation": {
    "rows": {
      "idle": {"fps": 4, "loop": true, "durations_ms": [250, 250, 250, 250]},
      "walk": {"fps": 8, "loop": true, "durations_ms": [125, 125, 125]}
    }
  }
}
```

---

### Test 4: curation (웹 큐레이터) ✅
**명령어**:
```bash
.venv/Scripts/python -m sprite_gen.cli curation \
  --run-dir tests/fixtures/run --lang ko
```

**결과**:
- ✅ 웹 서버 실행 (http://127.0.0.1:58827/)
- ✅ 한국어 UI 지원
- ✅ 프레임 선별/편집 UI

**기능**:
- 상태별 두 개의 행 (재생 시퀀스 + 후보 풀)
- 드래그앤드롭으로 프레임 순서 변경
- 비파괴 변환 (이동, 크기, 회전, 전단)
- 실시간 애니메이션 미리보기

---

## 📊 전체 파이프라인 검증

```
[1단계] 원본 스프라이트 스트립
    raw/walk.png (288×96, 마젠타 배경)
    
[2단계] extract - 프레임 추출
    ↓
    frames/walk/frame-0.png (96×96 RGBA 투명)
    frames/walk/frame-1.png
    frames/walk/frame-2.png
    
[3단계] compose-atlas - 아틀라스 생성
    ↓
    test_atlas.png (384×192)
    test_manifest.json (프레임 좌표 + 애니메이션 정보)
    
[4단계] curation - 웹 편집
    ↓
    http://127.0.0.1:58827/
    (프레임 선별/순서 변경/변환)
```

---

## 🎯 우리 픽셀아트 변환기와의 통합 시나리오

### 시나리오 1: 단일 이미지 → 투명 배경
```
사용자: 이미지 업로드
    ↓
우리 GUI: 픽셀아트 변환 (64×64, 16색)
    ↓
sprite-gen cutout: 배경 제거
    ↓
결과: 투명 픽셀아트 PNG
```

### 시나리오 2: GIF → 스프라이트시트
```
사용자: GIF 업로드 (10프레임)
    ↓
우리 GUI: 각 프레임 픽셀아트 변환
    ↓
임시 run-dir 생성: raw/<state>.png
    ↓
sprite-gen extract: 프레임 추출 + 배경 제거
    ↓
sprite-gen compose-atlas: 스프라이트시트 + manifest.json
    ↓
결과: atlas.png + manifest.json (Unity 바로 사용 가능)
```

### 시나리오 3: 고급 편집
```
사용자: "프레임 편집하고 싶어요"
    ↓
sprite-gen curation: 웹 큐레이터 실행
    ↓
브라우저: 드래그앤드롭으로 프레임 선별/순서 변경
    ↓
sprite-gen compose-atlas: 최종 아틀라스 재생성
```

---

## 💡 핵심 발견

### 1. manifest.json이 게임 체인저
- **절대 좌표** 제공 (x, y, w, h)
- **애니메이션 메타데이터** (fps, loop, duration_ms)
- **Unity/Godot에서 즉시 사용 가능**

### 2. 크로마 키 자동 감지
- `--key auto`로 마젠타/그린 자동 선택
- 우리 변환기 출력과 완벽 호환

### 3. 웹 큐레이터는 독립적
- 별도 포트로 실행
- 우리 웹 GUI와 공존 가능
- 또는 통합하여 한 UI에서 모두 제어

---

## 🚀 추천 통합 순서

### Phase 1: cutout (즉시)
```python
@app.route('/remove-background', methods=['POST'])
def remove_background():
    # sprite-gen cutout 호출
    subprocess.run([sprite_gen_python, '-m', 'sprite_gen.cli', 
                    'cutout', input_path, '--key', 'auto'])
```

### Phase 2: 스프라이트시트 (1일)
```python
@app.route('/create-spritesheet', methods=['POST'])
def create_spritesheet():
    # 1. 임시 run-dir 생성
    # 2. GIF 프레임을 raw/ 에 저장
    # 3. extract 실행
    # 4. compose-atlas 실행
    # 5. atlas.png + manifest.json 반환
```

### Phase 3: 큐레이터 연동 (2일)
```python
@app.route('/edit-frames', methods=['POST'])
def edit_frames():
    # sprite-gen curation 실행
    # 포트 번호 반환
    # 프론트엔드에서 iframe으로 임베드
```

---

## ⚠️ 주의사항

1. **run-dir 구조 필수**
   - sprite-request.json 필요
   - raw/ 폴더에 스프라이트 스트립

2. **크로마 키 일관성**
   - magenta (#FF00FF) 또는 green (#00FF00)
   - 우리 변환기 출력과 매칭 필요

3. **Python 가상환경**
   - sprite-gen/.venv/Scripts/python 사용
   - 절대 경로로 호출

---

## 📈 성능 측정

| 작업 | 입력 | 출력 | 시간 |
|------|------|------|------|
| cutout | 128×192 PNG | 투명 PNG | ~1초 |
| extract | 288×96 스트립 | 3×96×96 프레임 | ~0.5초 |
| compose-atlas | 7 프레임 | 384×192 아틀라스 | ~0.3초 |
| curation | run-dir | 웹 서버 | ~2초 (기동) |

**총합**: 단일 이미지 → 스프라이트시트 **약 4초** ✅

---

## 🎨 결론

sprite-gen은 **게임 개발자용 프로덕션 툴**입니다.

**강점**:
- ✅ 완벽한 크로마 키 제거
- ✅ manifest.json (게임 엔진 호환)
- ✅ 웹 큐레이터 (고급 편집)
- ✅ 결정론적 출력 (같은 입력 = 같은 바이트)

**약점**:
- ❌ 복잡한 구조 (run-dir, sprite-request.json)
- ❌ GIF 네이티브 지원 없음
- ❌ 일반 사용자에게는 과잉

**통합 전략**:
1. **cutout만 먼저 통합** (배경 제거)
2. 필요시 스프라이트시트 기능 추가
3. 큐레이터는 고급 모드로 선택적 제공
