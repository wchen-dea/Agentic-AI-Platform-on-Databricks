"""Specialist agent classes and registry exports."""

from .base import BaseSpecialistAgent, AgentResult
from .ai_frontend_engineer import AIFrontendEngineerAgent
from .ai_backend_engineer import AIBackendEngineerAgent
from .ai_machine_learning_engineer import AIMachineLearningEngineerAgent
from .ai_engineer import AIEngineerAgent
from .ai_fullstack_engineer import AIFullStackEngineerAgent
from .ai_data_engineer import AIDataEngineerAgent
from .ai_data_scientist import AIDataScientistAgent
from .ai_database_admin import AIDatabaseAdminAgent, AIDBAAgent
from .ai_stream_engineer import AIStreamEngineerAgent
from .registry import SpecialistSpec, SPECIALIST_CATALOG, SPECIALIST_NAMES, SPECIALIST_REGISTRY

# Backward-compatible aliases for existing imports.
FrontendAgent = AIFrontendEngineerAgent
BackendAgent = AIBackendEngineerAgent
MLEngineerAgent = AIMachineLearningEngineerAgent
FullStackAgent = AIFullStackEngineerAgent
DataEngineerAgent = AIDataEngineerAgent
DataScientistAgent = AIDataScientistAgent
DatabaseAdminAgent = AIDatabaseAdminAgent
StreamEngineerAgent = AIStreamEngineerAgent

__all__ = [
    "BaseSpecialistAgent",
    "AgentResult",
    "AIFrontendEngineerAgent",
    "AIBackendEngineerAgent",
    "AIMachineLearningEngineerAgent",
    "AIEngineerAgent",
    "AIFullStackEngineerAgent",
    "AIDataEngineerAgent",
    "AIDataScientistAgent",
    "AIDatabaseAdminAgent",
    "AIDBAAgent",
    "AIStreamEngineerAgent",
    "FrontendAgent",
    "BackendAgent",
    "MLEngineerAgent",
    "FullStackAgent",
    "DataEngineerAgent",
    "DataScientistAgent",
    "DatabaseAdminAgent",
    "StreamEngineerAgent",
    "SpecialistSpec",
    "SPECIALIST_CATALOG",
    "SPECIALIST_NAMES",
    "SPECIALIST_REGISTRY",
]
