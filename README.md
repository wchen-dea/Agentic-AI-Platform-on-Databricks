# Agentic Application

Agentic Application is a reference implementation for modern data domain management with collaborating AI specialists.

Core idea:

- Model capability is not the unique advantage.
- Durable value comes from combining models with trusted data, typed tools, and governed orchestration.

## What It Includes

- Supervisor-specialist orchestration with quality gates (peer review and revision).
- Typed tool layer built with Pydantic AI.
- Shared collaboration primitives: memory + message bus.
- MCP-based retrieval from Databricks-backed sources.
- Operational grounding via Lakebase metrics (Kafka, Flink, Aurora from CloudWatch/Grafana pipeline).
- Local/container runtime plus Databricks CI/CD deployment path.

## Specialist Team

| Specialist Key | Role | Primary Focus |
| --- | --- | --- |
| `frontend` | AI Frontend Engineer | UX and UI delivery surfaces |
| `backend` | AI Backend Engineer | APIs, services, auth, data contracts |
| `ml_engineer` | AI Machine Learning Engineer | Training pipelines and MLOps |
| `ai_engineer` | AI Engineer | LLM apps, RAG, prompt/tool flows |
| `fullstack` | AI Full-Stack Engineer | End-to-end feature delivery |
| `data_engineer` | AI Data Engineer | ETL/ELT, orchestration, data platform |
| `data_scientist` | AI Data Scientist | EDA, experimentation, statistical analysis |
| `database_admin` | AI Database Admin | DB operations, reliability, governance |
| `stream_engineer` | AI Stream Engineer | Kafka/Flink operations and incident response |

## Quick Start

```bash
uv sync
cp .env.example .env
# set at minimum: ANTHROPIC_API_KEY

uv run multi-ai-agent --task "build a user authentication system"
uv run multi-ai-agent --task "build a user authentication system" --implementation langgraph
```

Useful commands:

```bash
make sync
make run TASK="build a RAG chatbot"
make run-quiet TASK="build a data pipeline"
make run-reset TASK="redesign recommendation engine"
make build-wheel
```

## Runtime Configuration

Common environment controls:

- `AI_APP_IMPLEMENTATION` (`classic` or `langgraph`)
- `SUPERVISOR_MAX_WORKERS`
- `SUPERVISOR_MAX_ITERATIONS`
- `ANTHROPIC_MODEL`, `ANTHROPIC_MAX_TOKENS`
- `MONGODB_URI` / `MONGODB_DB` / `MONGODB_MEMORY_COLLECTION`
- `RABBITMQ_URL`
- `DATABRICKS_MCP_URL`, `DATABRICKS_TOKEN`, MCP tool/source variables

If MongoDB or RabbitMQ is unavailable, the runtime degrades to in-memory collaboration backends for local iteration.

## Repository Layout

```text
src/ai_app/
  agents/            # AI specialist implementations and registry
  integrations/      # MCP data source gateway
  utils/             # memory and message bus backends
  orchestration.py   # supervisor prompt + tool contracts
  supervisor.py      # classic orchestration
  supervisor_langgraph.py
  runtime_factory.py # dependency wiring from env
```

## Documentation

- [Architecture](docs/architecture.md)
- [Runbook](docs/runbook.md)
- [ADRs](docs/adrs/README.md)
- [Container Setup](container/README.md)

Key ADRs:

- [ADR-0005: Pydantic AI Tool Layer](docs/adrs/0005-pydantic-ai-tool-layer.md)
- [ADR-0006: Layered Prompt Engineering Design](docs/adrs/0006-prompt-engineering-layered-governed-design.md)
