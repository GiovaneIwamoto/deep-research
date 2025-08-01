"""
Reflection and follow-up query generation services for the Deep Research Agent project.
"""

import logging
from models.base import ReportState
from templates.knowledge_gap_reflection import knowledge_gap_reflection_prompt
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from typing import Dict, Any
import json


def reflect_on_summary(state: ReportState) -> Dict[str, Any]:
    """
    Use an reasoning model to reflect on the current summary, identify knowledge gaps, and generate follow-up queries.
    """
    new_loop_count = state.research_loop_count + 1
    
    # Define the reasoning model
    reasoning_llm_openai = ChatOpenAI(
        model="o4-mini-2025-04-16",
        reasoning_effort="medium",
    )

    # Invoke the reasoning model
    result = reasoning_llm_openai.invoke([
        SystemMessage(content=knowledge_gap_reflection_prompt.format(research_brief=state.user_input, aggregated_summaries=state.queries_results))
    ])

    # Parse the result
    try:
        reflection_content = json.loads(result.content)
        
        logging.info("Reflection analysis:")
        logging.info(f"Knowledge gaps: {reflection_content.get('knowledge_gaps', [])}")
        logging.info(f"Follow-up queries: {reflection_content.get('follow_up_queries', [])}")
        logging.info("End of reflection analysis.\n")
        
        queries = reflection_content.get('follow_up_queries', [])
        
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
