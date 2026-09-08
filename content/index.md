# 🧠 LLM Wiki

> 개인 지식 베이스. 손에 쥔 카드처럼 펼쳐진 카드를 탐색해보세요.
> **호버** = 살짝 올라옴 · **클릭 1번** = 확대 + 마우스 따라 기울임 · **클릭 2번** = 페이지 이동

<div class="deck-wrap">
<div class="deck">

<div class="card" data-href="projects/" data-type="all" data-title="모든 프로젝트" data-sub="ALL PROJECTS" data-badge="도메인 허브" data-label="문서 수" data-value="220+ 페이지" data-accent="#E8C96D"></div>

<div class="card" data-href="projects/gamedev/pixel-sprite-workflow/" data-type="pixel" data-title="도트 스프라이트" data-sub="PIXEL PIPELINE" data-badge="AI · 파이프라인" data-label="워크플로우" data-value="5단계 변환" data-accent="#299E4C"></div>

<div class="card" data-href="projects/gamedev/링스택/" data-type="unity" data-title="링 스택" data-sub="RING STACK 3D" data-badge="Unity · 3D" data-label="판정 시스템" data-value="720 슬롯 AND" data-accent="#297BD4"></div>

<div class="card" data-href="llm/사용로그" data-type="log" data-title="LLM 사용로그" data-sub="USAGE LOG" data-badge="기록 · 회고" data-label="누적 방식" data-value="Append Only" data-accent="#9254E5"></div>

<div class="card" data-href="llm/프롬프트-패턴" data-type="prompt" data-title="프롬프트 패턴" data-sub="PROMPT PATTERNS" data-badge="실전 기법" data-label="설계 규격" data-value="검증된 템플릿" data-accent="#EF681B"></div>

</div>
</div>

<style>

/* treeclick UI 레이아웃 토큰 정의 (Tokens.dc.html 규격) */
:root {
  --tc-surface-detail: #161616;
  --tc-surface-panel: #161D21;
  --tc-text-primary: #F2F4F4;
  --tc-text-secondary: #899094;
  --tc-text-tertiary: #6E767B;
  --tc-action-btn: #1A6046;
  --tc-action-btn-hover: #08B67C;
  --tc-badge-bg: #23282C;
  --tc-badge-text: #A8AFB3;
  --tc-divider: #262B2F;
}

.deck-wrap {
  position: relative;
  width: 100%;
  padding: 2.5rem 0 3.5rem;
  perspective: 1800px;
  perspective-origin: 50% 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: visible;
}

.deck {
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 440px;
  width: 100%;
  max-width: 1100px;
  margin: 0 auto;
}

