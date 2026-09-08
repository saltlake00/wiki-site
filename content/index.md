# 🧠 LLM Wiki

> 개인 지식 베이스. 손에 쥔 카드처럼 펼쳐진 카드를 탐색해보세요.
> **호버** = 살짝 올라옴 · **클릭 1번** = 확대 + 마우스 따라 기울임 · **클릭 2번** = 페이지 이동

<svg width="0" height="0" style="position:absolute; display:none;" aria-hidden="true">
  <defs>
    <g id="corner-knot" fill="none" stroke="currentColor" stroke-width="1.6">
      <rect x="10" y="1" width="10" height="28" rx="5"/>
      <rect x="1" y="10" width="28" height="10" rx="5"/>
      <path d="M7 15h16M15 7v16"/>
    </g>
  </defs>
</svg>

<div class="deck-wrap">
<div class="deck">

<div class="card" data-href="projects/" data-icon="📁" data-title="모든 프로젝트" data-sub="ALL PROJECTS" data-badge="도메인 허브" data-desc="전체 위키 도메인 및 지식 구조 한눈에 탐색" data-accent="#e8c96d"></div>

<div class="card" data-href="projects/gamedev/pixel-sprite-workflow/" data-icon="🎨" data-title="도트 스프라이트" data-sub="PIXEL WORKFLOW" data-badge="AI · 파이프라인" data-desc="AI 이미지 생성부터 Unity 애니메이션 시트까지" data-accent="#08b67c"></div>

<div class="card" data-href="projects/gamedev/링스택/" data-icon="⚙️" data-title="링 스택" data-sub="RING STACK" data-badge="Unity · 3D 게임" data-desc="타이밍 회전 판정과 절차적 메시의 3D 스택 게임" data-accent="#399ce6"></div>

<div class="card" data-href="llm/사용로그" data-icon="📝" data-title="LLM 사용로그" data-sub="USAGE LOG" data-badge="기록 · 회고" data-desc="날짜별 AI 협업 기록과 통찰 누적 일지" data-accent="#9254e5"></div>

<div class="card" data-href="llm/프롬프트-패턴" data-icon="💡" data-title="프롬프트 패턴" data-sub="PROMPT PATTERNS" data-badge="기법 · 라이브러리" data-desc="실전 검증된 고품질 AI 프롬프트 설계 모음" data-accent="#ef681b"></div>

</div>
</div>

<style>

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
  max-width: 1080px;
  margin: 0 auto;
}

