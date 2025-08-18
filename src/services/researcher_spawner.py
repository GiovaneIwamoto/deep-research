"""
Researcher spawner services for the Deep Research Agent project.
"""

import logging
from typing import List
from langgraph.types import Send
from models.base import DeepResearchState
from utils.current_date import get_current_date

def spawn_researchers(state: DeepResearchState) -> List[Send]:
    """
    Spawn parallel researcher agents for each search query.
    """
    logging.info("Spawning parallel researcher agents.\n")
    return [Send("search_and_summarize", {"query": query, "current_date": get_current_date()}) for query in state["search_queries"]] 