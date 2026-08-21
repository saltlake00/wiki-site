---
title: 티스토리 HTML 위젯 작성법
card_icon: 📝
card_sub: Tistory HTML
card_badge: 블로그 · HTML
card_desc: 티스토리 블로그에 HTML 위젯(인포그래픽, 비교표, 계산기, 인터랙티브 카드)을 안전하게 붙여넣는 방법. 스킨 CSS 충돌 방지, 디자인 품질, 실전 체크리스트.
created: 2026-08-18
updated: 2026-08-21
type: concept
status: active
tags: [블로그, HTML, CSS, JavaScript, 티스토리]
sources: []
confidence: high
---

# 티스토리 HTML 위젯 작성법

> **판단**: 티스토리 에디터는 iframe이 아니라 **페이지 DOM에 직접 삽입**한다. 그래서 위젯의 `body`/`html`/`:root` 규칙이 블로그 스킨 전체를 덮어쓴다 — **모든 CSS를 고유 래퍼 클래스 아래로 스코핑하는 것**이 나머지 모든 규칙의 근거다.
> **다음**: 새 위젯을 만들 때 "9가지 필수 규칙"을 체크리스트로 쓴다. 새로 겪은 스킨 충돌은 대응표에 추가한다.

> 티스토리 블로그에 HTML 위젯을 붙여넣을 때 **깨지지 않게** 만드는 방법.
> "안전하게 붙여넣기"(blog-html-embed 스킬) + "예쁘게 만들기"(claude-design 스킬)를 합친 실전 가이드.

## 핵심 원칙

티스토리 HTML 에디터는 붙여넣은 마크업을 **페이지 DOM에 직접 삽입**한다 (iframe 아님).
그래서 위젯의 `body{}`/`html{}`/`:root{}` 규칙이 **블로그 전체 스킨을 덮어쓴다.**

**→ 모든 CSS를 고유한 래퍼 클래스 아래로 스코핑해야 한다.**

## 붙여넣는 위치

1. 글쓰기 에디터에서 **"HTML" 편집 모드**로 전환
2. **비주얼/WYSIWYG 모드에 붙여넣지 말 것** — 태그가 자동 변환되어 깨짐
3. HTML 모드에서 위젯 코드 붙여넣기 → 비주얼 모드로 돌아가 미리보기 확인

## 위젯 코드 구조 (필수)

```html
<div class="mywidget2026">
  ...내용...
</div>

<style>
  .mywidget2026 { --bg:#fff; --accent:#533afd; }
  .mywidget2026 h3, .mywidget2026 p { margin:0; padding:0; }
  .mywidget2026 h3 { color:#171717 !important; }
  @import url('...pretendard.css');  /* 웹폰트는 @import로 */
</style>

<script>
(function(){
  var root = document.currentScript.closest('.mywidget2026') || document;
  // root 안에서만 쿼리
})();
</script>
```

## 9가지 필수 규칙

1. **문서 셸 제거** — `<!DOCTYPE>`, `<html>`, `<head>`, `<body>` 금지. `<div>` + `<style>` + `<script>`만
2. **고유 래퍼 클래스** — `.widget`/`.container` 같은 흔한 이름 금지. `.mywidget2026`처럼 충돌 안 나는 이름
3. **스코핑된 리셋** — 전역 `*{margin:0}` 금지. `.mywidget h1, .mywidget p {...}`처럼 쓸 태그만
4. **`!important` 의도적으로 사용** — 티스토리 스킨이 `#content h3` 같은 ID 선택자로 이기므로, 텍스트/배경/폰트에 `!important` 필수
5. **`position: sticky/fixed` 금지** — 스킨 헤더/사이드바와 겹침. static/relative 사용
6. **웹폰트는 `@import`로** — `<link>`는 에디터가 제거하지만 `<style>` 내용은 보존
7. **JS를 위젯 루트로 스코핑** — `document.currentScript.closest('.mywidget')`로 쿼리, IIFE로 감싸기
8. **시각을 위젯 안에 한정** — `min-height:100vh` 금지. 카드처럼 경계를 가진 요소로
9. **붙여넣을 위치 안내** — HTML 편집 모드, 비주얼 에디터 아님

## 디자인 품질 (claude-design 스킬 결합)

- **Surface-First**: 블로그 위젯은 대부분 **Decide/Learn**(독자 설득/전달). hero+3카드 남용 금지
- **Anti-Slop 자가진단**: 완성 후 10점 만점 점수 매기기
  - tech gradient / generic indigo / feature-tile grid / accent rail / unearned blur /
    monument stat / icon topper / center stack / default type / wrong surface
- **Content Discipline**: 가짜 지표, 장식용 통계, AI 플러프 금지
- **타이포**: Pretendard/Noto Sans KR 기본, 위젯 성격에 맞는 폰트 선택
- **색**: 브랜드 팔레트 없으면 작은 시스템 정의, WCAG 대비 확인

## 티스토리 스킨 충돌 대응표

| 증상 | 원인 | 해결 |
|------|------|------|
| 페이지 전체가 다크/라이트로 바뀜 | `body{}`/`:root{}`가 스킨 덮어씀 | 문서 셸 제거, 래퍼로 스코핑 |
| 특정 텍스트 안 보임 | 스킨 ID 선택자가 이김 | `!important` 추가 |
| 사이드바/메뉴 이상해짐 | 전역 리셋이 스킨 깨뜨림 | 스코핑된 리셋만 |
| 폰트가 serif로 바뀜 | `<link>` 폰트 제거됨 | `@import`를 `<style>` 안에 |
| 버튼이 다른 요소 조작 | JS가 전역 ID 쿼리 | `closest('.mywidget')`로 스코핑 |
| 스크롤 시 겹침 | sticky/fixed 충돌 | static/relative, JS scrollIntoView |

## 관련

- [[llm/프롬프트-패턴|프롬프트 패턴]] — 위젯 생성 시 유용한 프롬프트
- [[링스택-게임|링 스택 게임]] — 인터랙티브 카드 예시 (하스스톤풍)
