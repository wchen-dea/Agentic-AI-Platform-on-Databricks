"""Stream engineering specialist for Flink and Kafka operational support."""

from pydantic_ai import Agent, RunContext

from .base import BaseSpecialistAgent, SpecialistDeps

_SYSTEM = """You are a senior stream engineer specializing in operational support for Apache Flink and Apache Kafka infrastructure in domain management platforms.

Your responsibilities:
- Operate and maintain Kafka clusters (brokers, topics, partitions, consumer groups, ACLs)
- Operate and maintain Flink deployments (JobManager, TaskManager, checkpointing, savepoints)
- Design and troubleshoot streaming pipelines end-to-end
- Monitor consumer lag, backpressure, throughput, and latency KPIs
- Perform topic management: creation, retention policies, replication, and compaction
- Handle Flink job lifecycle: submit, cancel, savepoint, restore, and upgrade
- Diagnose and remediate common failure modes: message loss, duplicate delivery, checkpoint failures, partition imbalance
- Implement schema registry integration and schema evolution strategies
- Tune producer/consumer configurations for throughput and reliability
- Write operational runbooks, alerting rules, and capacity planning notes
- Preserve reliable domain event flow and handoff guarantees for downstream specialists

Operational metrics context:
Kafka and Flink infrastructure metrics are collected by AWS CloudWatch and Grafana
and ingested into Databricks Lakebase in real-time. Before producing runbooks,
incident responses, or capacity recommendations, call mcp_retrieve with
source_type='databricks_lakebase_mcp' to retrieve current metric snapshots,
alert history, consumer lag trends, and checkpoint performance data from Lakebase.

When writing code or docs:
- Prefer idempotent, exactly-once semantics where possible
- Include pre-checks and rollback guidance for any change
- Make monitoring queries and CLI commands copy-paste ready
- Document operational impact and risk for each procedure
- Connect incident recommendations to domain KPI degradation risk

Always produce practical, operationally safe stream engineering artifacts for domain operations."""


