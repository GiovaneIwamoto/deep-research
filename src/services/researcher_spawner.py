"""
Researcher spawner services for the Deep Research Agent project.
"""

from typing import List
from langgraph.types import Send
from models.base import DeepResearchState
from utils.current_date import get_current_date
from utils.logger_formatter import logging_researcher_spawner


def spawn_researchers(state: DeepResearchState) -> List[Send]:
    """
    Spawn parallel researcher agents for each search query.
    """
    
    logging_researcher_spawner()
    return [Send("search_and_summarize", {"query": query, "current_date": get_current_date()}) for query in state["search_queries"]] 