# 🧠 LLM Wiki

> 개인 지식 베이스. 카드에 마우스를 올리면 3D로 기울어져요. 클릭하면 이동합니다.

## 🏗️ 프로젝트

<div class="deck">

<div class="tilt-card" data-href="projects/unity/링스택/">
  <div class="tilt-card-inner">
    <div class="card-corner top-left">⚙️</div>
    <div class="card-face">
      <div class="card-icon">⚙️</div>
      <div class="card-title">링 스택</div>
      <div class="card-sub">Ring Stack</div>
    </div>
    <div class="card-bottom">
      <div class="card-badge">Unity · 게임</div>
      <div class="card-desc">스택 장르의 타이밍 탭 + 정렬 판정을 회전으로 재구성한 Unity 게임.</div>
    </div>
    <div class="card-corner bottom-right">⚙️</div>
  </div>
</div>

<div class="tilt-card" data-href="projects/">
  <div class="tilt-card-inner">
    <div class="card-corner top-left">📁</div>
    <div class="card-face">
      <div class="card-icon">📁</div>
      <div class="card-title">모든 프로젝트</div>
      <div class="card-sub">All Projects</div>
    </div>
    <div class="card-bottom">
      <div class="card-badge">전체 보기</div>
      <div class="card-desc">프로젝트 도메인 전체 목록과 하위 구조 탐색.</div>
    </div>
    <div class="card-corner bottom-right">📁</div>
  </div>
</div>

</div>

## 🤖 LLM

<div class="deck">

<div class="tilt-card" data-href="llm/사용로그">
  <div class="tilt-card-inner">
    <div class="card-corner top-left">📝</div>
    <div class="card-face">
      <div class="card-icon">📝</div>
      <div class="card-title">LLM 사용로그</div>
      <div class="card-sub">Usage Log</div>
    </div>
    <div class="card-bottom">
      <div class="card-badge">사용 기록</div>
      <div class="card-desc">날짜별 LLM 사용 기록. 무엇을 했고 뭘 배웠는지 append-only로 쌓음.</div>
    </div>
    <div class="card-corner bottom-right">📝</div>
  </div>
</div>

<div class="tilt-card" data-href="llm/프롬프트-패턴">
  <div class="tilt-card-inner">
    <div class="card-corner top-left">💡</div>
    <div class="card-face">
      <div class="card-icon">💡</div>
      <div class="card-title">프롬프트 패턴</div>
      <div class="card-sub">Prompt Patterns</div>
    </div>
    <div class="card-bottom">
      <div class="card-badge">기법</div>
      <div class="card-desc">LLM 사용 중 발견한 유용한 프롬프트/기법 모음.</div>
    </div>
    <div class="card-corner bottom-right">💡</div>
  </div>
</div>

</div>

<style>
.deck {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 1.4rem;
  margin-top: 1rem;
  margin-bottom: 2rem;
  perspective: 1000px;
}
/* 포커카드 비율 5:7 */
.tilt-card {
  aspect-ratio: 5 / 7;
  cursor: pointer;
  transition: transform 0.15s ease-out, box-shadow 0.3s ease;
  border-radius: 14px;
  border: 1px solid var(--border, rgba(128,128,128,0.35));
  background: var(--card, linear-gradient(145deg, rgba(128,128,128,0.14), rgba(128,128,128,0.04)));
  box-shadow: 0 4px 14px rgba(0,0,0,0.12);
  position: relative;
  transform-style: preserve-3d;
  will-change: transform;
}
.tilt-card:hover {
  box-shadow: 0 18px 40px rgba(0,0,0,0.28);
}
.tilt-card-inner {
  position: absolute;
  inset: 0;
  padding: 0.9rem;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  transform-style: preserve-3d;
}
.card-corner { font-size: 1.2rem; opacity: 0.8; }
.card-corner.top-left { align-self: flex-start; }
.card-corner.bottom-right { align-self: flex-end; transform: rotate(180deg); }
.card-face {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  flex: 1;
  gap: 0.4rem;
  transform: translateZ(30px);
}
.card-icon { font-size: 3rem; line-height: 1; filter: drop-shadow(0 4px 8px rgba(0,0,0,0.2)); }
.card-title { font-size: 1.15rem; font-weight: 700; text-align: center; }
.card-sub { font-size: 0.7rem; opacity: 0.55; text-transform: uppercase; letter-spacing: 0.08em; }
.card-bottom {
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
  align-items: center;
  transform: translateZ(20px);
}
.card-badge {
  font-size: 0.68rem;
  padding: 0.15rem 0.6rem;
  border-radius: 999px;
  background: rgba(128,128,128,0.22);
  white-space: nowrap;
}
.card-desc {
  font-size: 0.78rem;
  line-height: 1.4;
  text-align: center;
  color: var(--gray, #888);
  opacity: 0.85;
}
</style>

<script>
(function () {
  function initTilt() {
    var cards = document.querySelectorAll('.tilt-card');
    cards.forEach(function (card) {
      var maxTilt = 16;
      card.addEventListener('mousemove', function (e) {
        var rect = card.getBoundingClientRect();
        var x = (e.clientX - rect.left) / rect.width;   // 0~1
        var y = (e.clientY - rect.top) / rect.height;   // 0~1
        var rotY = (x - 0.5) * 2 * maxTilt;   // -16 ~ +16
        var rotX = (0.5 - y) * 2 * maxTilt;   // +16 ~ -16
        card.style.transform = 'perspective(900px) rotateX(' + rotX.toFixed(1) + 'deg) rotateY(' + rotY.toFixed(1) + 'deg) scale(1.03)';
      });
      card.addEventListener('mouseleave', function () {
        card.style.transform = 'perspective(900px) rotateX(0deg) rotateY(0deg) scale(1)';
      });
      card.addEventListener('click', function () {
        var href = card.getAttribute('data-href');
        if (href) window.location.href = href;
      });
    });
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initTilt);
  } else {
    initTilt();
  }
})();
</script>
