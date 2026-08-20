# 🧠 LLM Wiki

> 개인 지식 베이스. 손에 쥔 카드처럼 펼쳐진 카드를 탐색해보세요.
> **호버** = 살짝 올라옴 · **클릭 1번** = 확대 + 마우스 따라 기울임 · **클릭 2번** = 페이지 이동

<div class="deck">

<div class="card" data-href="projects/" data-img="assets/cards/all-projects.svg" data-icon="📁" data-title="모든 프로젝트" data-sub="All Projects" data-badge="전체 보기" data-desc="프로젝트 도메인 전체 목록과 하위 구조 탐색."></div>

<div class="card" data-href="projects/gamedev/pixel-sprite-workflow/" data-img="" data-icon="🎨" data-title="🎮 도트 스프라이트 제작" data-sub="" data-badge="" data-desc=""></div>

<div class="card" data-href="projects/gamedev/unity-2d-platformer/" data-img="" data-icon="🕹️" data-title="🎮 Unity 2D 플랫포머" data-sub="" data-badge="" data-desc=""></div>

<div class="card" data-href="projects/gamedev/unity-gamedev-prompt-template/" data-img="" data-icon="📋" data-title="📋 Unity 게임개발 클로드 프롬프트" data-sub="" data-badge="" data-desc=""></div>

<div class="card" data-href="projects/gamedev/varco-3d/" data-img="" data-icon="🧊" data-title="🧊 VARCO 3D 캐릭터 생성" data-sub="" data-badge="" data-desc=""></div>

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
.card:nth-child(1) { --fan: 24deg; }
.card:nth-child(2) { --fan: 8deg; }
.card:nth-child(3) { --fan: -8deg; }
.card:nth-child(4) { --fan: -24deg; }
.card:nth-child(5) { --fan: 40deg; }
.card:nth-child(6) { --fan: 16deg; }
.card:nth-child(7) { --fan: 0deg; }
.card:nth-child(8) { --fan: -16deg; }
.card:nth-child(9) { --fan: -40deg; }
.card:nth-child(10) { --fan: -56deg; }
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
  var maxTilt = 16;
  var selectedCard = null;
  var lastSelectTime = 0;   // 전역 쿨다운 (확대 직후 바로 이동 방지)

  // 카드 내부 내용 채우기 (빌드)
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
    card.dataset.built = '1';
  }

  // 현재 홈의 카드들 빌드 (이미 빌드됐으면 스킵)
  function ensureCardsBuilt() {
    document.querySelectorAll('.card:not([data-built])').forEach(function (card) {
      buildCard(card);
    });
  }

  // 클릭 처리 — document에 위임 (SPA 전환 후에도 유지, 중복 없음)
  document.addEventListener('click', function (e) {
    var card = e.target.closest('.card');
    var now = Date.now();

    if (!card) {
      // 카드 바깥 클릭 → 선택 해제
      if (selectedCard) {
        selectedCard.classList.remove('selected');
        selectedCard = null;
      }
      return;
    }

    var href = card.getAttribute('data-href');

    // 확대(선택) 상태에서 클릭
    if (card.classList.contains('selected')) {
      // 확대 직후(600ms) 클릭은 무시 — 확대 화면을 볼 시간 확보
      if (now - lastSelectTime < 600) return;
      window.location.href = href;
      return;
    }

    // 일반 카드 클릭 → 확대 (하나만)
    document.querySelectorAll('.card').forEach(function (c) {
      c.classList.remove('selected');
    });
    card.classList.add('selected');
    selectedCard = card;
    lastSelectTime = now;
  });

  // 마우스 이동 → 카드 전체 3D 틸트 (마우스 리스너는 카드별)
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
  });

  // 초기 빌드
  function init() {
    ensureCardsBuilt();
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  // Quartz SPA 페이지 전환: 홈에 돌아오면 카드 다시 빌드 (내용 사라짐 방지)
  document.addEventListener('nav', function () {
    if (document.querySelector('.card')) {
      // DOM이 교체됐을 수 있으므로 빌드 플래그 리셋 후 재빌드
      document.querySelectorAll('.card').forEach(function (c) {
        delete c.dataset.built;
        delete c.dataset.tiltInit;
      });
      ensureCardsBuilt();
      if (selectedCard) { selectedCard.classList.remove('selected'); selectedCard = null; }
      lastSelectTime = 0;
    }
  });
})();

</script>
