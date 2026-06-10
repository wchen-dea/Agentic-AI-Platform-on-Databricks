# ADR-0005: Use Pydantic AI for Tool Registration, Typed Deps, and Structured Output

- Status: Accepted
- Date: 2026-06-09
- Deciders: Agentic Application maintainers

## Context

`BaseSpecialistAgent` accumulated ~200 lines of hand-written JSON schema dictionaries (`extra_tools = [...]`) and manual `_dispatch_tool` if/elif chains across every specialist. This created:

- Brittle, unvalidated tool contracts that could silently drift from their Python implementations.
- No IDE support or type safety on tool inputs.
- Verbose boilerplate with no shared enforcement for side-effect tracking (files written, memory keys, messages sent).

## Decision

Adopt Pydantic AI as the tool and output layer for `BaseSpecialistAgent`:

- Use `pydantic_ai.Agent[SpecialistDeps, str]` as the per-specialist agent handle.
- Register tools with `@agent.tool` decorators; schemas are auto-generated from Python type hints and docstrings.
- Inject runtime dependencies (memory, message bus, project root, result accumulator) through `RunContext[SpecialistDeps]`.
- Replace the `AgentResult` dataclass with a Pydantic `BaseModel` for validated structured output.
- Centralize ML engineer MCP restriction via `ctx.deps.agent_name` check in the shared `mcp_retrieve` tool rather than per-subclass overrides.

The supervisor orchestration layer (`SupervisorAgent`, peer review loop, parallel dispatch) is unchanged.

## Consequences

- Eliminates ~200 lines of JSON schema boilerplate; tool contracts stay in sync with Python signatures.
- Tool inputs are validated by Pydantic before execution; type errors surface at the call site.
- `AgentResult` fields are validated on construction; invalid state is not possible.
- Side-effect tracking (files written, memory keys, messages sent) is handled uniformly in tool closures via `ctx.deps.result`.
- `pydantic-ai[anthropic]` becomes a direct dependency, replacing the bare `anthropic` package.

## Alternatives Considered

- Keep hand-written JSON schemas: Lowest external dependencies but highest maintenance burden and no type safety.
- Use function calling abstraction from LangChain: Adds a heavier framework dependency incompatible with the project's direct Anthropic SDK usage.
