# 🧠 LLM Wiki

> 개인 지식 베이스. 손에 쥔 카드처럼 펼쳐진 카드를 탐색해보세요.
> **호버** = 살짝 올라옴 · **클릭 1번** = 확대 + 마우스 따라 기울임 · **클릭 2번** = 페이지 이동

<div class="deck">

<div class="card" data-href="projects/" data-img="assets/cards/all-projects.svg" data-icon="📁" data-title="모든 프로젝트" data-sub="All Projects" data-badge="전체 보기" data-desc="프로젝트 도메인 전체 목록과 하위 구조 탐색."></div>

<div class="card" data-href="projects/unity/링스택/" data-img="assets/cards/ring-stack.svg" data-icon="⚙️" data-title="링 스택" data-sub="Ring Stack" data-badge="Unity · 게임" data-desc="스택 장르의 타이밍 탭 + 정렬 판정을 회전으로 재구성한 Unity 게임. 720슬롯 AND 판정, 절차적 메시, NPR 셰이더."></div>

<div class="card" data-href="llm/사용로그" data-img="assets/cards/llm-usage.svg" data-icon="📝" data-title="LLM 사용로그" data-sub="Usage Log" data-badge="사용 기록" data-desc="날짜별 LLM 사용 기록. 무엇을 했고 뭘 배웠는지 append-only로 쌓음."></div>

<div class="card" data-href="llm/프롬프트-패턴" data-img="assets/cards/prompt-patterns.svg" data-icon="💡" data-title="프롬프트 패턴" data-sub="Prompt Patterns" data-badge="기법" data-desc="LLM 사용 중 발견한 유용한 프롬프트/기법 모음."></div>

</div>

<style>

