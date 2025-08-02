"""
Final report writer services for the Deep Research Agent project.
"""

import logging
from models.base import ReportState
from templates.prompt_final_report_writer import final_report_writer_prompt 
from langchain_openai import ChatOpenAI
from typing import Dict, Any


def write_final_report(state: ReportState) -> Dict[str, Any]:
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
    
    logging.info("\n\nCompiled search results for final synthesis:\n\n%s", search_results)
    
    default_llm_openai = ChatOpenAI(model="gpt-4.1-mini-2025-04-14")
    final_report = default_llm_openai.invoke(prompt)
    
    return {"final_report": final_report} 