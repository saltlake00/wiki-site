# 🧠 LLM Wiki

> 개인 지식 베이스. 손에 쥔 카드처럼 펼쳐진 카드를 탐색해보세요.
> **호버** = 살짝 올라옴 · **클릭 1번** = 확대 + 마우스 따라 기울임 · **클릭 2번** = 페이지 이동

<div class="deck">

<div class="card" data-href="projects/unity/링스택/" data-img="assets/cards/ring-stack.svg" data-icon="⚙️" data-title="링 스택" data-sub="Ring Stack" data-badge="Unity · 게임" data-desc="스택 장르의 타이밍 탭 + 정렬 판정을 회전으로 재구성한 Unity 게임."></div>
<div class="card" data-href="projects/" data-img="assets/cards/all-projects.svg" data-icon="📁" data-title="모든 프로젝트" data-sub="All Projects" data-badge="전체 보기" data-desc="프로젝트 도메인 전체 목록과 하위 구조 탐색."></div>
<div class="card" data-href="llm/사용로그" data-img="assets/cards/llm-usage.svg" data-icon="📝" data-title="LLM 사용로그" data-sub="Usage Log" data-badge="사용 기록" data-desc="날짜별 LLM 사용 기록. 무엇을 했고 뭘 배웠는지 append-only로 쌓음."></div>
<div class="card" data-href="llm/프롬프트-패턴" data-img="assets/cards/prompt-patterns.svg" data-icon="💡" data-title="프롬프트 패턴" data-sub="Prompt Patterns" data-badge="기법" data-desc="LLM 사용 중 발견한 유용한 프롬프트/기법 모음."></div>

</div>

