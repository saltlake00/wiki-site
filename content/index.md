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
  min-height: 400px;
  margin: 2rem 0 3rem;
  perspective: 1600px;
  padding: 2rem 0;
}
/* 카드: 전체가 3D로 기울어짐 (내부가 아니라 카드 자체) */
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
  /* overflow: hidden 제거 — 툴팁이 카드 바깥에 표시되도록 */
  z-index: 1;
  margin: 0 -14px;
  box-shadow: 0 8px 20px rgba(0,0,0,0.45);
  background: #14141c;
  /* 카드 모서리 얇은 외곽선 */
  border: 1px solid rgba(255,255,255,0.18);
}
/* 반원 배치: 카드 전체가 중심축 기준으로 휘어짐 */
.card:nth-child(1) { --fan: 30deg; }
.card:nth-child(2) { --fan: 10deg; }
.card:nth-child(3) { --fan: -10deg; }
.card:nth-child(4) { --fan: -30deg; }

/* 호버: 카드 전체가 앞으로 나오며 살짝 올라옴 */
.card:hover {
  transform: rotateY(var(--fan)) translateZ(50px) translateY(-10px) scale(1.05);
  box-shadow: 0 20px 40px rgba(0,0,0,0.6);
  z-index: 60;
}
/* 선택(확대): 카드 전체가 중앙으로, 정면 */
.card.selected {
  transform: rotateY(0deg) translateZ(90px) scale(1.4);
  z-index: 100;
  transition: transform 0.45s cubic-bezier(0.2, 1.2, 0.3, 1);
}
.card.selected:hover {
  transform: rotateY(0deg) translateZ(90px) scale(1.4);
}
/* 활성화된 카드 하나만 강조: 나머지는 흐리게 */
.deck:has(.card.selected) .card:not(.selected) {
  opacity: 0.4;
  filter: grayscale(0.4) brightness(0.6);
}

/* 카드 내용: 백그라운드 이미지 + 블러 + 반투명 레이어 + 텍스트 */
.card-bg {
  position: absolute;
  inset: 0;
  border-radius: 16px;
  overflow: hidden;
  background-size: cover;
  background-position: center;
  filter: blur(6px) brightness(0.5);
  /* scale(1.1) 제거 — 블러가 카드 밖으로 튀어나오지 않게 */
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

/* 툴팁: 카드 외부(아래)에 표시, 잘리지 않게 */
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

    card.innerHTML =
      '<div class="card-bg" style="background-image:url(' + img + ')"></div>' +
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
      buildCard(card);
      var href = card.getAttribute('data-href');

      // 마우스 이동: 카드 전체가 기울어짐 (내부가 아니라)
      card.addEventListener('mousemove', function (e) {
        var rect = card.getBoundingClientRect();
        var px = (e.clientX - rect.left) / rect.width;   // 0~1
        var py = (e.clientY - rect.top) / rect.height;   // 0~1
        var rotY = (px - 0.5) * 2 * maxTilt;
        var rotX = (0.5 - py) * 2 * maxTilt;

        if (card.classList.contains('selected')) {
          // 선택 상태: 카드 전체가 마우스 따라 기울어짐
          card.style.transform = 'rotateY(0deg) translateZ(90px) scale(1.4) rotateX(' + rotX.toFixed(1) + 'deg) rotateY(' + rotY.toFixed(1) + 'deg)';
        } else {
          // 호버 상태: 카드 전체가 살짝 기울어짐
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

      // 클릭: 안 된 카드 클릭 = 선택(하나만 활성), 이미 선택된 카드 클릭 = 이동
      card.addEventListener('click', function (e) {
        e.stopPropagation();

        // 이미 선택된 카드를 다시 클릭 → 페이지 이동
        if (card.classList.contains('selected')) {
          window.location.href = href;
          return;
        }

        // 모든 카드 선택 해제 후, 이 카드만 활성화 (하나만)
        var allCards = document.querySelectorAll('.card');
        allCards.forEach(function (c) {
          c.classList.remove('selected');
        });
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
