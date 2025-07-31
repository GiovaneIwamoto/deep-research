"""
Query generation and agent spawning services for the Deep Research Agent project.
"""

import logging
from models.base import QueryResult, ReportState
from templates.build_queries import build_queries
from typing import List, Dict, Any
from langgraph.types import Send


def build_first_queries(state: ReportState) -> Dict[str, Any]:
    """
    Generate a list of search queries based on the user's input using an LLM.
    """
    class QueryList(QueryResult.__base__):
        queries: List[str]

    # Fill prompt placeholders with state data
    prompt = build_queries.format(user_input=state.user_input, current_date=state.current_date, num_queries=state.num_queries)

    # The LLM should be injected or imported from a config/service layer #FIXME:
    from langchain_openai import ChatOpenAI
    default_llm_openai = ChatOpenAI(model="gpt-4.1-mini-2025-04-14")
    query_llm = default_llm_openai.with_structured_output(QueryList)
    result = query_llm.invoke(prompt)

    logging.info("Generated search queries:")
    logging.info(result)
    logging.info("End of query generation.")
    
    return {"search_queries": result.queries}


def spawn_researchers(state: ReportState) -> List[Send]:
    """
    Spawn parallel researcher agents for each search query.
    """
    logging.info("Spawning parallel researcher agents.")
    return [Send("single_search", query) for query in state.search_queries]


def route_after_single_search(state: ReportState) -> str:
    """
    Decide whether to continue with reflection or proceed to final writing.
    """
    if state.use_reflection and state.research_loop_count < state.reflection_loops:
        return "reflect_on_summary"
    else:
        return "final_writer" 