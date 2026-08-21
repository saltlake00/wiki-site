---
title: VARCO 3D 워크플로우 템플릿 — 이미지 부품 분리 (Parts from Image)
description: 열려 있는 VARCO 3D "Parts from Image" 템플릿의 노드·엣지·프롬프트 전체 구조 — 하나의 이미지를 8개 부품으로 분리해 각각 3D 모델로 생성하는 재사용 가능한 워크플로우
created: 2026-08-21
updated: 2026-08-21
type: howto
status: active
sources: [varco-3d live workflow]
tags: [개발, 게임, Unity, AI/ML, 도구, VARCO-3D]
card_title: 🧩 VARCO 3D 부품 분리 템플릿
card_description: 이미지를 8개 부품으로 분리해 3D 모델 생성 (재사용 워크플로우)
card_icon: 🧩
card_color: "#10B981"
---

# VARCO 3D 워크플로우 템플릿 — Parts from Image (이미지 부품 분리)

> **판단**: 이 워크플로우는 **부품 분리 → 각 부품 3D 생성**의 재사용 템플릿으로, 게임 캐릭터·차량·크리처처럼 여러 구조물로 이루어진 에셋을 하나의 레퍼런스 이미지에서 통째로 뽑아내고 싶을 때 쓴다. **모델의 중복 부분(좌우 팔/다리 등)은 대표 1개만 뽑고, 텍스트(글자·문양·로고)는 전부 제외**하도록 프롬프트가 설계되어 있다. Generate3D 노드들은 아직 연결·실행되지 않은 상태(이미지 → 3D 변환 단계에서 멈춰 있음).

이 문서는 실제로 브라우저에 열려 있던 VARCO 3D 커스텀 워크플로우("Untitled", workflowId `692f09c6-8157-428d-8f62-5c63c90f8bc9`)의 **노드·엣지 구조와 전체 프롬프트를 그대로 기록**한 것이다. 새 에셋을 만들 때 이 템플릿을 그대로 재현하거나, 프롬프트만 교체해 재사용한다.

## 📌 이 워크플로우가 하는 일 (개요)

1. **레퍼런스 이미지 1장** 입력 → "Parts from Image" 템플릿
2. AI가 주제의 **핵심 대형 구조물 8개 부품**을 식별 → 8개 독립 프롬프트로 분해
3. 각 부품을 **독립된 3D 에셋**으로 만들 수 있도록 **단독 이미지** 1장씩 생성
4. 각 부품 이미지 → **Generate3D** 노드로 3D 모델 변환 (이번 세션에서는 여기서 멈춤)

이 방식은 NC 강의에서도 언급된 "**파츠별 생성 후 조합**" 전략과 정확히 일치한다 (현업 3D 아티스트가 이미지들을 따로 뽑아 파츠로 조합해 캐릭터를 만드는 방식).

## 🗂️ 노드 구성 (유형별 21개)

| 유형 | 개수 | 역할 |
|------|------|------|
| `ImageInput` | 1 | 레퍼런스 이미지 입력 (원본 객체 사진) |
| `TextInput` | 1 | 마스터 분리 프롬프트 (8개 부품 식별 규칙) |
| `AIAssistant` | 9 | (1) 부품 목록 생성 + (8) 각 부품 추출 |
| `GenerateImage` | 8 | 부품별 단독 이미지 생성 |
| `Generate3D` | 8 | 부품 이미지 → 3D 모델 (현재 empty) |
| `Annotation` | 1 | 사용법 안내 라벨 ("Parts from Image") |

## 🔗 데이터 흐름 (엣지 구조)

```
ImageInput (원본)
   ├─ reference → 8× GenerateImage      (각 부품 생성 시 원본 참조)
   └─ reference → 부품목록 AIAssistant

TextInput (분리 마스크 프롬프트)
   └─ prompt → 부품목록 AIAssistant

부품목록 AIAssistant (8개 프롬프트 번호 목록)
   ├─ out → 8× 부품 추출 AIAssistant (referenceText)
   │
   ├─ 각 추출 AIAssistant.out → 해당 GenerateImage.prompt
   ├─ 각 GenerateImage.out → 해당 Generate3D.image
   └─ (원본 이미지가 8× GenerateImage에 reference로도 공급)
```

**핵심 패턴**: 하나의 마스크 프롬프트로 목록을 만든 뒤, 목록을 **8개로 복제**해 각 추출기(AIAssistant)가 "목록 중 item N만 뽑아라"고 지시 → 각자 독립된 부품 이미지 생성. → **N당 1 파이프라인**이 병렬로 구성된다.

---

## 📝 핵심 프롬프트 (그대로 재사용 가능)

### 1. 분리 마스크 프롬프트 (TextInput → 부품목록 AI)

