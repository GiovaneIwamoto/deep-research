"""
Reflection and follow-up query generation services for the Deep Research Agent project.
"""

import logging
from models.base import ReportState
from templates.reflection_instructions import reflection_instructions
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from typing import Dict, Any
import json


def reflect_on_summary(state: ReportState) -> Dict[str, Any]:
    """
    Use an LLM to reflect on the current summary, identify knowledge gaps, and generate follow-up queries.
    """
    new_loop_count = state.research_loop_count + 1
    reasoning_llm_openai = ChatOpenAI(
        model="o4-mini-2025-04-16",
        reasoning_effort="medium",
    )
    result = reasoning_llm_openai.invoke([
        SystemMessage(content=reflection_instructions.format(research_topic=state.user_input)),
        HumanMessage(content=f"Reflect on our existing knowledge: \n === \n {state.queries_results}, \n === \n And now identify knowledge gaps and generate 1-2 follow-up web search queries:")
    ])
    try:
        reflection_content = json.loads(result.content)
        logging.info("Reflection analysis:")
        logging.info(f"Knowledge gaps: {reflection_content.get('knowledge_gaps', [])}")
        logging.info(f"Follow-up queries: {reflection_content.get('follow_up_queries', [])}")
        logging.info("End of reflection analysis.\n")
        queries = reflection_content.get('follow_up_queries', [])
        if not queries:
            queries = [f"Tell me more about {state.user_input}"]
        return {
            "search_queries": queries,
            "research_loop_count": new_loop_count
        }
    except (json.JSONDecodeError, KeyError, AttributeError):
        fallback_query = f"Tell me more about {state.user_input}"
        return {
            "search_queries": [fallback_query],
            "research_loop_count": new_loop_count
        }
