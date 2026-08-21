---
title: 게임 개발
created: 2026-08-20
updated: 2026-08-21
type: index
status: active
tags: [개발, 게임]
sources: []
---

# 게임 개발

> 게임 개발 도메인 진입점. Unity 게임 프로젝트, 에셋 워크플로우, 엔진 개념, 학습 노트.
> **엔진(Unity)은 폴더가 아니라 태그로 구분한다** — 게임 개발은 한 도메인이다.

## 게임 프로젝트
- [[projects/gamedev/링스택/index|링 스택]] — 스택 장르의 타이밍 탭 + 정렬 판정을 회전으로 재구성한 Unity 게임
  - [[링스택-게임]] — 개요·기술 스택·구조
  - [[링스택-판정로직]] — 720슬롯 각도 배열 기반 겹침 AND 판정
  - [[링스택-절차적-메시]] — 슬롯 패턴 → 3D 메시 절차적 생성
  - [[링스택-셰이더]] — ToonNPR 카툰 셰이더 + 반투명 Unlit 가이드
  - [[링스택-색상-팔레트]] — OKLCH 기반 층별 색 그라데이션
  - [[링스택-카메라]] — 아이소메트릭 추적 카메라 + 게임오버 리빌
  - [[링스택-vs-원본스택]] — 원본 Stack 대비 차별점

## 에셋 워크플로우 / 도구
- [[projects/gamedev/pixel-sprite-workflow/index|픽셀아트 스프라이트 워크플로우]] — AI 이미지 → 도트 스프라이트 → Unity 애니메이션 파이프라인 (허브)
  - [[projects/gamedev/pixel-sprite-workflow/workflow-a-ai-image|워크플로우 A]] — AI 이미지 경로 (기본)
  - [[projects/gamedev/pixel-sprite-workflow/workflow-b-3d-render|워크플로우 B]] — 3D 렌더 / 던파 방식
  - [[projects/gamedev/pixel-sprite-workflow/workflow-c-opensource-tools|워크플로우 C]] — 오픈소스 도구 비교
  - [[projects/gamedev/pixel-sprite-workflow/troubleshooting|품질·트러블슈팅]]
- [[projects/gamedev/varco-3d/index|VARCO 3D MCP]] — 브라우저 워크플로우를 MCP로 제어해 3D/캐릭터 에셋 생성
- [[projects/gamedev/unity-gamedev-prompt-template/index|Unity 게임개발 클로드 프롬프트 템플릿]] — 어떤 Unity 게임이든 재사용하는 범용 시작 프롬프트

## 엔진 개념
- [[2D-타일맵]] — Sprite/Sorting Order, Pixel Per Unit, Rule Tile, Override Tile, Tilemap Collider, Cinemachine

## 학습 노트
- [[projects/gamedev/unity-2d-platformer/index|Unity 2D 플랫포머]] — 스프라이트 애니메이션·정렬, 타일맵, 시네머신, 조작감
- [[projects/gamedev/ncai-varco-lecture/index|NC AI·VARCO 강의 노트]] — VARCO 소개, 바이브 코딩 게임 제작, 게임 직군·취업

## 관련
- [[projects/index|모든 프로젝트]]
- [[projects/llm/index|LLM 도구·프로젝트]] — 에이전트/프롬프트 쪽 지식
