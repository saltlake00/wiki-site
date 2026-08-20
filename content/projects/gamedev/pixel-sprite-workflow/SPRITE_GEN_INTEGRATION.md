---
title: sprite-gen 통합 가이드
created: 2026-08-19
updated: 2026-08-20
type: guide
status: active
tags: [개발, 도구]
sources:
  - projects/gamedev/pixel-sprite-workflow/index.md
---

# sprite-gen 통합 테스트 결과

## ✅ 설치 완료

**위치**: `C:\Users\KGA01\Documents\위키-참고자료\sprite-gen` (2026-08-20부터 — 이전엔 위키 폴더 안에 있었으나 외부 git clone+venv라서 위키 git 저장소 밖으로 이동)

**설치된 것**:
- sprite-gen 1.59.0
- Pillow 12.3.0
- NumPy 2.5.2
- Python 가상환경 (.venv)

## 🧪 통합 테스트 결과

### Test 1: 우리 변환기 → sprite-gen cutout

**파이프라인**:
```
원본 이미지 (128×192)
    ↓ [우리 픽셀아트 변환기]
픽셀아트 (64×96, 16색)
    ↓ [sprite-gen cutout --key auto]
투명 배경 픽셀아트 (74.67% 투명)
```

**명령어**:
```bash
# 1. 픽셀아트 변환
cd scripts
python3 advanced_converter.py \
  "../sprite-gen/tests/fixtures/moe/moe_green.png" \
  -o test_pixel.png \
  -w 64 -c 16

# 2. 배경 제거
cd ../sprite-gen
.venv/Scripts/python -m sprite_gen.cli cutout \
  "../scripts/test_pixel.png" \
  --key auto \
  --out ../scripts/test_pixel_cutout.png \
  --white-check
```

**결과**:
- ✅ 자동 크로마 키 감지 (마젠타)
- ✅ 배경 완전 제거 (74.67% 투명)
- ✅ 검증 이미지 생성 (cyan/magenta/yellow)

---

## 💡 통합 가능성 분석

### 🟢 즉시 통합 가능
1. **cutout (배경 제거)** ⭐⭐⭐
   - 단일 명령으로 실행
   - 자동 크로마 키 감지
   - JSON 결과 출력
   
### 🟡 중기 통합 가능
2. **extract (프레임 추출)**
   - 런 디렉터리 구조 필요
   - 우리 GIF → 프레임 추출 → extract → 정리

3. **compose-atlas (스프라이트시트)**
   - 매니페스트 생성
   - Unity/Godot 호환

### 🔴 장기 통합 (선택적)
4. **curation (웹 큐레이터)**
   - 별도 웹 서버 필요
   - 우리 웹 GUI와 중복
   
5. **breathe (호흡 효과)**
   - 고급 기능
   - 게임 개발자용

---

## 🚀 추천 통합 순서

### Phase 1: cutout 통합 (1시간)
```python
# web_gui.py에 추가
@app.route('/remove-background', methods=['POST'])
def remove_background():
    import subprocess
    from pathlib import Path
    
    sprite_gen_root = Path(__file__).parent.parent / 'sprite-gen'
    python_exe = sprite_gen_root / '.venv' / 'Scripts' / 'python'
    
    result = subprocess.run([
        str(python_exe),
        '-m', 'sprite_gen.cli', 'cutout',
        input_path,
        '--key', 'auto',
        '--out', output_path
    ], capture_output=True, text=True)
    
    result_json = json.loads(result.stdout)
    return jsonify(result_json)
```

**웹 UI 추가**:
```html
<div class="checkbox-group">
    <input type="checkbox" id="removeBg">
    <label for="removeBg">🧹 배경 제거 (sprite-gen cutout)</label>
</div>
```

### Phase 2: 스프라이트시트 출력 (반나절)
- GIF 프레임 → extract → compose-atlas
- manifest.json 생성
- Unity/Godot 호환

### Phase 3: 고급 기능 (선택적)
- 팔레트 스왑 (recolor)
- 백본 격자 (픽셀 스냅)

---

## 📊 성능 비교

| 기능 | 우리 구현 | sprite-gen | 통합 추천 |
|------|-----------|-----------|-----------|
| 픽셀아트 변환 | ✅ 8배/가변 | ❌ | 우리 유지 |
| GIF 애니메이션 | ✅ 전체 프레임 | ❌ | 우리 유지 |
| 배경 제거 | ❌ | ✅ 크로마 키 | **통합** ⭐ |
| 픽셀 스냅 | ⚠️ 기본 | ✅ 백본 격자 | **통합** ⭐ |
| 스프라이트시트 | ❌ | ✅ manifest.json | **통합** ⭐ |
| 웹 UI | ✅ Flask | ✅ 별도 서버 | 우리 유지 |

---

## 🎯 최종 권장 사항

**즉시 구현**:
1. ✅ cutout 통합 (배경 제거)
2. ✅ sprite-gen 실행 경로 설정

**중기 고려**:
3. 스프라이트시트 + manifest.json
4. 픽셀 스냅 (백본 격자)

**장기/선택적**:
5. 팔레트 스왑
6. 호흡 효과

---

## 🛠️ 설치 가이드 (다른 환경)

```bash
# 1. sprite-gen 클론
git clone https://github.com/aldegad/sprite-gen.git

# 2. 가상환경 + 설치
cd sprite-gen
python3 -m venv .venv
.venv/Scripts/python -m pip install -e .

# 3. 테스트
.venv/Scripts/python -m sprite_gen.cli --help
```

---

## 📝 라이선스
- sprite-gen: Apache-2.0
- 우리 프로젝트: 호환 가능
