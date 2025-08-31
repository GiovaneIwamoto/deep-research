"""
Final report writer services for the Deep Research Agent project.

Rationale:
For detailed technical rationale and design thinking considerations please refer to the RATIONALE.md file Topic 01.
"""

from models.base import DeepResearchState
from templates.prompt_final_report_writer import final_report_writer_prompt 
from config.system_config import Configuration
from utils.current_date import get_current_date
from utils.logger_formatter import logging_final_report_writer

from langchain_core.runnables import RunnableConfig
from langchain_openai import ChatOpenAI
from typing import Dict, Any


def write_final_report(state: DeepResearchState, config: RunnableConfig) -> Dict[str, Any]:
    """
    Aggregate all search results and synthesize a final report using an LLM.
    """
    search_results = ""
    
    # Aggregate all search results and synthesize a final report.
    for i, result in enumerate(state.get("queries_results", [])):
        search_results += f"[{i+1}]\n\n"
        search_results += f"Title: {result.title}\n"
        search_results += f"URL: {result.url}\n"
        search_results += f"Content: {result.summary}\n\n"
    
    prompt = final_report_writer_prompt.format(current_date=get_current_date(), 
                                              research_brief=state["research_brief"], 
                                              aggregated_summaries=search_results)
    
    logging_final_report_writer(search_results)

    # Use configuration from RunnableConfig
    configurable = Configuration.from_runnable_config(config)
    
    # Use the configured model for final report generation
    final_report_llm = ChatOpenAI(model=configurable.final_report_model)
    final_report = final_report_llm.invoke(prompt)
    
    return {"final_report": final_report.content} 