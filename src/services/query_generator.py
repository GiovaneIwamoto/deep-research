"""
Query generator services for the Deep Research Agent project.
"""

import logging
from typing import List, Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableConfig

from config.system_config import Configuration
from models.base import DeepResearchState, QueryResult
from utils.current_date import get_current_date
from templates.prompt_query_generator import query_generator_prompt

def generate_queries(state: DeepResearchState, config: RunnableConfig) -> Dict[str, Any]:
    """Generate a list of search queries based on the research brief using an LLM."""
    configurable = Configuration.from_runnable_config(config)
    
    class QueryList(QueryResult.__base__):
        queries: List[str]

    # Each query will be dealt with by a single researcher
    num_queries = configurable.research_units_initial

    # Fill prompt placeholders
    prompt = query_generator_prompt.format(
        research_brief=state["research_brief"],
        current_date=get_current_date(),
        num_queries=num_queries)

    # Invoke model
    query_generator_llm = ChatOpenAI(model=configurable.query_generation_model).with_structured_output(QueryList)
    response = query_generator_llm.invoke(prompt)

    logging.info(f"Generated search queries:\n\n{response.queries}\n\n")
    
    return {"search_queries": response.queries} 