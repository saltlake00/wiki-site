# 🏗️ 프로젝트

> 진행했거나 진행 중인 프로젝트 모음. 카드를 클릭하면 상세 페이지로 이동합니다.

<div class="project-grid">

<div class="project-card">
<a href="projects/unity/링스택/">
<div class="project-card-inner">
<div class="project-icon">⚙️</div>
<div class="project-info">
<div class="project-title">링 스택 (Ring Stack)</div>
<div class="project-badge">Unity · 게임</div>
<div class="project-desc">스택(Stack) 장르의 핵심 재미를 회전으로 재구성한 Unity 게임. 720슬롯 AND 판정, 절차적 메시, 커스텀 NPR 셰이더를 활용한 타이밍 스태킹 게임.</div>
</div>
</div>
</a>
</div>

</div>

<style>
.project-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 1.2rem;
  margin-top: 1rem;
}
.project-card {
  border-radius: 12px;
  overflow: hidden;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  border: 1px solid var(--border, rgba(128,128,128,0.3));
  background: var(--card, rgba(128,128,128,0.08));
}
.project-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0,0,0,0.15);
}
.project-card a { text-decoration: none; color: inherit; display: block; }
.project-card-inner { display: flex; gap: 1rem; padding: 1.2rem; }
.project-icon { font-size: 2.4rem; line-height: 1; }
.project-title { font-size: 1.15rem; font-weight: 600; margin-bottom: 0.3rem; }
.project-badge {
  display: inline-block;
  font-size: 0.75rem;
  padding: 0.15rem 0.6rem;
  border-radius: 999px;
  background: rgba(128,128,128,0.2);
  margin-bottom: 0.5rem;
}
.project-desc { font-size: 0.9rem; line-height: 1.5; color: var(--gray, #888); }
</style>
