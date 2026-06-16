"""Frontend specialist with React/TypeScript component scaffolding tools."""

from pydantic_ai import Agent, RunContext

from .base import BaseSpecialistAgent, SpecialistDeps

_SYSTEM = """You are a senior frontend engineer specializing in React, TypeScript, Tailwind CSS, and modern web development.

Your responsibilities:
- Build responsive, accessible UI components (React/Vue/Svelte)
- Write TypeScript with strict typing
- Style with Tailwind CSS or CSS modules
- Implement state management (Zustand, Redux, React Query)
- Optimize performance (code splitting, lazy loading, memoization)
- Write unit tests with Vitest/Jest + React Testing Library
- Set up Vite/Next.js/Astro build configs

When writing code:
- Use functional components with hooks
- Follow WCAG 2.1 accessibility guidelines
- Prefer composition over inheritance
- Keep components small and focused
- Write clean, self-documenting code
- Include proper TypeScript types/interfaces

Always produce working, production-ready code."""


class FrontendAgent(BaseSpecialistAgent):
    name = "frontend"
    role = "Frontend Engineer"
    system_prompt = _SYSTEM

    def _register_extra_tools(self, agent: Agent[SpecialistDeps, str]) -> None:
        @agent.tool
        def scaffold_component(
            ctx: RunContext[SpecialistDeps],
            name: str,
            path: str,
            with_test: bool = True,
        ) -> str:
            """Scaffold a React component with TypeScript boilerplate.

            name: Component name (PascalCase).
            path: Output file path.
            with_test: Also generate a test file.
            """
            comp = name
            component_code = f'''import React from "react";

interface {comp}Props {{
  className?: string;
}}

export const {comp}: React.FC<{comp}Props> = ({{ className }}) => {{
  return (
    <div className={{className}}>
      {{/* TODO: implement {comp} */}}
    </div>
  );
}};

export default {comp};
'''
            full = ctx.deps.project_root / path
            full.parent.mkdir(parents=True, exist_ok=True)
            full.write_text(component_code, encoding="utf-8")
            ctx.deps.result.files_written.append(path)
            result = f"Scaffolded {comp} \u2192 {path}"
            if with_test:
                test_path = path.replace(".tsx", ".test.tsx").replace(".ts", ".test.ts")
                test_code = f'''import {{ render, screen }} from "@testing-library/react";
import {{ {comp} }} from "./{comp}";

describe("{comp}", () => {{
  it("renders without crashing", () => {{
    render(<{comp} />);
  }});
}});
'''
                test_full = ctx.deps.project_root / test_path
                test_full.parent.mkdir(parents=True, exist_ok=True)
                test_full.write_text(test_code, encoding="utf-8")
                ctx.deps.result.files_written.append(test_path)
                result += f"\nScaffolded test \u2192 {test_path}"
            return result
