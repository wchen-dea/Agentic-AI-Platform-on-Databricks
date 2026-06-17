# ADR-0006: Adopt Layered, Governed Prompt Engineering Design

- Status: Accepted
- Date: 2026-06-17
- Deciders: Agentic Application maintainers
- Technical Story: N/A

## Context

Prompt behavior is a first-order reliability factor in this multi-agent system. A single monolithic prompt is not sufficient for this architecture because:

- Supervisor planning and specialist execution have different objectives.
- Operational tasks require grounding in trusted enterprise data, not model priors alone.
- Multi-agent collaboration requires explicit context-sharing and handoff discipline.
- Tool use must be constrained by typed contracts and policy checks.

The project principle is that model capability is not the unique advantage. Durable value is created when model selection and prompt behavior are coupled with trusted data and governed execution.

## Decision

Adopt a layered prompt engineering design with explicit governance boundaries:

- Supervisor prompt layer:
  - Keep orchestration policy in the supervisor system prompt (`orchestration.py`) for decomposition, routing, peer review, and revision loops.
  - Encode cross-specialist quality gates and decision logging requirements in shared supervisor instructions.
- Specialist prompt layer:
  - Keep role-specific domain instructions in each specialist module (`agents/ai_*.py`).
  - Define specialist responsibilities, output standards, and domain constraints at this layer.
- Shared collaboration prompt layer:
  - Append consistent collaboration directives in `BaseSpecialistAgent` (memory usage, message bus usage, inbox-first behavior, artifact persistence).
  - Ensure all specialists inherit the same collaboration baseline.
- Typed tool and policy layer:
  - Expose tool usage through Pydantic AI typed tools (`@agent.tool`) rather than free-form instructions.
  - Keep MCP retrieval, memory, and messaging under typed inputs and centralized policy checks.
- Data-grounding layer:
  - Require MCP retrieval for operational analysis paths, especially Lakebase-backed tasks for Kafka/Flink/Aurora operations.
  - Treat retrieval evidence as part of prompt context, not optional add-on text.

## Consequences

- Improves consistency between planning, delegation, and specialist execution.
- Reduces prompt drift by separating prompt responsibilities into stable layers.
- Increases auditability because decisions and artifacts are persisted through memory/message tools.
- Strengthens trustworthiness by coupling prompt behavior with governed data retrieval.
- Introduces additional design overhead when adding new specialists because role prompts must align with shared collaboration and tool policies.

## Alternatives Considered

- Single global prompt for all agents:
  - Simpler authoring but weak role separation and poor scalability for specialist evolution.
- Unstructured per-agent prompts with ad-hoc tool guidance:
  - Faster iteration initially but high drift risk and weak policy consistency.
- Tool-only control without explicit prompt layering:
  - Better constraints than free-form prompting, but weaker planning and collaboration behavior without supervisor/specialist prompt contracts.
