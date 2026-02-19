# PROGRESS.md — Skills & Work Package Tracker

> **Purpose:** Pick up exactly where we left off in new sessions.
> **Last Updated:** 2026-02-19

---

## Current Position

- **Active Phase:** AlphaWhale Flagship Roadmap (9 phases, 12 WPs)
- **Active WP:** WP-117 complete — async utilities in py-core
- **Next WP:** WP-118 (FastAPI + SSE Streaming — Phase 2)
- **Blocker:** None
- **Flagship:** AlphaWhale — conversational trading assistant (React chat UI, SSE streaming, RAG, LangGraph agent)

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
| LangChain @tool decorator | ✅ Practised | WP-100 | 🟢 Comfortable |
| LangChain prompt templates | ✅ Practised | WP-100 | 🟢 Comfortable |
| Claude Code skills authoring | ✅ Practised | WP-007 | 🟡 Needs more reps |
| Claude Code hooks | ✅ Practised | WP-007 | 🟡 Needs more reps |
| Claude Code commands (prompts) | ✅ Practised | WP-007 | 🟡 Needs more reps |
| LangSmith tracing | ✅ Practised | WP-106 | 🟢 Comfortable |
| LangGraph StateGraph | ✅ Practised | WP-104 | 🟡 Needs more reps |
| LangGraph human-in-loop | ⬜ Not started | WP-114 | 🔴 |
| BigQuery Python client | ✅ Practised | WP-101 | 🟢 Comfortable |
| Airflow DAGs | ⬜ Not started | WP-102 | 🔴 |
| Technical indicators (RSI/MACD) | ⬜ Not started | WP-103 | 🔴 |
| httpx + asyncio patterns | ✅ Practised | WP-117 | 🟡 Needs more reps |
| FastAPI + SSE streaming | ⬜ Not started | WP-118 | 🔴 |
| TypeScript basics | ⬜ Not started | WP-004 | 🔴 |
| Next.js / React | ⬜ Not started | WP-004 | 🔴 |
| shadcn/ui | ⬜ Not started | WP-004 | 🔴 |
| Redis async + caching | ⬜ Not started | WP-119 | 🔴 |
| Instructor (structured extraction) | ⬜ Not started | WP-120 | 🔴 |
| LangGraph multi-tool agents | ⬜ Not started | WP-114 | 🔴 |
| LangGraph human-in-loop | ⬜ Not started | WP-114 | 🔴 |
| Pinecone + VectorStore abstraction | ⬜ Not started | WP-205 | 🔴 |
| LlamaIndex (RAG ingestion/retrieval) | ⬜ Not started | WP-121 | 🔴 |
| Hybrid search (BM25 + vector) | ⬜ Not started | WP-121 | 🔴 |
| Reranking (Cohere/SentenceTransformer) | ⬜ Not started | WP-121 | 🔴 |
| Firecrawl web scraping | ⬜ Not started | WP-121 | 🔴 |
| RAGAS evaluation | ⬜ Not started | WP-122 | 🔴 |
| Retrieval metrics (MRR, NDCG) | ⬜ Not started | WP-122 | 🔴 |
| HuggingFace fine-tuning (embeddings) | ⬜ Not started | WP-125 | 🔴 |
| HuggingFace Hub (model publishing) | ⬜ Not started | WP-125 | 🔴 |
| AI safety guardrails | ⬜ Not started | WP-124 | 🔴 |
| Logfire + OpenTelemetry | ⬜ Not started | WP-123 | 🔴 |
| FastMCP | ⬜ Not started | WP-112 | 🔴 |
| HuggingFace local models | ⬜ Not started | WP-202 | 🔴 |
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
| WP-100 | LangChain Hello World | Feb 11, 2026 | #52 | 3 finance tools, tool-calling chain, 16 tests, Pydantic auto-schema |
| WP-101 | BigQuery Bronze Layer | Feb 13, 2026 | #53 | Alpha Vantage → BigQuery ingestion, SecretStr, 15 tests, Medallion Bronze |
| WP-104 | LangGraph Hello World | Feb 15, 2026 | #54 | StateGraph, manual tools_node, conditional routing, langgraph 1.0, 13 tests |
| WP-007 | Claude Code Best Practices | Feb 16, 2026 | #55 | 8 skills, 2 commands, hooks, CLAUDE.md audit, MCP audit |
| WP-106 | LangSmith Observability | Feb 17, 2026 | #57 | AgentSettings, auto-tracing with RunnableConfig, evaluation dataset + 2 heuristic evaluators, 25 new tests (70 total) |
| WP-117 | httpx + Async Patterns | Feb 19, 2026 | #125 | AsyncHTTPClient with Tenacity retry, gather_with_concurrency, HTTPClientError, 16 tests |

