# 🧠 LLM Wiki

> 개인 지식 베이스. 프로젝트 / LLM / 개념을 카드로 탐색하세요.

## 🏗️ 프로젝트

<div class="project-grid">

<div class="project-card" onclick="window.location.href='projects/unity/링스택/';" style="cursor:pointer;">
<div class="project-card-inner">
<div class="project-icon">⚙️</div>
<div class="project-info">
<div class="project-title">링 스택 (Ring Stack)</div>
<div class="project-badge">Unity · 게임</div>
<div class="project-desc">스택 장르의 타이밍 탭 + 정렬 판정을 회전으로 재구성한 Unity 게임. 720슬롯 AND 판정, 절차적 메시, NPR 셰이더.</div>
</div>
</div>
</div>

<div class="project-card" onclick="window.location.href='projects/';" style="cursor:pointer;">
<div class="project-card-inner">
<div class="project-icon">📁</div>
<div class="project-info">
<div class="project-title">모든 프로젝트</div>
<div class="project-badge">전체 보기</div>
<div class="project-desc">프로젝트 도메인 전체 목록과 하위 구조 탐색.</div>
</div>
</div>
</div>

</div>

## 🤖 LLM

<div class="project-grid">

<div class="project-card" onclick="window.location.href='llm/사용로그';" style="cursor:pointer;">
<div class="project-card-inner">
<div class="project-icon">📝</div>
<div class="project-info">
<div class="project-title">LLM 사용로그</div>
<div class="project-badge">사용 기록</div>
<div class="project-desc">날짜별 LLM 사용 기록. 무엇을 했고 뭘 배웠는지 append-only로 쌓음.</div>
</div>
</div>
</div>

<div class="project-card" onclick="window.location.href='llm/프롬프트-패턴';" style="cursor:pointer;">
<div class="project-card-inner">
<div class="project-icon">💡</div>
<div class="project-info">
<div class="project-title">프롬프트 패턴</div>
<div class="project-badge">기법</div>
<div class="project-desc">LLM 사용 중 발견한 유용한 프롬프트/기법 모음.</div>
</div>
</div>
</div>

</div>

<style>
.project-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 1.2rem;
  margin-top: 1rem;
  margin-bottom: 2rem;
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
