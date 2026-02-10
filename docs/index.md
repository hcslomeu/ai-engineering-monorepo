---
template: home.html
hide:
  - navigation
  - toc
---

## Projects

<div class="project-grid" markdown>

<div class="project-card" markdown>

### AlphaWhale

**Finance** — BigQuery, Airflow, LangGraph, WhatsApp (Evolution API)

AI-powered financial analysis with agentic workflows and real-time notifications.

</div>

<div class="project-card" markdown>

### MediGuard

**Healthcare** — FHIR APIs, Hugging Face (PII masking), LlamaIndex

Clinical document processing with PII protection and RAG-based retrieval.

</div>

<div class="project-card" markdown>

### RailSense

**Transportation** — Kafka, PyTorch LSTM, Supabase, CrewAI

Real-time rail disruption prediction with streaming data and ML models.

</div>

</div>

## Tech Stack

<div class="tech-stack" markdown>

<span class="tech-pill">Python</span>
<span class="tech-pill">TypeScript</span>
<span class="tech-pill">LangGraph</span>
<span class="tech-pill">LlamaIndex</span>
<span class="tech-pill">Airflow</span>
<span class="tech-pill">FastAPI</span>
<span class="tech-pill">Next.js</span>
<span class="tech-pill">Docker</span>
<span class="tech-pill">Nx</span>
<span class="tech-pill">GitHub Actions</span>

</div>

## Repository Layout

```
ai-engineering-monorepo/
├── libs/              # Shared libraries (py-core, py-agents, py-retrieval, ...)
├── apps/              # Applications (alpha-whale, medi-guard, rail-sense)
├── pipelines/         # Data engineering (Airflow DAGs, Databricks jobs)
├── tests/             # Integration & E2E tests
├── docs/              # This documentation site
└── infra/             # Docker & Terraform
```