class StreamEngineerAgent(BaseSpecialistAgent):
    name = "stream_engineer"
    role = "Stream Engineer"
    system_prompt = _SYSTEM

    def _register_extra_tools(self, agent: Agent[SpecialistDeps, str]) -> None:

        @agent.tool
        def scaffold_kafka_ops_runbook(
            ctx: RunContext[SpecialistDeps],
            cluster_name: str,
            path: str,
        ) -> str:
            """Scaffold a Kafka operational runbook for day-to-day cluster management.

            cluster_name: Logical name of the Kafka cluster.
            path: Output markdown file path.
            """
            cluster = cluster_name
            content = f"""# {cluster} Kafka Operational Runbook

## Scope

- Target cluster: `{cluster}`
- Owner: Stream Engineering
- Objective: Ensure Kafka cluster health, throughput, and consumer-group reliability.

## Daily Health Checks

```bash
# Broker availability
kafka-broker-api-versions.sh --bootstrap-server <broker>:9092

# Under-replicated partitions (should be 0)
kafka-topics.sh --bootstrap-server <broker>:9092 --describe --under-replicated-partitions

# Consumer group lag overview
kafka-consumer-groups.sh --bootstrap-server <broker>:9092 --describe --all-groups
```

## Topic Management

```bash
# Create topic
kafka-topics.sh --bootstrap-server <broker>:9092 --create \\
  --topic <topic> --partitions 12 --replication-factor 3 \\
  --config retention.ms=604800000

# List topics
kafka-topics.sh --bootstrap-server <broker>:9092 --list

# Alter retention
kafka-configs.sh --bootstrap-server <broker>:9092 --entity-type topics \\
  --entity-name <topic> --alter --add-config retention.ms=86400000
```

## Consumer Group Operations

```bash
# Check lag
kafka-consumer-groups.sh --bootstrap-server <broker>:9092 \\
  --describe --group <group>

# Reset offsets to latest (use with caution)
kafka-consumer-groups.sh --bootstrap-server <broker>:9092 \\
  --group <group> --topic <topic> --reset-offsets --to-latest --execute
```

## Incident Triage

1. Classify: consumer lag spike, broker down, under-replicated partitions, high disk usage.
2. Identify affected topics and consumer groups.
3. Check broker logs and JVM heap metrics.
4. Common mitigations:
   - Lag spike: scale consumer instances or increase partition count.
   - Broker down: trigger controller election or replace node.
   - High disk: reduce retention or compact topic.
5. Record timeline, root cause, and remediation in incident log.

## Capacity Planning

- Monitor partition growth, message rate, and disk usage weekly.
- Trigger expansion when disk utilisation exceeds 70% or throughput reaches 80% of headroom.
- Pre-stage broker nodes before reaching limits.

## On-call Handover

- Clusters with elevated lag or under-replicated partitions
- Any in-progress partition rebalances
- Pending schema or topic changes
- Escalation contacts
"""
            self._write_scaffold_file(ctx, path, content)
            return f"Scaffolded Kafka ops runbook ({cluster}) \u2192 {path}"

        @agent.tool
        def scaffold_flink_ops_runbook(
            ctx: RunContext[SpecialistDeps],
            app_name: str,
            path: str,
        ) -> str:
            """Scaffold a Flink operational runbook for job lifecycle and incident management.

            app_name: Logical Flink application name.
            path: Output markdown file path.
            """
            app = app_name
            content = f"""# {app} Flink Operational Runbook

## Scope

- Application: `{app}`
- Owner: Stream Engineering
- Objective: Maintain Flink job availability, checkpoint health, and end-to-end latency SLOs.

## Job Lifecycle Commands

```bash
# Submit job
flink run -d -p <parallelism> -c <MainClass> <jar>

# List running jobs
flink list -r

# Trigger savepoint
flink savepoint <job-id> <savepoint-dir>

# Cancel job with savepoint
flink cancel -s <savepoint-dir> <job-id>

# Restore from savepoint
flink run -s <savepoint-path> -d -p <parallelism> -c <MainClass> <jar>
```

## Checkpoint Monitoring

- Target checkpoint interval: set per SLO
- Alert when checkpoint duration > 2× interval
- Alert when failed checkpoints > 3 in 10 minutes

```bash
# Via Flink REST API
curl http://<jobmanager>:8081/jobs/<job-id>/checkpoints | jq .
```

## Backpressure Diagnosis

1. Open Flink UI → job graph → identify red/orange operators.
2. Profile slow operator: check thread dump, GC pauses, external call latency.
3. Common fixes:
   - Increase parallelism for bottleneck operator.
   - Add async I/O for external lookups.
   - Tune buffer timeout and network buffers.

## Upgrade Procedure

1. Trigger savepoint on current job version.
2. Cancel job (verify savepoint completed).
3. Deploy new jar.
4. Restore from savepoint with updated parallelism if required.
5. Validate metrics: throughput, lag, checkpoint completion rate.
6. Keep savepoint for 48 h before deleting.

## Incident Triage

1. Classify: job failed, checkpoint timeout, backpressure, restarts loop.
2. Capture job exceptions from Flink UI or logs.
3. Restore from last successful savepoint if state is consistent.
4. Escalate to on-call if cluster-level issue (TaskManager crashes, network partition).

## Observability KPIs

- Checkpoint duration and failure rate
- Operator backpressure ratio
- End-to-end event latency (source watermark lag)
- Records-in / records-out per operator
- JVM heap and GC pause duration

## On-call Handover

- Jobs currently in restart loop or degraded state
- Pending upgrades or savepoints
- Cluster resource utilisation
- Escalation contacts
"""
            self._write_scaffold_file(ctx, path, content)
            return f"Scaffolded Flink ops runbook ({app}) \u2192 {path}"

        @agent.tool
        def scaffold_stream_healthcheck_script(
            ctx: RunContext[SpecialistDeps],
            system_name: str,
            path: str,
        ) -> str:
            """Scaffold a streaming infrastructure health-check Python script.

            system_name: Logical name of the streaming system.
            path: Output Python file path.
            """
            name = system_name
            content = f'''"""Streaming infrastructure health check scaffold for {name}."""

from __future__ import annotations

import json
import time
from dataclasses import dataclass


@dataclass
class CheckResult:
    name: str
    ok: bool
    details: str


def check_kafka_connectivity() -> CheckResult:
    # TODO: connect to Kafka bootstrap servers and verify metadata response.
    return CheckResult(name="kafka_connectivity", ok=True, details="brokers reachable")


def check_consumer_lag() -> CheckResult:
    # TODO: query consumer group lag via AdminClient and compare to threshold.
    return CheckResult(name="consumer_lag", ok=True, details="lag within threshold")


def check_flink_jobs() -> CheckResult:
    # TODO: call Flink REST API /jobs/overview and verify no jobs in FAILED state.
    return CheckResult(name="flink_jobs", ok=True, details="all jobs running")


def check_checkpoint_health() -> CheckResult:
    # TODO: call Flink REST API and verify recent checkpoint completed successfully.
    return CheckResult(name="checkpoint_health", ok=True, details="checkpoints healthy")


def main() -> int:
    started = time.time()
    checks = [
        check_kafka_connectivity(),
        check_consumer_lag(),
        check_flink_jobs(),
        check_checkpoint_health(),
    ]
    status = {{
        "system": "{name}",
        "ok": all(c.ok for c in checks),
        "duration_ms": int((time.time() - started) * 1000),
        "checks": [c.__dict__ for c in checks],
    }}
    print(json.dumps(status, indent=2))
    return 0 if status["ok"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
'''
            self._write_scaffold_file(ctx, path, content)
            return f"Scaffolded stream health check script ({name}) \u2192 {path}"
