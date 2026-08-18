# Wiki Schema

## Domain
개인 지식 베이스 — 일상 업무, 개인 취미, 프로그램 개발 전반을 아우르는
지속적으로 축적되는 개인 위키. RAG처럼 매번 검색하지 않고, 지식을 한 번
정리해서 계속 갱신한다.

## Conventions
- File names: lowercase, hyphens, no spaces (e.g., `transformer-architecture.md`)
- Every wiki page starts with YAML frontmatter (see below)
- Use `[[wikilinks]]` to link between pages (minimum 2 outbound links per page)
- When updating a page, always bump the `updated` date
- Every new page must be added to `index.md` under the correct section
- Every action must be appended to `log.md`
- **Provenance markers:** On pages that synthesize 3+ sources, append `^[raw/articles/source-file.md]`
  at the end of paragraphs whose claims come from a specific source.
- **이미지 규칙:** 이미지는 Git에 커밋하지 않는다. `raw/assets/` 폴더에 두고
  `![[이미지.png]]`로 참조. (Git 저장소를 가볍게 유지하기 위함)

## 폴더 구조 (도메인별 분리)

위키는 **도메인(영역)별로 폴더를 나눠** 관리한다. 프로젝트/취미/업무/LLM 등
서로 다른 영역이 섞이지 않도록 한다.

```
wiki/
├── SCHEMA.md / index.md / log.md
├── raw/                    # 원본 자료 (도메인별 하위 폴더)
│   └── <도메인>/<하위>/<항목>/
├── projects/               # 프로젝트 도메인
│   └── <기술/분야>/<프로젝트명>/
│       ├── <프로젝트>-개요.md
│       ├── <프로젝트>-<기능>.md
│       └── ...
├── concepts/               # 공통 개념 (여러 도메인에 걸쳐 쓰이는 것만)
├── comparisons/            # 공통 비교 (여러 도메인에 걸친 것만)
└── queries/                # 저장할 가치 있는 질문 결과
```

**핵심 원칙:**
- **프로젝트는 자기 폴더에 전부** — 개요/기능/비교 페이지가 한 곳에 모인다.
- **`concepts/`는 진짜 공통 개념만** — 여러 프로젝트/도메인에 걸쳐 쓰이는 것만 여기로.
- **`type`은 frontmatter에 유지** — 폴더가 바뀌어도 entity/concept/comparison 구분은 남는다.
- **새 프로젝트 추가 시**: `projects/<분야>/<프로젝트명>/` 폴더를 만들고 그 안에 페이지를 넣는다.

## Frontmatter
  ```yaml
  ---
  title: Page Title
  created: YYYY-MM-DD
  updated: YYYY-MM-DD
  type: entity | concept | comparison | query | summary
  tags: [from taxonomy below]
  sources: [raw/articles/source-name.md]
  # Optional quality signals:
  confidence: high | medium | low
  contested: true
  contradictions: [other-page-slug]
  ---
  ```

### raw/ Frontmatter
  ```yaml
  ---
  source_url: https://example.com/article
  ingested: YYYY-MM-DD
  sha256: <hex digest of the raw content below the frontmatter>
  ---
  ```

## Tag Taxonomy
최상위 도메인 태그 (10-20개 유지. 새 태그는 여기에 먼저 추가 후 사용):

- **업무**: 업무, 회의, 프로젝트, 문서, 커뮤니케이션
- **개발**: 개발, 프로그래밍, 언어, 프레임워크, 도구, 알고리즘, 데이터베이스, 보안, DevOps, AI/ML
- **취미**: 취미, 게임, 음악, 영화, 독서, 운동, 요리, 여행
- **개인**: 건강, 재정, 습관, 목표, 일상
- **메타**: 비교, 타임라인, 논쟁, 예측, 리뷰

Rule: every tag on a page must appear in this taxonomy. If a new tag is needed,
add it here first, then use it.

## Page Thresholds
- **Create a page** when an entity/concept appears in 2+ sources OR is central to one source
- **Add to existing page** when a source mentions something already covered
- **DON'T create a page** for passing mentions, minor details, or things outside the domain
- **Split a page** when it exceeds ~200 lines — break into sub-topics with cross-links
- **Archive a page** when its content is fully superseded — move to `_archive/`, remove from index

## Entity Pages
One page per notable entity. Include:
- Overview / what it is
- Key facts and dates
- Relationships to other entities ([[wikilinks]])
- Source references

## Concept Pages
One page per concept or topic. Include:
- Definition / explanation
- Current state of knowledge
- Open questions or debates
- Related concepts ([[wikilinks]])

## Comparison Pages
Side-by-side analyses. Include:
- What is being compared and why
- Dimensions of comparison (table format preferred)
- Verdict or synthesis
- Sources

## Update Policy
When new information conflicts with existing content:
1. Check the dates — newer sources generally supersede older ones
2. If genuinely contradictory, note both positions with dates and sources
3. Mark the contradiction in frontmatter: `contradictions: [page-name]`
4. Flag for user review in the lint report