<style>
.deck {
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 360px;
  margin: 2rem 0 3rem;
  perspective: 1400px;
  padding-top: 1rem;
}
/* 카드 기본: 깔끔한 디자인 + 반원(rotateY) 배치 */
.card {
  --fan: 0deg;
  position: relative;
  width: 160px;
  aspect-ratio: 5 / 7;
  cursor: pointer;
  transform-origin: 50% 100%;
  transform: rotateY(var(--fan));
  transition: transform 0.4s cubic-bezier(0.25, 1, 0.5, 1), box-shadow 0.3s, filter 0.3s;
  border-radius: 14px;
  border: 1px solid var(--border, rgba(128,128,128,0.35));
  background: var(--card, #1a1a22);
  box-shadow: 0 6px 16px rgba(0,0,0,0.4);
  overflow: hidden;
  z-index: 1;
  margin: 0 -12px;
}
/* 반원 배치: 카드들이 중심축 기준으로 휘어짐 */
.card:nth-child(1) { --fan: 32deg; }
.card:nth-child(2) { --fan: 11deg; }
.card:nth-child(3) { --fan: -11deg; }
.card:nth-child(4) { --fan: -32deg; }

.card:hover {
  transform: rotateY(var(--fan)) translateZ(40px) scale(1.06);
  box-shadow: 0 18px 36px rgba(0,0,0,0.55);
  z-index: 60;
}
/* 선택(확대) 상태: 중앙으로 모이고 정면 */
.card.selected {
  transform: rotateY(0deg) translateZ(80px) scale(1.45);
  z-index: 100;
  transition: transform 0.45s cubic-bezier(0.2, 1.2, 0.3, 1);
}
.card.selected:hover {
  transform: rotateY(0deg) translateZ(80px) scale(1.45);
}

/* 카드 내용 */
.card-inner {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  padding: 12px;
  transform-style: preserve-3d;
}
.card-art {
  flex: 1;
  border-radius: 10px;
  overflow: hidden;
  background: #0d0d14;
  position: relative;
}
.card-art img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}
.card-art-glow {
  position: absolute;
  inset: 0;
  background: radial-gradient(circle at 50% 25%, rgba(255,255,255,0.08), transparent 60%);
  pointer-events: none;
}
.card-info {
  margin-top: 10px;
  text-align: center;
}
.card-icon { font-size: 1.6rem; line-height: 1; margin-bottom: 2px; }
.card-title { font-size: 0.95rem; font-weight: 700; color: var(--foreground, #eee); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.card-sub { font-size: 0.65rem; opacity: 0.5; text-transform: uppercase; letter-spacing: 0.06em; margin-top: 1px; }
.card-badge {
  display: inline-block;
  font-size: 0.65rem;
  padding: 2px 10px;
  margin-top: 6px;
  border-radius: 999px;
  background: rgba(128,128,128,0.18);
  color: var(--gray, #aaa);
  border: 1px solid rgba(128,128,128,0.25);
  white-space: nowrap;
}

/* 툴팁 */
.card-tooltip {
  position: absolute;
  left: 50%;
  bottom: -34px;
  transform: translateX(-50%);
  background: rgba(0,0,0,0.88);
  color: #eee;
  font-size: 0.7rem;
  padding: 6px 12px;
  border-radius: 8px;
  width: max-content;
  max-width: 220px;
  text-align: center;
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.25s;
  z-index: 200;
  border: 1px solid rgba(128,128,128,0.4);
  box-shadow: 0 4px 12px rgba(0,0,0,0.4);
}
.card:hover .card-tooltip,
.card.selected .card-tooltip {
  opacity: 1;
}
</style>

<script>
(function () {
  var selected = null;
  var maxTilt = 14;

  function buildCard(card) {
    var icon = card.getAttribute('data-icon');
    var title = card.getAttribute('data-title');
    var sub = card.getAttribute('data-sub');
    var badge = card.getAttribute('data-badge');
    var desc = card.getAttribute('data-desc');
    var img = card.getAttribute('data-img');

    card.innerHTML =
      '<div class="card-inner">' +
        '<div class="card-art"><img src="' + img + '" alt="' + title + '"/><div class="card-art-glow"></div></div>' +
        '<div class="card-info">' +
          (icon ? '<div class="card-icon">' + icon + '</div>' : '') +
          '<div class="card-title">' + title + '</div>' +
          (sub ? '<div class="card-sub">' + sub + '</div>' : '') +
          (badge ? '<div class="card-badge">' + badge + '</div>' : '') +
        '</div>' +
      '</div>' +
      '<div class="card-tooltip">' + desc + '</div>';
  }

  function initCards() {
    var cards = document.querySelectorAll('.card');
    cards.forEach(function (card) {
      buildCard(card);
      var href = card.getAttribute('data-href');
      var inner = card.querySelector('.card-inner');
      var lastClick = 0;

      // 마우스 이동: 선택 상태에서 3D 틸트
      card.addEventListener('mousemove', function (e) {
        var rect = card.getBoundingClientRect();
        var px = (e.clientX - rect.left) / rect.width;   // 0~1
        var py = (e.clientY - rect.top) / rect.height;   // 0~1
        var rotY = (px - 0.5) * 2 * maxTilt;
        var rotX = (0.5 - py) * 2 * maxTilt;
        inner.style.transform = 'rotateX(' + rotX.toFixed(1) + 'deg) rotateY(' + rotY.toFixed(1) + 'deg) translateZ(0px)';
      });
      card.addEventListener('mouseleave', function () {
        inner.style.transform = '';
      });

      // 클릭: 1번 = 확대/선택, 2번 = 이동
      card.addEventListener('click', function (e) {
        e.stopPropagation();
        var now = Date.now();
        if (now - lastClick < 500) {
          window.location.href = href;
          return;
        }
        lastClick = now;

        if (card.classList.contains('selected')) {
          window.location.href = href;
          return;
        }
        if (selected) selected.classList.remove('selected');
        card.classList.add('selected');
        selected = card;
      });
    });

    // 빈 곳 클릭 시 선택 해제
    document.addEventListener('click', function (e) {
      if (!e.target.closest('.card') && selected) {
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
