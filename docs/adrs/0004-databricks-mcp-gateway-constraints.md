# ADR-0004: Define Databricks MCP Gateway Constraints

- Status: Accepted
- Date: 2026-06-09
- Deciders: Agentic Application maintainers
- Technical Story: N/A

## Context

The project integrates multiple Databricks-backed retrieval sources behind a single gateway (`MCPDataSourceGateway`). Without explicit constraints, source behavior, payload shape, and runtime configuration can drift over time. That drift can lead to fragile integrations and unclear agent expectations.

Databricks Lakebase (`databricks_lakebase_mcp`) serves as the primary real-time operational knowledge base for the platform. AWS CloudWatch collects metrics from Kafka brokers, Flink jobs, and Aurora (RDS) database instances. Grafana ingests these metrics into Lakebase in real-time. Operational specialists (`stream_engineer`, `database_admin`) query Lakebase via `mcp_retrieve` to ground their analysis in current infrastructure state; these map to AI Stream Engineer and AI Database Admin roles.

## Decision

Constrain Databricks MCP integration to a read-oriented, source-typed gateway contract:

- `MCPDataSourceGateway.from_env(...)` requires `DATABRICKS_MCP_URL` and supports optional `DATABRICKS_TOKEN`.
- Source selection is explicit via `DataSourceType`:
  - `databricks_uc` — Unity Catalog general knowledge retrieval.
  - `databricks_feature_store` — Feature Store retrieval (restricted to `ml_engineer`, AI Machine Learning Engineer).
  - `databricks_lakebase_mcp` — Primary real-time operational knowledge base fed by CloudWatch and Grafana metrics for Kafka, Flink, and Aurora.
- Tool names are configurable by environment and default to:
  - `unity_catalog_search`
  - `feature_store_search`
  - `lakebase_search`
- Retrieval requests are normalized to include catalog/schema/query/top_k plus source-specific table and column fields.
- Response parsing supports `documents`, nested `result.documents`, and fallback `rows` extraction.
- Gateway scope is retrieval only; index generation and data writes remain external pipeline responsibilities.

## Consequences

- Agents interact through one stable retrieval API (`gateway.retrieve(...)`).
- Environment-driven configuration improves deployment flexibility without code changes.
- Clear source boundaries reduce accidental cross-source behavior.
- Additional response-shape handling increases adapter complexity, but it also improves runtime resilience.
- `LAKEBASE_METRICS_TABLE` enables the real-time operational metrics table to be configured independently from the general Lakebase knowledge-base table.

## Alternatives Considered

- Separate gateway per source type: Simpler per adapter, but duplicates orchestration logic.
- Hard-code MCP tool names and payload schema: Lower flexibility across environments.
- Allow write/index operations in gateway: Increases coupling and operational risk in runtime path.
