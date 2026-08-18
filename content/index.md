# 🧠 LLM Wiki

> 개인 지식 베이스. 손에 쥔 카드처럼 펼쳐진 카드를 탐색해보세요.
> **호버** = 살짝 올라옴 · **클릭 1번** = 확대+마우스 따라 기울임 · **클릭 2번** = 페이지 이동

<div class="hearth-deck">

<div class="hearth-card" data-href="projects/unity/링스택/" data-title="링 스택">
  <div class="hc-inner">
    <div class="hc-frame">
      <div class="hc-art">
        <img src="assets/cards/ring-stack.svg" alt="링 스택" />
        <div class="hc-art-overlay"></div>
      </div>
      <div class="hc-name">⚙️ 링 스택</div>
      <div class="hc-stats">
        <span class="hc-stat">Unity</span>
        <span class="hc-stat gem">게임</span>
      </div>
    </div>
    <div class="hc-tooltip">720슬롯 AND 판정 · 절차적 메시 · NPR 셰이더</div>
  </div>
</div>

<div class="hearth-card" data-href="projects/" data-title="모든 프로젝트">
  <div class="hc-inner">
    <div class="hc-frame">
      <div class="hc-art">
        <img src="assets/cards/all-projects.svg" alt="모든 프로젝트" />
        <div class="hc-art-overlay"></div>
      </div>
      <div class="hc-name">📁 모든 프로젝트</div>
      <div class="hc-stats">
        <span class="hc-stat">전체</span>
        <span class="hc-stat gem">보기</span>
      </div>
    </div>
    <div class="hc-tooltip">프로젝트 도메인 전체 목록과 하위 구조 탐색</div>
  </div>
</div>

<div class="hearth-card" data-href="llm/사용로그" data-title="LLM 사용로그">
  <div class="hc-inner">
    <div class="hc-frame">
      <div class="hc-art">
        <img src="assets/cards/llm-usage.svg" alt="LLM 사용로그" />
        <div class="hc-art-overlay"></div>
      </div>
      <div class="hc-name">🤖 LLM 사용로그</div>
      <div class="hc-stats">
        <span class="hc-stat">기록</span>
        <span class="hc-stat gem">Log</span>
      </div>
    </div>
    <div class="hc-tooltip">날짜별 LLM 사용 기록 · append-only</div>
  </div>
</div>

<div class="hearth-card" data-href="llm/프롬프트-패턴" data-title="프롬프트 패턴">
  <div class="hc-inner">
    <div class="hc-frame">
      <div class="hc-art">
        <img src="assets/cards/prompt-patterns.svg" alt="프롬프트 패턴" />
        <div class="hc-art-overlay"></div>
      </div>
      <div class="hc-name">💡 프롬프트 패턴</div>
      <div class="hc-stats">
        <span class="hc-stat">기법</span>
        <span class="hc-stat gem">Prompt</span>
      </div>
    </div>
    <div class="hc-tooltip">유용한 프롬프트/기법 모음</div>
  </div>
</div>

</div>

<style>
/* 하스스톤 카드 손패 부채꼴 */
.hearth-deck {
  position: relative;
  display: flex;
  justify-content: center;
  align-items: flex-end;
  gap: -0.5rem;
  min-height: 380px;
  margin: 2rem 0 3rem;
  perspective: 1600px;
  padding-top: 2rem;
}
.hearth-card {
  --base-angle: 0deg;
  position: relative;
  width: 150px;
  aspect-ratio: 5 / 7;
  cursor: pointer;
  transform-origin: 50% 100%;
  transform: rotate(var(--base-angle));
  transition: transform 0.35s cubic-bezier(0.25, 1, 0.5, 1), z-index 0s, filter 0.3s;
  filter: drop-shadow(0 6px 16px rgba(0,0,0,0.45));
  z-index: 1;
}
/* 각 카드의 부채꼴 각도 (n=4: -13.5, -4.5, 4.5, 13.5) */
.hearth-card:nth-child(1) { --base-angle: -14deg; margin-right: -18px; }
.hearth-card:nth-child(2) { --base-angle: -4.5deg; margin-right: -18px; }
.hearth-card:nth-child(3) { --base-angle: 4.5deg; margin-right: -18px; }
.hearth-card:nth-child(4) { --base-angle: 14deg; }

.hearth-card:hover {
  transform: rotate(var(--base-angle)) translateY(-24px) scale(1.12);
  filter: drop-shadow(0 16px 28px rgba(0,0,0,0.6));
  z-index: 50;
}
/* 확대/선택 상태 */
.hearth-card.selected {
  transform: rotate(0deg) translateY(-60px) scale(1.5);
  z-index: 100;
  transition: transform 0.4s cubic-bezier(0.2, 1.2, 0.3, 1);
}
.hearth-card.selected:hover {
  transform: rotate(0deg) translateY(-60px) scale(1.5);
}

