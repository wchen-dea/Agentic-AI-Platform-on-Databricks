"""Specialist agent classes and registry exports."""

from .base import BaseSpecialistAgent, AgentResult
from .frontend import FrontendAgent
from .backend import BackendAgent
from .ml_engineer import MLEngineerAgent
from .ai_engineer import AIEngineerAgent
from .fullstack import FullStackAgent
from .data_engineer import DataEngineerAgent
from .data_scientist import DataScientistAgent
from .database_admin import DatabaseAdminAgent
from .stream_engineer import StreamEngineerAgent
from .registry import SpecialistSpec, SPECIALIST_CATALOG, SPECIALIST_NAMES, SPECIALIST_REGISTRY

__all__ = [
    "BaseSpecialistAgent",
    "AgentResult",
    "FrontendAgent",
    "BackendAgent",
    "MLEngineerAgent",
    "AIEngineerAgent",
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
