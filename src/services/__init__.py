"""
Service layer for the Deep Research Agent project.
Exposes all main service functions for orchestration.
"""

from .query_generation import build_first_queries, spawn_researchers, route_after_single_search
from .search import single_search
from .final_writer import final_writer
from .reflection import reflect_on_summary