.hc-inner {
  position: absolute;
  inset: 0;
  transform-style: preserve-3d;
  will-change: transform;
}
.hc-frame {
  position: absolute;
  inset: 0;
  border-radius: 14px;
  padding: 10px;
  background: linear-gradient(160deg, #7f1d1d 0%, #450a0a 40%, #1a0b2e 100%);
  border: 2px solid #f59e0b;
  box-shadow: inset 0 0 0 2px rgba(245,158,11,0.35), inset 0 0 30px rgba(0,0,0,0.6);
  display: flex;
  flex-direction: column;
}
.hc-art {
  flex: 1;
  border-radius: 9px;
  overflow: hidden;
  position: relative;
  border: 2px solid #fbbf24;
}
.hc-art img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}
.hc-art-overlay {
  position: absolute;
  inset: 0;
  background: radial-gradient(circle at 50% 30%, rgba(255,215,0,0.12), transparent 60%);
  pointer-events: none;
}
.hc-name {
  margin-top: 8px;
  font-size: 0.9rem;
  font-weight: 700;
  text-align: center;
  color: #fde68a;
  text-shadow: 0 1px 2px rgba(0,0,0,0.8);
  letter-spacing: 0.02em;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.hc-stats {
  display: flex;
  justify-content: space-between;
  margin-top: 6px;
}
.hc-stat {
  font-size: 0.7rem;
  font-weight: 600;
  color: #fbbf24;
  background: rgba(0,0,0,0.4);
  padding: 2px 8px;
  border-radius: 999px;
  border: 1px solid rgba(251,191,36,0.4);
}
.hc-stat.gem {
  color: #c084fc;
  border-color: rgba(192,132,252,0.5);
  background: rgba(88,28,135,0.5);
}
.hc-tooltip {
  position: absolute;
  left: 50%;
  bottom: -32px;
  transform: translateX(-50%);
  background: rgba(0,0,0,0.85);
  color: #fde68a;
  font-size: 0.68rem;
  padding: 5px 10px;
  border-radius: 8px;
  white-space: nowrap;
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.25s;
  z-index: 200;
  border: 1px solid rgba(251,191,36,0.4);
}
.hearth-card:hover .hc-tooltip,
.hearth-card.selected .hc-tooltip {
  opacity: 1;
}

/* 확대 상태에서 카드 상세 표시 */
.hearth-card.selected .hc-detail {
  display: block;
}
</style>

<script>
(function () {
  var selected = null;
  var maxTilt = 18;

  function initCards() {
    var cards = document.querySelectorAll('.hearth-card');

    cards.forEach(function (card) {
      var inner = card.querySelector('.hc-inner');
      var href = card.getAttribute('data-href');
      var lastClick = 0;

      // 호버 시 살짝 올라옴 (CSS transition으로 처리됨)
      // 마우스 이동에 따른 3D 틸트 (선택 상태에서만)
      card.addEventListener('mousemove', function (e) {
        if (!card.classList.contains('selected')) {
          // 선택 안 된 카드도 살짝 틸트
          var rect = card.getBoundingClientRect();
          var px = (e.clientX - rect.left) / rect.width;
          var py = (e.clientY - rect.top) / rect.height;
          var rotY = (px - 0.5) * maxTilt;
          var rotX = (0.5 - py) * maxTilt * 0.7;
          inner.style.transform = 'translateZ(0px) rotateX(' + rotX.toFixed(1) + 'deg) rotateY(' + rotY.toFixed(1) + 'deg)';
        }
      });

      card.addEventListener('mouseleave', function () {
        inner.style.transform = 'translateZ(0px) rotateX(0deg) rotateY(0deg)';
      });

      // 클릭 처리: 1번째 = 확대/선택, 2번째 = 이동
      card.addEventListener('click', function (e) {
        var now = Date.now();
        if (now - lastClick < 500) {
          // 더블클릭 → 페이지 이동
          window.location.href = href;
          return;
        }
        lastClick = now;

        if (card.classList.contains('selected')) {
          // 이미 선택된 상태에서 클릭 → 페이지 이동
          window.location.href = href;
          return;
        }

        // 이전 선택 해제
        if (selected) {
          selected.classList.remove('selected');
        }
        card.classList.add('selected');
        selected = card;
      });
    });

    // 빈 곳 클릭 시 선택 해제
    document.addEventListener('click', function (e) {
      if (!e.target.closest('.hearth-card') && selected) {
        selected.classList.remove('selected');
        selected = null;
      }
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initCards);
  } else {
    initCards();
  }
})();
</script>
