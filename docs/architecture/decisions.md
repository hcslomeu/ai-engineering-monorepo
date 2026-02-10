# Architectural Decisions

Key decisions made during the project, with rationale. New decisions are added as they arise.

## ADR-001: Hybrid Monorepo (Poetry + pnpm + Nx)

**Decision:** Use Poetry for Python, pnpm for TypeScript, and Nx as the cross-language orchestrator.

**Rationale:** Python and TypeScript have incompatible dependency ecosystems. Rather than forcing a single tool, each language uses its native package manager. Nx coordinates tasks across both without caring about the underlying language.

**Alternatives considered:** Turborepo (TypeScript-only), Pants (steeper learning curve), Bazel (enterprise complexity).

## ADR-002: AlphaWhale First, Then MediGuard

**Decision:** Complete AlphaWhale (finance) end-to-end before starting MediGuard (healthcare).

**Rationale:** Job urgency requires a demo-able portfolio fast. Depth in one project is more impressive than shallow progress across three. AlphaWhale covers the most in-demand skills (LangGraph, Airflow, BigQuery).

## ADR-003: Unified Frontend

**Decision:** Build a single Next.js application with routes per project (`/alphawhale`, `/mediguard`, `/railsense`) instead of three separate frontends.

**Rationale:** One URL for recruiters, shared design system (shadcn/ui), single deployment. Reduces duplication and gives a polished portfolio experience.

## ADR-004: CI Only (No CD Yet)

**Decision:** The GitHub Actions pipeline covers CI (test, lint, security, typecheck) but not CD.

**Rationale:** There's nothing to deploy yet. CD will be added when there's a deployable application (API or frontend).

## ADR-005: RailSense Deferred

**Decision:** Defer all RailSense work packages. Keep them in the backlog but don't schedule them.

**Rationale:** Two projects deep is more valuable than three projects shallow. RailSense skills (Kafka, PyTorch LSTM) are adjacent to AI Engineering but not core to target roles.

## ADR-006: Learn LangGraph Before FastMCP

**Decision:** Implement LangGraph agents manually before using FastMCP for automation.

**Rationale:** Understanding what MCP abstracts away is essential before using the abstraction. Learn the manual approach first, then appreciate what FastMCP simplifies.

## ADR-007: Pedagogical WP Splitting

**Decision:** Split complex work packages into "Hello World" + "Real Implementation" pairs (e.g., WP-102 → WP-102 + WP-113 for Airflow, WP-104 → WP-104 + WP-114 for LangGraph).

**Rationale:** Learning a new framework and building a production feature at the same time leads to confusion. Separating them means the first WP focuses purely on learning the tool, and the second WP applies it to a real use case.