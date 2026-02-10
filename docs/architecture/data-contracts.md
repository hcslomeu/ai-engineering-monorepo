# Data Contracts

## Medallion Architecture

All data pipelines follow a three-layer pattern: **Bronze → Silver → Gold**. Each layer has a clear purpose and strict boundaries.

```text
  External APIs          Kafka Topics          Webhooks
       │                      │                    │
       ▼                      ▼                    ▼
┌─────────────────────────────────────────────────────────┐
│  Bronze (Raw)          No transformation, just store    │
└──────────────────────────┬──────────────────────────────┘
                           ▼
┌─────────────────────────────────────────────────────────┐
│  Silver (Cleaned)      Validate, deduplicate, conform   │
└──────────────────────────┬──────────────────────────────┘
                           ▼
┌─────────────────────────────────────────────────────────┐
│  Gold (Feature-Ready)  Aggregate, embed, serve          │
└─────────────────────────────────────────────────────────┘
```

| Layer | Purpose | Examples |
|-------|---------|---------|
| **Bronze** | Raw ingestion — store exactly what arrived | Raw API responses, Kafka messages, webhook payloads |
| **Silver** | Cleaned and conformed — validate against schemas, standardise timestamps (UTC), deduplicate | Pydantic-validated records, PII-tagged fields |
| **Gold** | Feature-ready — aggregations, vector embeddings, ML features | Daily transaction rollups, RAG-ready embeddings |

### Rules

- **Bronze never transforms.** If the source sends invalid JSON, Bronze stores the invalid JSON. Fixing happens in Silver.
- **Silver validates against data contracts.** Every record that passes Silver conforms to a JSON Schema definition.
- **Gold is use-case specific.** Different consumers (agents, dashboards, ML models) may need different Gold tables from the same Silver data.

## Schema Flow

Data contracts ensure that Python backends and TypeScript frontends always agree on data shapes.

```text
libs/schemas/definitions/        ← JSON Schema (source of truth)
       │
       ├──→ libs/schemas/generated/python/       ← Pydantic models (auto-generated)
       │
       └──→ libs/schemas/generated/typescript/   ← Zod schemas (auto-generated)
```

### Why JSON Schema as the source of truth?

JSON Schema is **language-neutral**. By defining data shapes once in JSON Schema, we can generate type-safe models for any language:

- **Python** → Pydantic models (runtime validation + type hints)
- **TypeScript** → Zod schemas (runtime validation + TypeScript types)

If a field changes in the JSON Schema, both generated outputs update together. No drift between backend and frontend.

### How it works in practice

1. Define or update a schema in `libs/schemas/definitions/`
2. Run the code generation step (generates Pydantic + Zod)
3. Import the generated models in your Python/TypeScript code
4. The Silver layer uses the Pydantic models for validation
5. The frontend uses the Zod schemas for form validation and API responses

!!! warning "Not yet implemented"
    The schema generation pipeline will be built in later work packages. This page documents the intended architecture.