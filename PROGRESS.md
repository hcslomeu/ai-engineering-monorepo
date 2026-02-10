# PROGRESS.md — Skills & Work Package Tracker

> **Purpose:** Pick up exactly where we left off in new sessions.
> **Last Updated:** 2026-02-10

---

## Current Position

- **Active Phase:** Phase 0 — Foundation (complete)
- **Active WP:** None (WP-006 complete)
- **Next WP:** WP-100 (LangChain Hello World)
- **Blocker:** None

---

## Skills Tracker

| Skill | Status | Learned In | Confidence |
|-------|--------|-----------|------------|
| Poetry (dependency management) | ✅ Practised | WP-002 | 🟢 Comfortable |
| Pydantic (shared schemas) | ✅ Practised | WP-002 | 🟢 Comfortable |
| Nx monorepo basics | ✅ Practised | WP-001 | 🟡 Needs more reps |
| GitHub Actions (CI) | ✅ Practised | WP-003 | 🟢 Comfortable |
| Ruff (linting + formatting) | ✅ Practised | WP-003 | 🟢 Comfortable |
| Pytest (unit testing) | ✅ Practised | WP-002, WP-003 | 🟢 Comfortable |
| Mypy (type checking) | ✅ Practised | WP-003 | 🟡 Needs more reps |
| Bandit (security scanning) | ✅ Practised | WP-003 | 🟡 Needs more reps |
| Docker multi-stage builds | ✅ Practised | WP-005 | 🟡 Needs more reps |
| Docker Compose | ✅ Practised | WP-005 | 🟡 Needs more reps |
| .dockerignore | ✅ Practised | WP-005 | 🟢 Comfortable |
| MkDocs Material | ✅ Practised | WP-006 | 🟢 Comfortable |
| LangChain @tool decorator | ⬜ Not started | WP-100 | 🔴 |
| LangChain prompt templates | ⬜ Not started | WP-100 | 🔴 |
| LangSmith tracing | ⬜ Not started | WP-106 | 🔴 |
| LangGraph StateGraph | ⬜ Not started | WP-104 | 🔴 |
| LangGraph human-in-loop | ⬜ Not started | WP-114 | 🔴 |
| BigQuery Python client | ⬜ Not started | WP-101 | 🔴 |
| Airflow DAGs | ⬜ Not started | WP-102 | 🔴 |
| Technical indicators (RSI/MACD) | ⬜ Not started | WP-103 | 🔴 |
| FastMCP | ⬜ Not started | WP-112 | 🔴 |
| LlamaIndex (RAG) | ⬜ Not started | WP-204 | 🔴 |
| Pinecone | ⬜ Not started | WP-205 | 🔴 |
| HuggingFace local models | ⬜ Not started | WP-202 | 🔴 |
| TypeScript basics | ⬜ Not started | WP-004 | 🔴 |
| Next.js / React | ⬜ Not started | WP-004, WP-107 | 🔴 |
| shadcn/ui | ⬜ Not started | WP-004, WP-107 | 🔴 |
| WhatsApp Evolution API | ⬜ Not started | WP-105 | 🔴 |
| n8n workflows | ⬜ Not started | WP-115 | 🔴 |

---

## Work Package Log

### ✅ Completed
| WP | Title | Date Completed | PR | Notes |
|----|-------|---------------|-----|-------|
| WP-001 | Monorepo Foundation Scaffold | Jan 26, 2026 | — | Nx + pnpm + Poetry hybrid workspace |
| WP-002 | py-core Shared Library | Feb 6, 2026 | #35 | Pydantic config, structlog logging, custom exceptions, 13 tests |
| WP-003 | CI Pipeline | Feb 9, 2026 | #36 | 4 parallel jobs: pytest, ruff, bandit, mypy |
| WP-005 | Docker Base Images | Feb 10, 2026 | #47 | Python + Node multi-stage Dockerfiles, Compose, .dockerignore |
| WP-006 | MkDocs Documentation | Feb 10, 2026 | #49 | MkDocs Material site, 9 docs pages, deploy-docs workflow, Nx target |

### 🔄 In Progress
| WP | Title | Started | Est. Completion | Notes |
|----|-------|---------|----------------|-------|
| — | — | — | — | — |

### ⏸️ Deferred
| WP | Title | Reason | Revisit When |
|----|-------|--------|-------------|
| WP-004 | ts-core + Shared Frontend Scaffold | No TS needed until UI phase | Phase 3 (~Feb 25) |
| WP-103 (Databricks) | Databricks Feature Eng | User taking a Databricks course separately | After hired |
| WP-301-309 | RailSense (all) | Depth > breadth for now | After Phase 4 |
| WP-304 | PyTorch LSTM | ML Eng skill, side project | Side project |
| WP-308 | Terraform | DevOps skill | After deployment |
| WP-110 | Polymarket API | Nice enrichment, not core | After Phase 3 if time allows |
| WP-111 | Statistical Treatment | Deep quant work, pairs with LSTM | Side project |

---

## Decisions Made

| Date | Decision | Rationale |
|------|----------|-----------|
| Feb 8 | AlphaWhale 100% first, then decide next project | Job urgency — need demo-able portfolio fast |
| Feb 8 | Keep: LangGraph, LlamaIndex, LangSmith, Airflow | Core AI Eng skills for target roles |
| Feb 8 | Add FastMCP (after LangGraph, not before) | Learn manual before automatic — understand what MCP abstracts |
| Feb 8 | Defer Databricks, Kafka, PyTorch, Terraform | These are adjacent roles (Data Eng, ML Eng, DevOps) |
| Feb 8 | Defer RailSense entirely (not deleted) | 2 projects deep > 3 projects shallow |
| Feb 8 | LSTM/statistical modelling → side project | Fascinating but ML Eng territory, not AI Eng priority |
| Feb 9 | CI Pipeline is CI only (not CD) | CD added later when there's something to deploy |
| Feb 9 | Split WP-102 into Hello World + Bronze→Silver (WP-113) | Pedagogical split: learn Airflow first, then build real pipeline |
| Feb 9 | Split WP-104 into Hello World + Agent v1 (WP-114) | Same pattern: learn LangGraph basics, then build full agent |
| Feb 9 | Unified frontend: single Next.js app for all projects | One URL for recruiters, shared design system, routes per project (/alphawhale, /mediguard, /railsense) |
| Feb 9 | WP-004 expanded to include frontend scaffold | ts-core + Next.js setup + shadcn/ui + shared layout, routing |
| Feb 9 | WP-107/207/307 become "Frontend Views" per project | Each adds its project-specific views to the shared app |
| Feb 9 | Added WP-504 Portfolio Landing Page | The `/` route of the unified app, built with Claude frontend skill |
| Feb 9 | Added WP-115 n8n Agent Orchestration | Workflow orchestration layer for agent triggers and notifications |

---

## Revised Roadmap Summary

```
Phase 0: Foundation          Feb 08-12  (2.5 days)   WP-005, WP-006
Phase 1: LangChain/LangGraph Feb 12-19  (7 days)     WP-100, WP-101, WP-106, WP-104, WP-114
Phase 2: Data Eng + Airflow  Feb 19-25  (7 days)     WP-102, WP-113, WP-103, WP-109
Phase 3: UI + Integration    Feb 25-Mar4 (7 days)    WP-004, WP-107, WP-105, WP-108, WP-115
Phase 4: FastMCP + MediGuard Mar 04-13  (9.5 days)   WP-112, WP-201-206, WP-207
Phase 5: Polish + Deploy     Mar 13-18  (5 days)     WP-500-504
                                         TOTAL: ~39 working days (~6 weeks)
```
