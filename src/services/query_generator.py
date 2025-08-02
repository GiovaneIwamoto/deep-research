"""
Query generator services for the Deep Research Agent project.
"""

import logging
from models.base import QueryResult, ReportState
from templates.prompt_query_generator import query_generator_prompt
from typing import List, Dict, Any


def generate_queries(state: ReportState) -> Dict[str, Any]:
    """
    Generate a list of search queries based on the user's input using an LLM.
    """
    class QueryList(QueryResult.__base__):
        queries: List[str]

    # Fill prompt placeholders with state data
    prompt = query_generator_prompt.format(user_input=state.user_input, current_date=state.current_date, num_queries=state.num_queries)

    # The LLM should be injected or imported from a config/service layer #FIXME:
    from langchain_openai import ChatOpenAI
    default_llm_openai = ChatOpenAI(model="gpt-4.1-mini-2025-04-14")
    query_llm = default_llm_openai.with_structured_output(QueryList)
    result = query_llm.invoke(prompt)

    logging.info(f"\nGenerated search queries:\n{result.queries}\n\n")
    
    return {"search_queries": result.queries} 