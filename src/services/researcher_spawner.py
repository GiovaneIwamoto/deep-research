"""
Researcher spawner services for the Deep Research Agent project.
"""

import logging
from models.base import ReportState
from config.system_config import Configuration
from langchain_core.runnables import RunnableConfig
from typing import List
from langgraph.types import Send


def spawn_researchers(state: ReportState, config: RunnableConfig) -> List[Send]:
    """
    Spawn parallel researcher agents for each search query.
    """
    logging.info("Spawning parallel researcher agents.\n")
    return [Send("search_and_summarize", {"query": query, "current_date": state.current_date}) for query in state.search_queries] 