```
Using the provided reference image as the only source, identify exactly 8 essential large-scale parts
of the main subject for 3D asset production.

Do not generate an image. Instead, return a numbered list of 8 text prompts, where each prompt
can be used separately to generate one individual part.

Prioritize the most important and largest structural components first. Focus on parts that a
professional 3D artist would separate for production: core body sections, major limbs, large
attachments, armor pieces, equipment, outer shell sections, mechanical modules, clothing
sections, or other primary construction units.

Avoid small decorative details unless there are not enough major parts. Avoid duplicate or
near-duplicate parts. If the subject has repeated or symmetrical components, include only one
representative version unless the repeated parts are clearly different in shape, role, or design.

Do not include text-based elements as parts. Exclude letters, numbers, logos, runes, symbols,
signage, UI elements, captions, markings, or typography-like details from the selected parts and
from the generated prompts.

Each part prompt must:
* describe only one isolated part
* preserve the original subject's design language, proportions, material, color, and surface style
* avoid inventing new components
* avoid referencing the full subject as a complete object
* be suitable for generating a standalone 3D asset part
* request a clean isolated object with no labels, no text, no numbers, and no background elements

Return only the list in the following format:
1. [Part name] — [Standalone generation prompt for this part]
2. [Part name] — [Standalone generation prompt for this part]
... (8 items)
```

### 2. 부품 추출 프롬프트 (AIAssistant × 8 — item 번호만 다름)

각각 "목록에서 **item N번**만 뽑아라"가 바뀌고 나머지는 동일:

```
From the provided numbered list of 8 part-generation prompts, extract only item N.
Return the part name and its standalone generation prompt, but make sure the final prompt
explicitly instructs the generator to create only the described part, isolated from the full
subject. The output must not include the full body, full object, complete character, complete
vehicle, complete creature, or complete subject. Show only the selected part as a standalone
extracted component. Do not include surrounding body sections unless they are physically part
of the described component.
```

`N` = 1~8 (노드마다 `item N`만 다름, 8번째 노드는 `item 8`).

### 3. GenerateImage 설정 (모두 동일)

| 항목 | 값 |
|------|-----|
| `prompt` | ← 추출기 AI 출력 연결 |
| `reference` | ← 원본 이미지 연결 |
| `count` | 1 |
| `aspectRatio` | `1:1` |
| `model` | `gpt-image-2-medium` |

### 4. Generate3D (이번 세션 미실행)

`image` ← 부품 이미지 출력 연결. count=1. **실행 안 된 상태(empty)** — 이어서 이 노드들을 실행하면 각 부품의 3D 모델이 나온다.

---

## ✅ 실제 부품 분해 예시 (스타일라이즈드 록 골렘)

이 템플릿을 실행한 예시 — 참조 이미지(스타일화된 암석 골렘)에서 AI가 뽑아낸 8개 부품:

| # | 부품 | 설명 요약 |
|---|------|-----------|
| 1 | **Main Torso** | 불규칙한 암흑 회색 돌판 + 초록 이끼 + 푸른 에너지 패턴, 넓고 근육질 |
| 2 | **Head** | 암석 판 헤드, 붉은 눈, 이마에 조각 + 푸른 에너지 |
| 3 | **Upper Arm Module** | 암석 판 + 파란 수정 스파이크 |
| 4 | **Lower Arm & Hand** | 전완·주먹, 뼈의 마디에 파란 수정 클러스터 |
| 5 | **Upper Leg (thigh)** | 두꺼운 암석 판, 이끼 |
| 6 | **Lower Leg & Foot** | 넓고 강력한 발, 이끼 |
| 7 | **Waist Segment** | 허리 벨트 판, 중앙에 파란 에너지 심볼 |
| 8 | **Loincloth** | 낡은 갈색 천 헝겊 |

→ 이 8개 부품 이미지가 각각 GenerateImage로 생성 완료, 3D 변환만 남은 상태.

**프롬프트 스타일 특징**: "rocks/stone plates + moss + glowing cyan energy" 같은 **재질·색·표면 스타일이 모든 부품에 반복**되므로, 개별 부품으로 뽑아도 원본과 일관된 디자인 언어를 유지한다. → 부품 프롬프트를 짤 때 **재질·색·표면·디테일 어휘를 모든 부품에 반복시키는 것**이 핵심 요령.

---

## ♻️ 다른 에셋에 재사용하는 방법

1. **원본 이미지 교체** — `ImageInput` 노드의 이미지를 새 레퍼런스로 바꾼다.
2. **(선택) 분리 프롬프트의 개수·제약 조정** — 부품 수가 더 많으면 텍스트의 "8개"와 추출 노드 수를 같이 늘린다.
3. **Run All** 실행 → 부품 목록 → 부품 이미지 → Generate3D 실행.
4. 부품별 3D 출력은 `get_output_downloads`로 받아 Unity 프로젝트에 조립.

> **주의 (유니티 MCP 스킬에서 재확인)**: VARCO는 브라우저에 워크플로우가 열려 있어야 동작. MCP 도구가 실패하면 재시도 전에 브라우저 확인. 부품 기반 생성은 "Logic/Visual 분리 + `Visual` 자식 노드만 교체" 원칙과 잘 맞는다 — 각 부품을 독립 3D 에셋으로 만들어 조립하면 된다.

## 관련

- [[projects/gamedev/varco-3d/index|VARCO 3D MCP]] — MCP 제어 기초·도구 목록·픽셀 스프라이트 파이프라인
- [[projects/gamedev/unity-mcp-game-dev|Unity MCP 게임 개발]] — Logic/Visual 분리·부품 교체 구조
- [[projects/gamedev/ncai-varco-lecture/index|NC AI·VARCO 강의]] — 부품별 생성 전략·현업 품질 평가
