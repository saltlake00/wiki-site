---
title: Unity 게임개발용 클로드 시작 프롬프트 템플릿
description: 어떤 Unity 게임이든 재사용 가능한 범용 시작 프롬프트 — 프로젝트 확정 제약(URP, New Input System, VARCO 분리) 포함
created: 2026-08-20
updated: 2026-08-21
type: guide
status: active
sources: []
tags: [개발, 게임, Unity, 프롬프트, 도구]
card_title: 📋 Unity 게임개발 클로드 프롬프트
card_description: 어떤 게임이든 그대로 쓰는 범용 시작 프롬프트
card_icon: 📋
card_color: "#F59E0B"
---

# Unity 게임개발용 클로드 시작 프롬프트 템플릿

> **판단**: 이 계정 Unity 프로젝트의 **확정 제약을 프롬프트에 미리 박아두는 것**이 이 템플릿의 요점이다 (URP/Lit, New Input System 전용, InputSystemUIInputModule). 이걸 빼면 매번 같은 함정 — 마젠타 머티리얼, UI 클릭 무반응 — 에 다시 빠진다.
> **다음**: 새 게임을 시작할 때 이 템플릿으로 시작하고, **새로 겪은 함정은 `[사전 확인]` 절에 추가**한다.

어떤 Unity 게임이든 그대로 쓸 수 있는 **범용 시작 프롬프트**. `GameBootstrap` 코드 생성 방식, VARCO 3D 연동, 이 계정 Unity 프로젝트의 확정 제약을 미리 박아뒀다.

## 📄 템플릿 본문

`{{ 이 칸 채우기 }}`로 표시된 부분만 게임에 맞게 바꾸면 된다.

```markdown
Unity에서 [게임 이름]를 만들어줘.

## [사전 확인]
먼저 현재 프로젝트 구조, 기존 오브젝트, 스크립트, Input 방식(레거시 Input Manager인지 새 Input System인지), Console Error를 확인한 뒤 기존 기능을 최대한 유지하면서 작업해줘. 프로젝트의 Active Input Handling 설정에 맞는 입력 방식을 사용해줘.

아래는 이 계정 Unity 프로젝트의 확정 제약이니 사전 확인과 관계없이 반드시 지켜줘.
- Unity 6000.3.21f1, URP 17.3. 코드로 머티리얼을 만들 때 Shader.Find("Standard")를 쓰면 전부 마젠타가 된다. 반드시 Universal Render Pipeline/Lit을 써줘.
- Active Input Handling = 1 (New Input System 전용). 레거시 Input.*를 호출하면 InvalidOperationException이 난다. UnityEngine.InputSystem의 Mouse.current/Keyboard.current를 쓰거나 UI 이벤트만 사용해줘.
- EventSystem을 코드로 만들 때 InputSystemUIInputModule을 붙여줘. StandaloneInputModule을 붙이면 UI 클릭이 전부 무반응이 된다.
- 3D 오브젝트 호버는 UI 이벤트가 안 오므로 Physics.Raycast + 마우스 포지션을 써줘.
- 한자/특수문자 텍스트는 기본 TMP 폰트에 글리프가 없을 수 있어. 확인해보고 없으면 폴백하거나 방법을 알려줘. 두부(□)로 깨진 채 넘어가지 마.
- 새 패키지는 추가하지 마. TextMeshPro Essentials가 없으면 기본 Text로 폴백하거나 임포트 방법을 알려줘.

## [작업 방식]
- "{{ 씬 이름 }}"이라는 새 씬을 만들어 작업하고, 기존 씬은 수정하지 마.
- 씬 오브젝트를 수동 배치하지 말고, GameBootstrap 스크립트 하나가 실행 시점에 게임 전체(플레이어·세계·스포너·UI·카메라 리그)를 코드로 생성하도록 해줘. 씬에는 GameBootstrap이 붙은 빈 오브젝트와 카메라, 라이트만 있으면 되게.
- UI 텍스트는 코드로 생성하고, TMP 없으면 기본 UI로 대체하거나 임포트 방법을 안내해줘.

## [게임 요구사항]
{{ 핵심 게임 루프와 요구사항. 예: WASD 이동, 점프, GAME CLEAR, 리스폰, 높이/HP/점수 표시, 60초 생존 등 }}

## [VARCO 3D 연동 — 중요]
이 세션에는 varco-3d MCP 서버가 연결되어 있어. 나는 이후 VARCO 3D로 생성한 3D 모델을 {{ 교체할 대상 }}의 외형으로 교체할 예정이야.
- 모델 생성을 요청하면 varco-3d MCP 도구를 사용해서 생성하고, 결과 모델 파일을 Assets/Models 폴더에 임포트한 뒤 대상 오브젝트의 Visual을 교체해줘.
- varco-3d 도구 호출이 실패하면 임의로 재시도만 반복하지 말고, 내가 브라우저에 VARCO 3D 워크플로우 페이지를 열어둔 상태인지 확인하라고 안내해줘. 이 서버는 브라우저의 활성 세션으로 도구 호출을 중계하는 구조야.
- 모든 게임 오브젝트는 로직과 비주얼을 분리해줘. 부모에 Collider·Rigidbody·기능 스크립트, 실제 보이는 메시는 Visual 자식 오브젝트에.
- 스크립트는 절대 특정 Mesh나 MeshRenderer에 의존하지 마. 모델 교체는 Visual 자식만 갈아끼우고 크기·방향을 맞추면 끝나야 하고, Collider는 부모 것을 유지해줘.
- 반복 생성 개체는 프리팹 또는 생성 함수 한 곳만 고치면 전부 바뀌는 구조로. id → prefab 매핑을 한 곳에서 관리해서 모델이 0개여도 프리미티브 폴백으로 끝까지 플레이 가능하게 해줘.

## [확장성]
{{ 추가할 기능 + 원하는 스크립트 목록. 예: 경험치·레벨업·새 무기·보스·멀티샷. PlayerController, Enemy, EnemySpawner, AutoAttack, Projectile, Health, GameManager, GameUI 등 기능별 스크립트로 나눠 확장하기 쉽게 구성해줘. }}

## [제약]
최종적으로 Unity WebGL 빌드 후 itch.io에 올릴 예정이야. Web에서 문제없는 기본 Unity 기능 위주로 구현하고, 새 패키지는 추가하지 마.

## [우선순위와 검증]
화려한 기능보다 {{ 핵심 루프 요약 }}까지 전체 루프가 안정적으로 동작하는 것이 최우선이야. 구현 후 Console Error를 확인하고, 가능하면 Play 모드로 실제 동작을 확인해서 문제가 있으면 수정해줘. 직접 확인이 불가능한 부분은 내가 테스트할 체크리스트를 알려줘.
```

## ✅ 사용법

1. 이 위키 페이지 또는 템플릿 파일에서 `{{ 이 칸 채우기 }}`를 게임에 맞게 채운다.
2. 완성된 프롬프트를 Claude Code에 붙여넣거나 `claude -p "$(cat prompt.md)"`로 실행한다.
3. 이 프로젝트처럼 상세 기획이 있으면 `docs/GameDesign.md`를 읽게 하고, 프롬프트를 Day별로 쪼개 실행한다.

## 관련

- [[projects/gamedev/varco-3d/index|VARCO 3D MCP]] — VARCO 3D MCP 활용
- [[projects/gamedev/unity-2d-platformer/index|Unity 2D 플랫포머]] — Unity 2D 플랫포머 학습
- [[projects/gamedev/ncai-varco-lecture/index|NC AI·VARCO 강의 노트 (1차시)]] — 이 템플릿의 제약과 실습 맥락이 나온 수업
