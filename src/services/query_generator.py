"""
Query generator services for the Deep Research Agent project.
"""

import logging
from models.base import QueryResult, ReportState
from templates.prompt_query_generator import query_generator_prompt
from config.system_config import Configuration
from langchain_core.runnables import RunnableConfig
from typing import List, Dict, Any
from langchain_openai import ChatOpenAI


def generate_queries(state: ReportState, config: RunnableConfig) -> Dict[str, Any]:
    """
    Generate a list of search queries based on the user's input using an LLM.
    """
    class QueryList(QueryResult.__base__):
        queries: List[str]

    # Use configuration from RunnableConfig
    configurable = Configuration.from_runnable_config(config)
    model_name = configurable.query_generation_model

    # Number of queries to generate for initial search, each query will be dealt with by a single researcher
    num_queries = configurable.research_units_initial

    # Fill prompt placeholders with state data
    prompt = query_generator_prompt.format(
        user_input=state.user_input, 
        current_date=state.current_date, 
        num_queries=num_queries)

    # Define the query generation model
    query_llm = ChatOpenAI(model=model_name).with_structured_output(QueryList)
    result = query_llm.invoke(prompt)

    logging.info(f"Generated search queries:\n\n{result.queries}\n\n")
    
    return {"search_queries": result.queries} 