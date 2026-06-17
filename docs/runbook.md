# Runbook

## Purpose

This runbook covers day-to-day operation of Agentic Application, including local execution, validation, packaging, and Databricks CI/CD rollout.

Operational framing: this platform is run as a modern data domain management system where specialist agents own role-specific responsibilities and coordinate via supervisor-controlled handoffs.

It is architecture-aligned to the implemented runtime path:

- `src/ai_app/runtime_factory.py`: assembly of Anthropic client, memory backend, message bus, and supervisor implementation.
- `src/ai_app/supervisor.py` / `src/ai_app/supervisor_langgraph.py`: orchestration control plane.
- `src/ai_app/utils/memory.py` / `src/ai_app/utils/message_bus.py`: collaboration plane backends.
- `src/ai_app/integrations/mcp_data_sources.py`: Databricks MCP retrieval gateway.

For architectural rationale and trade-offs, see [ADRs](adrs/README.md).

## Local Setup

```bash
uv sync
cp .env.example .env
```

Required local environment variables:

- ANTHROPIC_API_KEY

Optional shared-memory backend variable:

- MONGODB_URI (for example: mongodb://localhost:27017)

Optional message bus variable:

- RABBITMQ_URL (default: amqp://guest:guest@localhost:5672/)

Optional RabbitMQ credentials (used in docker-compose defaults):

- RABBITMQ_USER (default: guest)
- RABBITMQ_PASS (default: guest)

Optional MongoDB memory configuration:

- MONGODB_DB (default: agentic_app)
- MONGODB_MEMORY_COLLECTION (default: shared_memory)

Optional runtime wiring configuration:

- AI_APP_IMPLEMENTATION (classic or langgraph, default: classic)
- SUPERVISOR_MAX_WORKERS (default: 4)
- ANTHROPIC_MODEL (default: claude-opus-4-7)
- ANTHROPIC_MAX_TOKENS (default: 8096)
- SUPERVISOR_MAX_ITERATIONS (default: 40)

Optional runtime variables for MCP data retrieval:

- DATABRICKS_MCP_URL
- DATABRICKS_TOKEN
- DATABRICKS_MCP_UC_TOOL
- DATABRICKS_MCP_FEATURE_STORE_TOOL
- DATABRICKS_MCP_LAKEBASE_TOOL
- UC_CATALOG
- UC_SCHEMA
- UC_KB_TABLE
- UC_FEATURE_TABLE
- UC_FEATURE_TEXT_COLUMN
- UC_FEATURE_SCORE_COLUMN
- LAKEBASE_TABLE
- LAKEBASE_METRICS_TABLE (real-time operational metrics table in Lakebase; falls back to LAKEBASE_TABLE)

## Specialist Coverage

Current specialist roster includes: `frontend`, `backend`, `ml_engineer`, `ai_engineer`, `fullstack`, `data_engineer`, `data_scientist`, `database_admin`, and `stream_engineer`.

Domain operations intent:

- `data_engineer`, `data_scientist`, and `ml_engineer` cover domain data product development and model outcomes.
- `database_admin` and `stream_engineer` cover operational reliability for domain-serving data infrastructure.
- `backend`, `frontend`, and `fullstack` cover delivery surfaces that expose domain intelligence to users and systems.

Use `database_admin` for operational DBA workflows such as backup/restore validation, health-check automation, performance triage, and incident runbook generation.

Use `stream_engineer` for Kafka and Flink operational workflows such as consumer-lag investigation, topic management, Flink job lifecycle (savepoint, restore, upgrade), backpressure triage, and streaming infrastructure health checks.

## Observability Pipeline

AWS CloudWatch collects metrics from Kafka brokers/topics, Flink jobs/checkpoints, and Aurora database instances. Grafana ingests these metrics into Databricks Lakebase in real-time.

Agents retrieve operational context from Lakebase via `mcp_retrieve` with `source_type='databricks_lakebase_mcp'`. Set `LAKEBASE_METRICS_TABLE` to the table that holds the real-time metrics (defaults to `LAKEBASE_TABLE`).

## Common Commands

```bash
# run a task
uv run multi-ai-agent --task "build a RAG chatbot"

# domain-oriented examples
uv run multi-ai-agent --task "design domain ownership metrics and data quality checks for order-to-cash"
uv run multi-ai-agent --task "triage streaming lag and propose domain incident remediation steps"

# include memory and message logs
uv run multi-ai-agent --task "build a churn model" --show-memory --show-messages

# reset state before run
uv run multi-ai-agent --task "redesign recommendation engine" --reset-memory
```

Make targets:

```bash
make sync
make init-env
make run TASK="build a user authentication system"
make run-quiet TASK="build a data pipeline"
make run-reset TASK="redesign the recommendation engine"
make run-container
make stop-container
make clean-container
make build-wheel
make clean
```

Containerized run with MongoDB and RabbitMQ:

```bash
docker compose -f container/docker-compose.yml up --build
```

RabbitMQ management UI: <http://localhost:15672> (guest/guest by default).

## Validation Checklist

```bash
uv run python -m compileall src
uv run multi-ai-agent --help
make build-wheel
```

Expected artifact:

- `dist/agentic_app-<version>-py3-none-any.whl`

## CI/CD Workflow

Pipeline:

- `.github/workflows/databricks-cicd.yml`

Deploy helper:

- `scripts/databricks_deploy.sh`

Stages:

1. Build and validate wheel on Python 3.13.
2. Upload wheel artifact from dist/.
3. Deploy to staging Databricks App.
4. Optional production deploy via workflow_dispatch input deploy_prod=true.

## GitHub Environment Secrets

Required secrets in staging and production environments:

- DATABRICKS_HOST
- DATABRICKS_TOKEN
- DATABRICKS_APP_NAME
- DATABRICKS_VOLUME_PATH
- RUNTIME_ENV_B64

RUNTIME_ENV_B64 generation:

```bash
cat .env.runtime | base64
```

DATABRICKS_VOLUME_PATH format:

```text
<catalog>/<schema>/<volume>
```

## Deployment and Rollout Behavior

`scripts/databricks_deploy.sh` performs:

1. Validation of required Databricks variables.
2. Upload of wheel artifact to:
   `dbfs:/Volumes/<catalog>/<schema>/<volume>/releases/<commit_sha>/`
3. Databricks App deploy from generated bundle at .databricks/app_bundle.
4. App start and status retrieval for rollout visibility.

## Troubleshooting

- Build fails on compileall:
  - Run uv sync --frozen and re-run compile checks.
- Wheel missing in dist:
  - Run uv build --wheel and check pyproject metadata.
- Databricks deploy command fails:
  - Verify databricks CLI version and workspace app support.
  - Validate DATABRICKS_HOST, DATABRICKS_TOKEN, and DATABRICKS_APP_NAME.
- Runtime config not applied:
  - Recreate RUNTIME_ENV_B64 from the correct .env.runtime content.

## Operational Notes

- Runtime dependencies are assembled by `src/ai_app/runtime_factory.py`, which builds the Anthropic client, memory backend, message bus, and selected supervisor implementation from environment + CLI overrides.
- Shared memory uses MongoDB when available (`MONGODB_URI`/`MONGODB_DB`/`MONGODB_MEMORY_COLLECTION`) and degrades to an in-memory store if MongoDB is unavailable.
- Inter-agent messages use RabbitMQ topic exchange (`agent_messages`) with durable inbox queues (`agent_inbox.<name>`) when RabbitMQ is available, and degrade to an in-memory bus if RabbitMQ is unavailable.
- Use --reset-memory for clean reruns to avoid stale coordination context.
- For production rollout, require manual workflow dispatch with deploy_prod=true.
