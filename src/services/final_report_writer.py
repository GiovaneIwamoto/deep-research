"""
Final report writer services for the Deep Research Agent project.
"""

import logging
from models.base import ReportState
from templates.prompt_final_report_writer import final_report_writer_prompt 
from config.system_config import Configuration
from langchain_core.runnables import RunnableConfig
from langchain_openai import ChatOpenAI
from typing import Dict, Any


def write_final_report(state: ReportState, config: RunnableConfig) -> Dict[str, Any]:
    """
    Aggregate all search results and synthesize a final report using an LLM.
    """
    search_results = ""
    reference = ""
    
    # Aggregate all search results and synthesize a final report.
    for i, result in enumerate(state.queries_results):
        search_results += f"[{i+1}]\n\n"
        search_results += f"Title: {result.title}\n"
        search_results += f"URL: {result.url}\n"
        search_results += f"Content: {result.summary}\n\n"
        reference += f"[{i+1}] - {result.title} ({result.url})\n"
    
    prompt = final_report_writer_prompt.format(current_date=state.current_date, 
                                              research_brief=state.user_input, 
                                              aggregated_summaries=search_results)
    
    logging.info(f"[COMPILED SEARCH RESULTS FOR FINAL SYNTHESIS]:\n\n{search_results}\n\n")
    
    # Use configuration from RunnableConfig
    configurable = Configuration.from_runnable_config(config)
    model_name = configurable.final_report_model
    
    # Use the configured model for final report generation
    final_report_llm = ChatOpenAI(model=model_name)
    final_report = final_report_llm.invoke(prompt)
    
    return {"final_report": final_report} 