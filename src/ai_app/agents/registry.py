"""Specialist catalog and registry helpers."""

from __future__ import annotations

from dataclasses import dataclass

from .ai_engineer import AIEngineerAgent
from .ai_backend_engineer import AIBackendEngineerAgent
from .ai_data_engineer import AIDataEngineerAgent
from .ai_data_scientist import AIDataScientistAgent
from .ai_database_admin import AIDatabaseAdminAgent
from .ai_frontend_engineer import AIFrontendEngineerAgent
from .ai_stream_engineer import AIStreamEngineerAgent
from .ai_fullstack_engineer import AIFullStackEngineerAgent
from .ai_machine_learning_engineer import AIMachineLearningEngineerAgent


@dataclass(frozen=True)
class SpecialistSpec:
    key: str
    role: str
    description: str
    agent_cls: type


SPECIALIST_CATALOG: tuple[SpecialistSpec, ...] = (
    SpecialistSpec(
        key="frontend",
        role="AI Frontend Engineer",
        description="React, TypeScript, Tailwind, a11y, state management.",
        agent_cls=AIFrontendEngineerAgent,
    ),
    SpecialistSpec(
        key="backend",
        role="AI Backend Engineer",
        description="FastAPI, databases, auth, REST APIs, Python services.",
        agent_cls=AIBackendEngineerAgent,
    ),
    SpecialistSpec(
        key="ml_engineer",
        role="AI Machine Learning Engineer",
        description="PyTorch, scikit-learn, training pipelines, MLOps.",
        agent_cls=AIMachineLearningEngineerAgent,
    ),
    SpecialistSpec(
        key="ai_engineer",
        role="AI Engineer",
        description="LLM apps, RAG, Claude tool use, prompt engineering.",
        agent_cls=AIEngineerAgent,
    ),
    SpecialistSpec(
        key="fullstack",
        role="AI Full-Stack Engineer",
        description="End-to-end features, Next.js, Docker, CI/CD.",
        agent_cls=AIFullStackEngineerAgent,
    ),
    SpecialistSpec(
        key="data_engineer",
        role="AI Data Engineer",
        description="ETL/ELT, Airflow, dbt, Spark, streaming, SQL.",
        agent_cls=AIDataEngineerAgent,
    ),
    SpecialistSpec(
        key="data_scientist",
        role="AI Data Scientist",
        description="EDA, statistics, A/B tests, forecasting.",
        agent_cls=AIDataScientistAgent,
    ),
    SpecialistSpec(
        key="database_admin",
        role="AI Database Admin",
        description="DB operations, backup/restore, performance tuning, incident response.",
        agent_cls=AIDatabaseAdminAgent,
    ),
    SpecialistSpec(
        key="stream_engineer",
        role="AI Stream Engineer",
        description="Kafka and Flink operations, consumer lag, checkpointing, incident response.",
        agent_cls=AIStreamEngineerAgent,
    ),
)

SPECIALIST_REGISTRY = {spec.key: spec.agent_cls for spec in SPECIALIST_CATALOG}
SPECIALIST_NAMES = tuple(spec.key for spec in SPECIALIST_CATALOG)
