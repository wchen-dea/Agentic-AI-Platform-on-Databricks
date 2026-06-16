# Agentic Application

Agentic Application is an enterprise AI agent system for building and operationalizing one or more collaborating agents that can execute complex tasks.

Instead of relying on a single model call, the platform combines multiple interacting components, including large language models (LLMs), classical machine learning (ML) models, enterprise data, and external tools, to achieve business goals reliably and efficiently.

The system is designed with built-in evaluation and governance so outputs can be measured against defined objectives while maintaining security, compliance, and accountability across the full workflow.

In this repository, that model is implemented as a supervisor-driven multi-agent engineering runtime with specialist agents, shared memory, typed messaging, and environment-driven dependency wiring via the runtime factory.

This repository is a reference project (proof-of-concept style) that demonstrates architecture, orchestration patterns, and collaboration primitives in a practical end-to-end setup.

It is intentionally designed to be extended into real-time operational analytics support, where enterprise teams can evolve this foundation into production-grade data and AI workflows.

Modern data engineering in this context emphasizes event-driven, cloud-native, governed, and automated data platforms that deliver trusted, real-time data products using software engineering principles.

## Agent System Lifecycle

- Prepare data: organize and preprocess enterprise data so it is accessible and relevant for agent reasoning and interactions.
- Build agents: compose generative AI models, classical ML models, and tools for role-specific tasks.
- Deploy agents: run agents in production settings with secure, reliable interactions across users and systems.
- Evaluate performance: continuously measure output quality and progress against target outcomes.
- Govern operations: enforce security, compliance, and ethical standards with end-to-end operational visibility.

## Why This Project

- Multi-agent orchestration with explicit specialist roles.
- Pydantic AI tool layer: auto-generated schemas, typed deps via `RunContext`, and validated `AgentResult`.
- Collaboration primitives for memory sharing and inter-agent messaging.
- Databricks-backed retrieval through an MCP gateway.
- Packaging and deployment support with `uv`, wheel builds, and Databricks CI/CD.
- Explicit runtime assembly via `runtime_factory.py` for predictable startup behavior.

## Specialist Agents

| Agent | Focus |
| --- | --- |
| frontend | React, TypeScript, Tailwind, accessibility |
| backend | FastAPI, SQLAlchemy, auth, API design |
| ml_engineer | Model training pipelines and MLOps workflows |
| ai_engineer | LLM applications, RAG, tool use, prompts |
| fullstack | End-to-end product implementation |
| data_engineer | ETL/ELT, orchestration, data platform |
| data_scientist | EDA, experiments, statistical analysis |

## Quick Start

```bash
uv sync
cp .env.example .env
# set required variables (at minimum: ANTHROPIC_API_KEY)
uv run multi-ai-agent --task "build a user authentication system"
uv run multi-ai-agent --task "build a user authentication system" --implementation langgraph
```

Optional environment-driven runtime defaults:

- `AI_APP_IMPLEMENTATION` (`classic` or `langgraph`)
- `SUPERVISOR_MAX_WORKERS` (default: `4`)
- `ANTHROPIC_MODEL` (default: `claude-opus-4-7`)
- `ANTHROPIC_MAX_TOKENS` (default: `8096`)
- `SUPERVISOR_MAX_ITERATIONS` (default: `40`)
- `MONGODB_URI` / `MONGODB_DB` / `MONGODB_MEMORY_COLLECTION`
- `RABBITMQ_URL`

If MongoDB or RabbitMQ is unavailable, the app degrades to in-memory collaboration backends so local iteration can continue.

## Useful Commands

```bash
make sync
make run TASK="build a RAG chatbot"
make run-quiet TASK="build a data pipeline"
make run-reset TASK="redesign the recommendation engine"
uv run multi-ai-agent --task "build a RAG chatbot" --implementation langgraph
make build-wheel
```

For runtime operations and deployment details, see the runbook.

## Documentation

- [Architecture](docs/architecture.md)
- [Runbook](docs/runbook.md)
- [ADRs](docs/adrs/README.md)
- [Container Setup](container/README.md)

## Project Structure

```text
agentic-application/
├── src/
│   └── ai_app/
│       ├── main.py
│       ├── runtime_factory.py
│       ├── settings.py
│       ├── orchestration.py
│       ├── supervisor.py
│       ├── supervisor_langgraph.py
│       ├── integrations/
│       ├── agents/
│       │   └── registry.py
│       ├── utils/
│       │   ├── memory.py
│       │   └── message_bus.py
│       └── resources/
├── docs/
│   ├── adrs/
│   ├── architecture.md
│   └── runbook.md
├── container/
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── README.md
├── .github/workflows/
├── scripts/
├── pyproject.toml
└── uv.lock
```