### 🔄 In Progress
| WP | Title | Started | Est. Completion | Notes |
|----|-------|---------|----------------|-------|
| — | — | — | — | — |

### ⏸️ Deferred
| WP | Title | Reason | Revisit When |
|----|-------|--------|-------------|
| WP-102 | Airflow Hello World | Reprioritized behind AlphaWhale flagship | After flagship complete |
| WP-113 | Airflow Bronze→Silver | Reprioritized behind AlphaWhale flagship | After WP-102 |
| WP-103 (Databricks) | Databricks Feature Eng | User taking a Databricks course separately | After hired |
| WP-301-309 | RailSense (all except WP-304) | Depth > breadth for now | After AlphaWhale flagship |
| WP-308 | Terraform | DevOps skill | After deployment |
| WP-110 | Polymarket API | Nice enrichment, not core | After flagship if time |
| WP-111 | Statistical Treatment | Deep quant work, pairs with LSTM | Side project |
| WP-112 | FastMCP | Learn manual before automatic | After LangGraph agent v1 |

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
| Feb 17 | AlphaWhale designated as monorepo flagship | Conversational trading assistant: React chat UI, SSE, RAG, LangGraph |
| Feb 17 | Pinecone as vector DB with abstraction layer | Factory Pattern in shared lib, DB-agnostic VectorStore interface |
| Feb 17 | LlamaIndex for RAG, LangGraph for orchestration | LlamaIndex QueryEngine wrapped as LangGraph tool — both coexist |
| Feb 17 | Firecrawl for financial news ingestion | Structured markdown from any site, replaces basic RSS approach |
| Feb 17 | Hybrid search: BM25 + vector + reranking | Catches exact terms (tickers, dates) AND semantic meaning |
| Feb 17 | Logfire for app-level observability | Complements LangSmith (LLM-level); native FastAPI/OpenTelemetry |
| Feb 17 | Added WP-124 Guardrails & AI Safety | High-signal AI eng concept: prompt injection, hallucination, PII |
| Feb 17 | Vertical-slice sequencing strategy | Demo-able chat UI by Phase 3, then iterate with depth |

---

## Revised Roadmap Summary

### AlphaWhale Flagship Roadmap (Active)

```
Phase 1: Async Utilities     WP-117  httpx + asyncio patterns (shared lib)
Phase 2: FastAPI + SSE       WP-118  FastAPI backend, SSE streaming
Phase 3: Chat UI             WP-004  Next.js + shadcn/ui, SSE consumption
Phase 4: Redis Caching       WP-119  Redis async, LangChain RedisCache
Phase 5a: Structured Output  WP-120  Instructor + Pydantic extraction
Phase 5b: Agent v1           WP-114  LangGraph multi-tool + human-in-loop
Phase 6a: Vector Store       WP-205  Pinecone abstraction (shared lib)
Phase 6b: RAG Pipeline       WP-121  LlamaIndex + hybrid search + reranking
Phase 7a: RAG Evaluation      WP-122  RAGAS + hit rate/MRR/NDCG
Phase 7b: Embedding Tuning   WP-125  HuggingFace fine-tuning + Hub publishing
Phase 8a: AI Safety          WP-124  Guardrails (input/output validation)
Phase 8b: Observability      WP-123  Logfire + OpenTelemetry
Phase 9: MLflow (RailSense)  WP-304  MLflow tracking (independent track)
```

### Dependency Chain
```
WP-117 → WP-118 → WP-004 (demo-able vertical slice)
WP-117 → WP-205 → WP-121 → WP-122 → WP-125 (RAG pipeline + fine-tuning)
WP-118 → WP-119 → WP-120 → WP-114 (agent orchestration)
WP-114 → WP-124 (guardrails)
WP-118 → WP-123 (observability)
WP-304 (independent)
```

### Previous Roadmap (Superseded)
```
Phase 0: Foundation          Feb 08-12  (2.5 days)   WP-005, WP-006 ✅
Phase 1: LangChain/LangGraph Feb 12-19  (7 days)     WP-100 ✅, WP-101 ✅, WP-106 ✅, WP-104 ✅
Phase 2-5: See AlphaWhale Flagship Roadmap above
```
