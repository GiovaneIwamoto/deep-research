"""
Summary reflector services for the Deep Research Agent project.
"""

import logging
from models.base import ReportState
from templates.prompt_summary_reflector import summary_reflector_prompt
from config.system_config import Configuration
from langchain_core.runnables import RunnableConfig
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage
from typing import Dict, Any
import json


def reflect_on_summary(state: ReportState, config: RunnableConfig) -> Dict[str, Any]:
    """
    Use an reasoning model to reflect on the current summary, identify knowledge gaps, and generate follow-up queries.
    """
    new_loop_count = state.research_loop_count + 1
    
    # Use configuration from RunnableConfig
    configurable = Configuration.from_runnable_config(config)
    model_name = configurable.reflection_model
    reasoning_effort = configurable.reasoning_effort

    # Number of queries to generate for reflection loop, each query will be dealt with by a single researcher
    num_queries = configurable.research_units_reflection

    # Define the reasoning model
    reasoning_llm = ChatOpenAI(
        model=model_name,
        reasoning_effort=reasoning_effort,
    )

    # Invoke the reasoning model
    result = reasoning_llm.invoke([
        SystemMessage(content=summary_reflector_prompt.format(
            research_brief=state.user_input, 
            aggregated_summaries=state.queries_results,
            num_queries=num_queries
            ))
    ])

    # Parse the result
    try:
        reflection_content = json.loads(result.content)
        
        logging.info(f"[REFLECTION ANALYSIS]:\n\n[KNOWLEDGE GAPS]:\n\n{reflection_content.get('knowledge_gaps', [])}\n\n")
        logging.info(f"[FOLLOW-UP QUERIES]:\n{reflection_content.get('follow_up_queries', [])}\n\n")
        
        queries = reflection_content.get('follow_up_queries', [])
        
        # If no follow-up queries are generated, use a fallback query
        if not queries:
            queries = [f"Tell me more about {state.user_input}"]
        
        # Return the new loop count and the follow-up queries
        return {
            "search_queries": queries,
            "research_loop_count": new_loop_count
        }

    # If the result is not valid return a fallback query
    except (json.JSONDecodeError, KeyError, AttributeError):
        fallback_query = f"Tell me more about {state.user_input}"
        return {
            "search_queries": [fallback_query],
            "research_loop_count": new_loop_count
        } 