.card {
  --accent: #e8c96d;
  --rot-z: 0deg;
  --rot-y: 0deg;
  --trans-y: 0px;
  --trans-x: 0px;
  position: relative;
  width: 184px;
  height: 316px;
  cursor: pointer;
  border-radius: 22px;
  background: radial-gradient(circle at 50% 18%, #1c2127 0%, #13171a 65%, #0b0d0f 100%);
  border: 1px solid var(--accent);
  box-shadow: 0 10px 30px rgba(0,0,0,0.8),
              0 0 14px color-mix(in srgb, var(--accent) 45%, transparent),
              0 0 35px color-mix(in srgb, var(--accent) 15%, transparent);
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

/* 1px 마비노기 이중 프레임 */
.card::before {
  content: '';
  position: absolute;
  inset: 6px;
  border: 1px solid color-mix(in srgb, var(--accent) 45%, transparent);
  border-radius: 16px;
  pointer-events: none;
  z-index: 1;
}

/* 네 모서리 룬 매듭 오너먼트 */
.card-knot {
  position: absolute;
  width: 22px;
  height: 22px;
  color: var(--accent);
  pointer-events: none;
  z-index: 2;
  opacity: 0.85;
}
.card-knot.tl { top: 6px; left: 6px; }
.card-knot.tr { top: 6px; right: 6px; }
.card-knot.bl { bottom: 6px; left: 6px; }
.card-knot.br { bottom: 6px; right: 6px; }

/* 카드 내부 컨텐츠 */
.card-inner {
  position: relative;
  z-index: 3;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-between;
  padding: 16px 12px 16px;
  text-align: center;
  box-sizing: border-box;
}

/* 상단 칩 배지 */
.card-chip-wrap {
  width: 100%;
  display: flex;
  justify-content: center;
  min-height: 24px;
}
.card-chip {
  display: inline-block;
  font-size: 0.68rem;
  font-weight: 600;
  letter-spacing: 0.04em;
  padding: 2px 10px;
  border-radius: 999px;
  background: rgba(11, 15, 18, 0.8);
  color: var(--accent);
  border: 1px solid color-mix(in srgb, var(--accent) 55%, transparent);
  box-shadow: 0 0 8px color-mix(in srgb, var(--accent) 25%, transparent);
}

/* 중앙 아이콘 및 발광 */
.card-icon-frame {
  position: relative;
  width: 68px;
  height: 68px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 2px 0;
}
.card-icon-glow {
  position: absolute;
  inset: -12px;
  border-radius: 50%;
  background: radial-gradient(circle, color-mix(in srgb, var(--accent) 35%, transparent) 0%, transparent 70%);
  pointer-events: none;
}
.card-icon {
  font-size: 2.3rem;
  line-height: 1;
  filter: drop-shadow(0 4px 10px rgba(0,0,0,0.8));
  position: relative;
  z-index: 1;
}

/* 제목 영역 (말줄임 없이 자연스러운 표시) */
.card-title-wrap {
  margin: 2px 0;
  width: 100%;
}
.card-title {
  font-size: 1.02rem;
  font-weight: 700;
  color: #f4f6f8;
  line-height: 1.35;
  margin-bottom: 3px;
  word-break: keep-all;
  white-space: normal;
  text-shadow: 0 2px 5px rgba(0,0,0,0.9);
}
.card-sub {
  font-size: 0.64rem;
  letter-spacing: 0.08em;
  color: #899094;
  text-transform: uppercase;
}

/* 1px 수평 분할선 */
.card-divider {
  width: 78%;
  height: 1px;
  background: linear-gradient(90deg, transparent, color-mix(in srgb, var(--accent) 45%, transparent), transparent);
  margin: 4px 0;
}

/* 설명문 */
.card-desc {
  font-size: 0.69rem;
  line-height: 1.45;
  color: #a0acae;
  padding: 0 4px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  word-break: keep-all;
}

/* 하단 액션 힌트 */
.card-action-hint {
  font-size: 0.66rem;
  color: var(--accent);
  font-weight: 600;
  opacity: 0.8;
  margin-top: 2px;
}

/* 호버 상태 (살짝 부유 + 네온 발광 증폭) */
.card:hover {
  transform: translateX(var(--trans-x)) translateY(calc(var(--trans-y) - 26px)) translateZ(70px) rotateZ(var(--rot-z)) rotateY(var(--rot-y)) scale(1.08);
  box-shadow: 0 20px 45px rgba(0,0,0,0.85),
              0 0 20px var(--accent),
              0 0 50px color-mix(in srgb, var(--accent) 35%, transparent);
  z-index: 80 !important;
}

/* 클릭 선택 상태 (중앙 확대 + 정면 정렬) */
.card.selected {
  transform: translateX(0) translateY(-14px) translateZ(140px) rotateZ(0deg) rotateY(0deg) scale(1.36) !important;
  box-shadow: 0 30px 60px rgba(0,0,0,0.95),
              0 0 30px var(--accent),
              0 0 70px color-mix(in srgb, var(--accent) 50%, transparent) !important;
  z-index: 120 !important;
  transition: transform 0.45s cubic-bezier(0.18, 1.2, 0.28, 1), box-shadow 0.45s ease;
}

/* 선택 시 배경 카드 부드러운 디밍 */
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

  // 완벽한 대칭 각도 및 곡률 수식 계산
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

  // 카드 돔 빌드 (마비노기 모바일 UI 구조 생성)
  function buildCard(card) {
    var icon = card.getAttribute('data-icon') || '📁';
    var title = card.getAttribute('data-title') || '';
    var sub = card.getAttribute('data-sub') || '';
    var badge = card.getAttribute('data-badge') || '';
    var desc = card.getAttribute('data-desc') || '';
    var accent = card.getAttribute('data-accent') || '#e8c96d';

    card.style.setProperty('--accent', accent);

    card.innerHTML =
      '<svg class="card-knot tl" viewBox="0 0 30 30" aria-hidden="true"><use href="#corner-knot"/></svg>' +
      '<svg class="card-knot tr" viewBox="0 0 30 30" aria-hidden="true"><use href="#corner-knot"/></svg>' +
      '<svg class="card-knot bl" viewBox="0 0 30 30" aria-hidden="true"><use href="#corner-knot"/></svg>' +
      '<svg class="card-knot br" viewBox="0 0 30 30" aria-hidden="true"><use href="#corner-knot"/></svg>' +
      '<div class="card-inner">' +
        (badge ? '<div class="card-chip-wrap"><span class="card-chip">' + badge + '</span></div>' : '<div style="height:24px;"></div>') +
        '<div class="card-icon-frame">' +
          '<div class="card-icon-glow"></div>' +
          '<div class="card-icon">' + icon + '</div>' +
        '</div>' +
        '<div class="card-title-wrap">' +
          '<div class="card-title">' + title + '</div>' +
          (sub ? '<div class="card-sub">' + sub + '</div>' : '') +
        '</div>' +
        '<div class="card-divider"></div>' +
        (desc ? '<div class="card-desc">' + desc + '</div>' : '') +
        '<div class="card-action-hint">열기 ↗</div>' +
      '</div>';

    card.dataset.built = '1';
  }

  function ensureCardsBuilt() {
    document.querySelectorAll('.deck .card:not([data-built])').forEach(function (card) {
      buildCard(card);
    });
    updateCardFan();
  }

  // 클릭 이벤트 처리 (선택 및 페이지 이동)
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

  // 마우스 이동 시 3D 원근 틸트 인터랙션
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

  // Quartz SPA 페이지 전환 복원
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
