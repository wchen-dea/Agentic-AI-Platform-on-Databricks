"""Database administration specialist for operational database activities."""

from pydantic_ai import Agent, RunContext

from .base import BaseSpecialistAgent, SpecialistDeps

_SYSTEM = """You are a senior database administrator focused on operational excellence, reliability, and governance.

Your responsibilities:
- Operate relational and analytical databases in production-like environments
- Plan and validate backup/restore and disaster recovery procedures
- Tune query performance and index strategies with measurable impact
- Design maintenance windows and zero/low-downtime operational runbooks
- Monitor health signals (latency, lock contention, replication lag, storage)
- Enforce security and compliance controls for data access and auditing
- Support incident response with clear triage and remediation steps

When writing code or docs:
- Prefer operationally safe defaults
- Include rollback and validation steps for any change
- Make checks scriptable and repeatable
- Keep runbooks actionable with pre-checks and post-checks

Always produce practical, production-ready DBA operations artifacts."""


class DatabaseAdminAgent(BaseSpecialistAgent):
    name = "database_admin"
    role = "Database Administrator"
    system_prompt = _SYSTEM

    def _register_extra_tools(self, agent: Agent[SpecialistDeps, str]) -> None:
        @agent.tool
        def scaffold_db_ops_runbook(
            ctx: RunContext[SpecialistDeps],
            database: str,
            path: str,
        ) -> str:
            """Scaffold a database operations runbook for maintenance and incident handling.

            database: Database/system name.
            path: Output markdown path.
            """
            db = database
            content = f'''# {db} Database Operations Runbook

## Scope

- Target system: `{db}`
- Owner: Database Administration
- Objective: Maintain availability, integrity, and performance for operational workloads.

## Standard Operating Activities

1. Daily health check
2. Weekly performance review
3. Backup verification
4. Access audit and role hygiene
5. Capacity planning update

## Change Procedure

1. Pre-checks
- Confirm replication and backup status are healthy.
- Capture baseline metrics (latency, throughput, lock wait, error rate).
- Announce maintenance window and rollback criteria.

2. Execution
- Apply change incrementally.
- Monitor live KPIs and error logs.
- Pause if SLO thresholds breach.

3. Post-checks
- Run smoke queries and integrity checks.
- Compare post-change metrics to baseline.
- Record change evidence and final status.

## Incident Triage

1. Identify blast radius (tenant, schema, service).
2. Classify issue type: availability, performance, data correctness, security.
3. Execute mitigation playbook:
- Read replica failover
- Query kill / lock relief
- Rollback migration
- Restore from backup (if corruption confirmed)
4. Publish timeline and RCA action items.

## Backup and Recovery Validation

- Backup cadence: define RPO target
- Restore drill cadence: monthly or quarterly
- Recovery checklist:
  - Latest successful backup timestamp
  - Restore completed in isolated environment
  - Data integrity verification passed
  - RTO within target

## Security and Governance Controls

- Principle of least privilege for all roles.
- Privileged access is time-bound and audited.
- Sensitive data access is logged and reviewed.
- Encryption at rest and in transit enabled.

## Observability KPIs

- Query p95/p99 latency
- Error rate
- Lock contention and deadlocks
- Replication lag
- CPU, memory, storage growth

## On-call Handover

- Current incidents/open risks
- Deferred maintenance actions
- Pending schema/data changes
- Contacts and escalation matrix
'''
            self._write_scaffold_file(ctx, path, content)
            return f"Scaffolded DB ops runbook ({db}) -> {path}"

        @agent.tool
        def scaffold_db_healthcheck_script(
            ctx: RunContext[SpecialistDeps],
            system_name: str,
            path: str,
        ) -> str:
            """Scaffold a database health-check Python script template.

            system_name: Logical database system name for reporting.
            path: Output Python file path.
            """
            name = system_name
            content = f'''"""Database health check scaffold for {name}."""

from __future__ import annotations

import json
import time
from dataclasses import dataclass


@dataclass
class CheckResult:
    name: str
    ok: bool
    details: str


def check_connectivity() -> CheckResult:
    # TODO: implement real DB connectivity probe.
    return CheckResult(name="connectivity", ok=True, details="connection successful")


def check_replication_lag() -> CheckResult:
    # TODO: query replication lag metrics and validate threshold.
    return CheckResult(name="replication_lag", ok=True, details="lag within threshold")


def check_lock_contention() -> CheckResult:
    # TODO: inspect active locks/deadlocks and compare to alert thresholds.
    return CheckResult(name="lock_contention", ok=True, details="no critical contention")


def main() -> int:
    started = time.time()
    checks = [
        check_connectivity(),
        check_replication_lag(),
        check_lock_contention(),
    ]
    status = {
        "system": "{name}",
        "ok": all(c.ok for c in checks),
        "duration_ms": int((time.time() - started) * 1000),
        "checks": [c.__dict__ for c in checks],
    }
    print(json.dumps(status, indent=2))
    return 0 if status["ok"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
'''
            self._write_scaffold_file(ctx, path, content)
            return f"Scaffolded DB health check script ({name}) -> {path}"
