# Agentic Application

Agentic Application is an enterprise AI agent system for building and operationalizing one or more collaborating agents that can execute complex tasks.

Instead of relying on a single model call, the platform combines multiple interacting components, including large language models (LLMs), classical machine learning (ML) models, enterprise data, and external tools, to achieve business goals reliably and efficiently.

The system is designed with built-in evaluation and governance so outputs can be measured against defined objectives while maintaining security, compliance, and accountability across the full workflow.

In this repository, that model is implemented as a supervisor-driven multi-agent engineering runtime with specialist agents, shared memory, typed messaging, and environment-driven dependency wiring via the runtime factory.

This repository is a reference project (proof-of-concept style) that demonstrates architecture, orchestration patterns, and collaboration primitives in a practical end-to-end setup.

It is intentionally designed to be extended into real-time operational analytics support, where enterprise teams can evolve this foundation into production-grade data and AI workflows.

Modern data engineering in this context emphasizes event-driven, cloud-native, governed, and automated data platforms that deliver trusted, real-time data products using software engineering principles.

## Extending The POC To Industry Domains

This project is intentionally generic as a POC. To evolve it into a domain-specific implementation, keep the supervisor-specialist runtime unchanged and add domain packs around it.

- Keep orchestration stable: reuse the existing supervisor loop and specialist collaboration model.
- Add domain data contracts: define industry-specific schemas, quality checks, and retrieval indexes in Databricks.
- Add domain guardrails: codify compliance and policy constraints in prompts, tool checks, and approval steps.
- Add domain playbooks: encode operational runbooks and escalation paths in memory templates and specialist prompts.

Retail example:

- Prioritize use cases such as demand forecasting, promotion analytics, pricing optimization, and inventory health.
- Extend Lakebase ingestion with POS, e-commerce, fulfillment, and customer-support telemetry.
- Add retail KPIs (stockout rate, basket size, promo lift, return rate) for agent reasoning and reporting.

Healthcare example:

- Prioritize use cases such as care pathway analytics, clinical operations support, and quality-measure reporting.
- Integrate EHR/claims/operational events through governed pipelines with strict access boundaries.
- Add compliance controls for PHI handling, auditability, and role-based access workflows.

Implementation suggestion:

- Create a domain configuration module (for example, `settings_retail.py` or `settings_healthcare.py`) that selects data sources, KPIs, and policy constraints per deployment environment.

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
- Real-time operational metrics from AWS CloudWatch and Grafana (Kafka, Flink, Aurora) are ingested into Databricks Lakebase, which serves as the agent knowledge base via `databricks_lakebase_mcp`.
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
| database_admin | Database operations, backup/restore, performance, and governance |
| stream_engineer | Kafka and Flink operations, consumer lag, checkpointing, and incident response |

Operational activities now covered by the specialist team include:

- Database health checks and maintenance runbooks.
- Backup and restore validation workflows.
- Query-performance triage and remediation patterns.
- Incident-response checklists for database reliability events.
- Kafka topic, consumer group, and broker operational runbooks.
- Flink job lifecycle management, savepoint/restore procedures, and backpressure triage.

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
├── Makefile
├── README.md
├── pyproject.toml
├── uv.lock
├── src/
│   └── ai_app/
│       ├── __init__.py
│       ├── main.py
│       ├── runtime_factory.py
│       ├── settings.py
│       ├── orchestration.py
│       ├── supervisor.py
│       ├── supervisor_langgraph.py
│       ├── integrations/
│       │   ├── __init__.py
│       │   └── mcp_data_sources.py
│       ├── agents/
│       │   ├── __init__.py
│       │   ├── base.py
│       │   ├── frontend.py
│       │   ├── backend.py
│       │   ├── ml_engineer.py
│       │   ├── ai_engineer.py
│       │   ├── fullstack.py
│       │   ├── data_engineer.py
│       │   ├── data_scientist.py
│       │   ├── database_admin.py
│       │   ├── stream_engineer.py
│       │   └── registry.py
│       ├── utils/
│       │   ├── __init__.py
│       │   ├── env.py
│       │   ├── memory.py
│       │   └── message_bus.py
│       └── resources/
│           ├── application.json
│           └── log4j.properties
├── docs/
│   ├── adrs/
│   │   ├── README.md
│   │   ├── 0001-supervisor-specialist-orchestration.md
│   │   ├── 0002-mongodb-shared-memory.md
│   │   ├── 0003-rabbitmq-message-bus.md
│   │   ├── 0004-databricks-mcp-gateway-constraints.md
│   │   ├── 0005-pydantic-ai-tool-layer.md
│   │   └── template.md
│   ├── architecture.md
│   └── runbook.md
├── container/
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── README.md
├── scripts/
│   └── databricks_deploy.sh
├── .github/workflows/
│   └── databricks-cicd.yml
```
