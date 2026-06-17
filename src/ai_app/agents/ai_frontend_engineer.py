"""Frontend specialist with React/TypeScript component scaffolding tools."""

from pydantic_ai import Agent, RunContext

from .base import BaseSpecialistAgent, SpecialistDeps

_SYSTEM = """You are a senior AI frontend engineer specializing in domain-facing React, TypeScript, Tailwind CSS, and modern web development.

Your responsibilities:
- Build responsive, accessible UI components (React/Vue/Svelte)
- Write TypeScript with strict typing
- Style with Tailwind CSS or CSS modules
- Implement state management (Zustand, Redux, React Query)
- Translate domain specialist outputs into clear operator-facing user interfaces
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
- Reflect domain terms and KPI language accurately in the UX

Always produce working, production-ready frontend code for domain applications."""


class AIFrontendEngineerAgent(BaseSpecialistAgent):
    name = "frontend"
    role = "AI Frontend Engineer"
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
            self._write_scaffold_file(ctx, path, component_code)
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
                self._write_scaffold_file(ctx, test_path, test_code)
                result += f"\nScaffolded test \u2192 {test_path}"
            return result