.deck {
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 420px;
  margin: 2rem 0 3rem;
  perspective: 1600px;
  padding: 2rem 0;
}
.card {
  --fan: 0deg;
  position: relative;
  width: 170px;
  aspect-ratio: 5 / 7;
  cursor: pointer;
  transform-origin: 50% 100%;
  transform: rotateY(var(--fan));
  transition: transform 0.4s cubic-bezier(0.25, 1, 0.5, 1), box-shadow 0.3s, filter 0.3s;
  border-radius: 16px;
  z-index: 1;
  margin: 0 -14px;
  box-shadow: 0 8px 20px rgba(0,0,0,0.45);
  background: #14141c;
  border: 1px solid rgba(255,255,255,0.18);
}
.card:nth-child(1) { --fan: 32deg; }
.card:nth-child(2) { --fan: 11deg; }
.card:nth-child(3) { --fan: -11deg; }
.card:nth-child(4) { --fan: -32deg; }
.card:nth-child(5) { --fan: 45deg; }
.card:nth-child(6) { --fan: 26deg; }
.card:nth-child(7) { --fan: 8deg; }
.card:nth-child(8) { --fan: -8deg; }
.card:nth-child(9) { --fan: -26deg; }
.card:nth-child(10) { --fan: -45deg; }
.card:hover {
  transform: rotateY(var(--fan)) translateZ(50px) translateY(-10px) scale(1.05);
  box-shadow: 0 20px 40px rgba(0,0,0,0.6);
  z-index: 60;
}
.card.selected {
  transform: rotateY(0deg) translateZ(90px) scale(1.4);
  z-index: 100;
  transition: transform 0.45s cubic-bezier(0.2, 1.2, 0.3, 1);
}
.card.selected:hover {
  transform: rotateY(0deg) translateZ(90px) scale(1.4);
}
.deck:has(.card.selected) .card:not(.selected) {
  opacity: 0.4;
  filter: grayscale(0.4) brightness(0.6);
}
.card-bg {
  position: absolute;
  inset: 0;
  border-radius: 16px;
  overflow: hidden;
  background-size: cover;
  background-position: center;
  filter: blur(6px) brightness(0.5);
}
.card-overlay {
  position: absolute;
  inset: 0;
  border-radius: 16px;
  background: linear-gradient(180deg, rgba(0,0,0,0.15) 0%, rgba(0,0,0,0.55) 100%);
}
.card-content {
  position: absolute;
  inset: 0;
  border-radius: 16px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 14px;
  text-align: center;
  gap: 6px;
}
.card-icon { font-size: 2.2rem; line-height: 1; filter: drop-shadow(0 2px 6px rgba(0,0,0,0.5)); }
.card-title { font-size: 1.05rem; font-weight: 700; color: #fff; text-shadow: 0 1px 4px rgba(0,0,0,0.7); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 100%; }
.card-sub { font-size: 0.68rem; opacity: 0.75; color: #ddd; text-transform: uppercase; letter-spacing: 0.08em; }
.card-badge {
  display: inline-block;
  font-size: 0.68rem;
  padding: 3px 12px;
  margin-top: 4px;
  border-radius: 999px;
  background: rgba(0,0,0,0.5);
  color: #fff;
  border: 1px solid rgba(255,255,255,0.25);
  white-space: nowrap;
  backdrop-filter: blur(4px);
}
.card-tooltip {
  position: absolute;
  left: 50%;
  bottom: -40px;
  transform: translateX(-50%);
  background: rgba(0,0,0,0.92);
  color: #eee;
  font-size: 0.7rem;
  padding: 6px 12px;
  border-radius: 8px;
  width: max-content;
  max-width: 240px;
  text-align: center;
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.25s;
  z-index: 500;
  border: 1px solid rgba(255,255,255,0.2);
  box-shadow: 0 4px 12px rgba(0,0,0,0.5);
}
.card:hover .card-tooltip,
.card.selected .card-tooltip {
  opacity: 1;
}

</style>

<script>

(function () {
  var selected = null;
  var maxTilt = 16;

  function buildCard(card) {
    var icon = card.getAttribute('data-icon');
    var title = card.getAttribute('data-title');
    var sub = card.getAttribute('data-sub');
    var badge = card.getAttribute('data-badge');
    var desc = card.getAttribute('data-desc');
    var img = card.getAttribute('data-img');

    var bg = img ? '<div class="card-bg" style="background-image:url(' + img + ')"></div>' : '';
    card.innerHTML =
      bg +
      '<div class="card-overlay"></div>' +
      '<div class="card-content">' +
        (icon ? '<div class="card-icon">' + icon + '</div>' : '') +
        '<div class="card-title">' + title + '</div>' +
        (sub ? '<div class="card-sub">' + sub + '</div>' : '') +
        (badge ? '<div class="card-badge">' + badge + '</div>' : '') +
      '</div>' +
      '<div class="card-tooltip">' + desc + '</div>';
  }

  function initCards() {
    var cards = document.querySelectorAll('.card');
    cards.forEach(function (card) {
      if (card.dataset.built) return;
      card.dataset.built = '1';
      buildCard(card);
      var href = card.getAttribute('data-href');

      card.addEventListener('mousemove', function (e) {
        var rect = card.getBoundingClientRect();
        var px = (e.clientX - rect.left) / rect.width;
        var py = (e.clientY - rect.top) / rect.height;
        var rotY = (px - 0.5) * 2 * maxTilt;
        var rotX = (0.5 - py) * 2 * maxTilt;
        if (card.classList.contains('selected')) {
          card.style.transform = 'rotateY(0deg) translateZ(90px) scale(1.4) rotateX(' + rotX.toFixed(1) + 'deg) rotateY(' + rotY.toFixed(1) + 'deg)';
        } else {
          card.style.transform = 'rotateY(var(--fan)) translateZ(50px) translateY(-10px) scale(1.05) rotateX(' + (rotX*0.5).toFixed(1) + 'deg) rotateY(' + (rotY*0.5).toFixed(1) + 'deg)';
        }
      });
      card.addEventListener('mouseleave', function () {
        if (card.classList.contains('selected')) {
          card.style.transform = 'rotateY(0deg) translateZ(90px) scale(1.4)';
        } else {
          card.style.transform = '';
        }
      });

      var lastSelectTime = 0;   // 확대된 시각 (더블클릭/연타 방지용 쿨다운)
      card.addEventListener('click', function (e) {
        e.stopPropagation();
        var now = Date.now();

        // 이미 선택(확대)된 상태
        if (card.classList.contains('selected')) {
          // 확대된 직후(쿨다운 600ms 이내) 클릭은 무시 — 확대 화면을 볼 시간 확보
          if (now - lastSelectTime < 600) return;
          window.location.href = href;
          return;
        }

        // 모든 카드 선택 해제 후, 이 카드만 활성화
        var allCards = document.querySelectorAll('.card');
        allCards.forEach(function (c) {
          c.classList.remove('selected');
          c.style.transform = '';
        });
        card.classList.add('selected');
        selected = card;
        lastSelectTime = Date.now();
      });
    });

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
  document.addEventListener('nav', function () {
    if (document.querySelector('.card')) {
      document.querySelectorAll('.card').forEach(function (c) { delete c.dataset.built; });
      initCards();
      var sel = document.querySelector('.card.selected');
      if (sel) sel.classList.remove('selected');
    }
  });
})();

</script>