.card {
  --accent: #E8C96D;
  --rot-z: 0deg;
  --rot-y: 0deg;
  --trans-y: 0px;
  --trans-x: 0px;
  position: relative;
  width: 192px;
  height: 326px;
  cursor: pointer;
  border-radius: 22px;
  background: radial-gradient(120% 80% at 50% 20%, #1D293D 0%, #161D21 60%, var(--tc-surface-detail) 100%);
  border: 1.5px solid var(--accent);
  box-shadow: 0 0 8px color-mix(in srgb, var(--accent) 55%, transparent),
              0 0 26px color-mix(in srgb, var(--accent) 25%, transparent),
              0 14px 34px rgba(0,0,0,0.85);
  transform-origin: 50% 125%;
  transform: translateX(var(--trans-x)) translateY(var(--trans-y)) rotateZ(var(--rot-z)) rotateY(var(--rot-y));
  transition: transform 0.4s cubic-bezier(0.2, 0.9, 0.3, 1),
              box-shadow 0.35s ease,
              opacity 0.35s ease,
              filter 0.35s ease;
  margin: 0 -14px;
  user-select: none;
  isolation: isolate;
  flex-shrink: 0;
  box-sizing: border-box;
}

/* 1px 인셋 보조 테두리선 (상세창 집중 프레임) */
.card::before {
  content: '';
  position: absolute;
  inset: 6px;
  border: 1px solid color-mix(in srgb, var(--accent) 32%, transparent);
  border-radius: 16px;
  pointer-events: none;
  z-index: 1;
}

/* 카드 내부 컨텐츠 */
.card-inner {
  position: relative;
  z-index: 2;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-between;
  padding: 16px 12px 14px;
  text-align: center;
  box-sizing: border-box;
}

/* 상단 알약형 칩 배지 (Tokens.dc.html 규격) */
.card-chip {
  display: inline-block;
  font-size: 11px;
  font-weight: 700;
  padding: 3px 10px;
  border-radius: 999px;
  background: var(--tc-badge-bg);
  color: var(--tc-badge-text);
  letter-spacing: 0.02em;
}

/* 중앙 아이콘 프레임 (DexDetail.dc.html 규격: #0D0D0D 바탕 + 1.5px 테두리) */
.card-icon-frame {
  width: 68px;
  height: 68px;
  border-radius: 18px;
  background: #0D0D0D;
  border: 1.5px solid var(--accent);
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 2px 0;
  box-shadow: inset 0 0 12px rgba(0,0,0,0.8);
}
.card-icon-frame svg {
  width: 34px;
  height: 34px;
  stroke: var(--accent);
}

/* 제목 영역 (Tokens.dc.html 타이포 규격: 굵기 700 + 고유 액센트 색상) */
.card-title-wrap {
  width: 100%;
  margin: 2px 0;
}
.card-title {
  font-size: 16px;
  font-weight: 700;
  color: var(--accent);
  line-height: 1.25;
  letter-spacing: -0.01em;
  word-break: keep-all;
  white-space: normal;
}
.card-sub {
  font-size: 10px;
  color: var(--tc-text-secondary);
  letter-spacing: 0.06em;
  text-transform: uppercase;
  margin-top: 3px;
}

/* 1px 수평 분할선 (Tokens.dc.html 규격) */
.card-divider {
  width: 88%;
  height: 1px;
  background: var(--tc-divider);
  margin: 2px 0;
}

/* 스펙 행 (DexDetail.dc.html 규격: 라벨과 고정폭 수치 분할) */
.card-spec-row {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  width: 88%;
  font-size: 11px;
  margin: 1px 0;
}
.card-spec-label {
  color: var(--tc-text-secondary);
}
.card-spec-value {
  color: var(--tc-text-primary);
  font-weight: 700;
  font-variant-numeric: tabular-nums;
}

/* 하단 주 행동 버튼 (Tokens.dc.html action.primary-onSurface 규격: #1A6046) */
.card-action-btn {
  width: 88%;
  padding: 7px 0;
  border: 0;
  border-radius: 999px;
  background: var(--tc-action-btn);
  color: #EAF7F1;
  font-family: inherit;
  font-size: 11px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  transition: background 0.2s ease;
}
.card:hover .card-action-btn {
  background: var(--tc-action-btn-hover);
}

/* 호버 상태 */
.card:hover {
  transform: translateX(var(--trans-x)) translateY(calc(var(--trans-y) - 24px)) translateZ(70px) rotateZ(var(--rot-z)) rotateY(var(--rot-y)) scale(1.08);
  box-shadow: 0 0 14px var(--accent),
              0 0 38px color-mix(in srgb, var(--accent) 45%, transparent),
              0 22px 48px rgba(0,0,0,0.9);
  z-index: 80 !important;
}

/* 클릭 선택 상태 */
.card.selected {
  transform: translateX(0) translateY(-14px) translateZ(140px) rotateZ(0deg) rotateY(0deg) scale(1.36) !important;
  box-shadow: 0 0 20px var(--accent),
              0 0 50px color-mix(in srgb, var(--accent) 55%, transparent),
              0 30px 60px rgba(0,0,0,0.95) !important;
  z-index: 120 !important;
  transition: transform 0.45s cubic-bezier(0.18, 1.2, 0.28, 1), box-shadow 0.45s ease;
}

/* 선택 시 배경 디밍 */
.deck:has(.card.selected) .card:not(.selected) {
  opacity: 0.3;
  filter: grayscale(0.5) brightness(0.5);
  pointer-events: auto;
}

</style>

<script>

(function () {
  var maxTilt = 18;
  var selectedCard = null;
  var lastSelectTime = 0;

  // 스트로크 기반 인라인 SVG 아이콘 맵 (이모지 배제 규칙 준수)
  var iconSvgMap = {
    all: '<svg viewBox="0 0 24 24" fill="none" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/></svg>',
    pixel: '<svg viewBox="0 0 24 24" fill="none" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="13.5" cy="6.5" r=".6" fill="currentColor"/><circle cx="17.5" cy="10.5" r=".6" fill="currentColor"/><circle cx="8.5" cy="7.5" r=".6" fill="currentColor"/><circle cx="6.5" cy="12.5" r=".6" fill="currentColor"/><path d="M12 2C6.5 2 2 6.5 2 12s4.5 10 10 10c.926 0 1.648-.746 1.648-1.688 0-.437-.18-.835-.437-1.125-.29-.289-.438-.652-.438-1.125a1.64 1.64 0 0 1 1.668-1.668h1.996c3.051 0 5.555-2.503 5.555-5.554C21.965 6.012 17.461 2 12 2z"/></svg>',
    unity: '<svg viewBox="0 0 24 24" fill="none" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83"/><circle cx="12" cy="12" r="4"/></svg>',
    log: '<svg viewBox="0 0 24 24" fill="none" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>',
    prompt: '<svg viewBox="0 0 24 24" fill="none" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M9 18h6M10 22h4M15.09 14c.18-.98.65-1.74 1.41-2.5A4.65 4.65 0 0 0 18 8 6 6 0 0 0 6 8c0 1 .23 2.23 1.5 3.5.76.76 1.23 1.52 1.41 2.5z"/></svg>'
  };

  // 수학적 대칭 각도 및 Y축 곡률 계산
  function updateCardFan() {
    var cards = Array.from(document.querySelectorAll('.deck .card'));
    var count = cards.length;
    if (count === 0) return;

    var mid = (count - 1) / 2;
    var stepAngle = count > 6 ? 4.6 : 6.0;

    cards.forEach(function (card, i) {
      var diff = i - mid;
      var rotZ = diff * stepAngle;
      var rotY = diff * -2.4;
      var transY = Math.pow(Math.abs(diff), 1.75) * 4.4;
      var transX = diff * 2.5;

      card.style.setProperty('--rot-z', rotZ.toFixed(2) + 'deg');
      card.style.setProperty('--rot-y', rotY.toFixed(2) + 'deg');
      card.style.setProperty('--trans-y', transY.toFixed(1) + 'px');
      card.style.setProperty('--trans-x', transX.toFixed(1) + 'px');
      card.style.zIndex = (10 + Math.round(10 - Math.abs(diff))).toString();
    });
  }

  // 카드 돔 빌드 (treeclick UI 시스템 적용)
  function buildCard(card) {
    var type = card.getAttribute('data-type') || 'all';
    var title = card.getAttribute('data-title') || '';
    var sub = card.getAttribute('data-sub') || '';
    var badge = card.getAttribute('data-badge') || '';
    var label = card.getAttribute('data-label') || '';
    var value = card.getAttribute('data-value') || '';
    var accent = card.getAttribute('data-accent') || '#E8C96D';

    card.style.setProperty('--accent', accent);

    var iconSvg = iconSvgMap[type] || iconSvgMap['all'];

    card.innerHTML =
      '<div class="card-inner">' +
        '<div style="width: 100%; display: flex; justify-content: center; min-height: 22px;">' +
          (badge ? '<span class="card-chip">' + badge + '</span>' : '') +
        '</div>' +
        '<div class="card-icon-frame">' + iconSvg + '</div>' +
        '<div class="card-title-wrap">' +
          '<div class="card-title">' + title + '</div>' +
          (sub ? '<div class="card-sub">' + sub + '</div>' : '') +
        '</div>' +
        '<div class="card-divider"></div>' +
        (label ? '<div class="card-spec-row"><span class="card-spec-label">' + label + '</span><span class="card-spec-value">' + value + '</span></div>' : '') +
        '<div class="card-action-btn">' +
          '<span>열기</span>' +
          '<svg viewBox="0 0 24 24" style="width:13px; height:13px;" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M7 17l9.2-9.2M17 17V8H8"/></svg>' +
        '</div>' +
      '</div>';

    card.dataset.built = '1';
  }

  function ensureCardsBuilt() {
    document.querySelectorAll('.deck .card:not([data-built])').forEach(function (card) {
      buildCard(card);
    });
    updateCardFan();
  }

  // 클릭 이벤트 (선택 및 페이지 이동)
  document.addEventListener('click', function (e) {
    var card = e.target.closest('.card');
    var now = Date.now();

    if (!card) {
      if (selectedCard) {
        selectedCard.classList.remove('selected');
        selectedCard.style.transform = '';
        selectedCard = null;
      }
      return;
    }

    var href = card.getAttribute('data-href');

    if (card.classList.contains('selected')) {
      if (now - lastSelectTime < 500) return;
      if (href) {
        window.location.href = href;
      }
      return;
    }

    document.querySelectorAll('.deck .card').forEach(function (c) {
      c.classList.remove('selected');
      c.style.transform = '';
    });
    card.classList.add('selected');
    selectedCard = card;
    lastSelectTime = now;
  });

  // 3D 마우스 틸트 인터랙션
  document.addEventListener('mouseover', function (e) {
    var card = e.target.closest('.card');
    if (!card || card.dataset.tiltInit) return;
    card.dataset.tiltInit = '1';

    card.addEventListener('mousemove', function (ev) {
      var rect = card.getBoundingClientRect();
      var px = (ev.clientX - rect.left) / rect.width;
      var py = (ev.clientY - rect.top) / rect.height;
      var rotY = (px - 0.5) * 2 * maxTilt;
      var rotX = (0.5 - py) * 2 * maxTilt;

      if (card.classList.contains('selected')) {
        card.style.transform = 'translateX(0) translateY(-14px) translateZ(140px) rotateZ(0deg) scale(1.36) rotateX(' + rotX.toFixed(1) + 'deg) rotateY(' + rotY.toFixed(1) + 'deg)';
      }
    });

    card.addEventListener('mouseleave', function () {
      if (card.classList.contains('selected')) {
        card.style.transform = '';
      }
    });
  });

  function init() {
    ensureCardsBuilt();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  document.addEventListener('nav', function () {
    if (document.querySelector('.deck .card')) {
      document.querySelectorAll('.deck .card').forEach(function (c) {
        delete c.dataset.built;
        delete c.dataset.tiltInit;
      });
      ensureCardsBuilt();
      if (selectedCard) {
        selectedCard.classList.remove('selected');
        selectedCard = null;
      }
      lastSelectTime = 0;
    }
  });

  window.addEventListener('resize', updateCardFan);
})();

</script>
