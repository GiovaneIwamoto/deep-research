"""
Summary reflector services for the Deep Research Agent project.
"""

import json
from typing import Dict, Any

from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableConfig

from config.system_config import Configuration
from models.base import DeepResearchState
from templates.prompt_summary_reflector import summary_reflector_prompt
from utils.logger_formatter import logging_reflection_analysis


def reflect_on_summary(state: DeepResearchState, config: RunnableConfig) -> Dict[str, Any]:
    """Use an reasoning model to reflect on the current summary, identify knowledge gaps, and generate follow-up queries."""
    configurable = Configuration.from_runnable_config(config)
    
    # Get current loop count and increment it
    current_loop_count = state.get("research_loop_count", 0)
    updated_loop_count = current_loop_count + 1
    
    # Get number of queries
    num_queries = configurable.research_units_reflection

    # Configure reasoning model
    refleciton_reasoning_llm = ChatOpenAI(model=configurable.reflection_model, reasoning_effort=configurable.reasoning_effort)

    # Prompt
    prompt = summary_reflector_prompt.format(
        research_brief=state["research_brief"], 
        aggregated_summaries=state["queries_results"],
        num_queries=num_queries
    )

    # Invoke model
    response = refleciton_reasoning_llm.invoke([SystemMessage(content=prompt)])

    # Parse result
    try:
        # Get reflection content
        reflection_content = json.loads(response.content)
        
        logging_reflection_analysis(reflection_content)
        
        # Get follow-up queries
        queries = reflection_content.get('follow_up_queries', [])
        
        # If no follow-up queries are generated use fallback query
        if not queries: queries = [f"Tell me more about {state['research_brief']}"]
        
        return {"search_queries": queries, "research_loop_count": updated_loop_count}

    # If the result is not valid return fallback query
    except (json.JSONDecodeError, KeyError, AttributeError):
        fallback_query = f"Tell me more about {state['research_brief']}"
        
        return {"search_queries": [fallback_query], "research_loop_count": updated_loop_count}
