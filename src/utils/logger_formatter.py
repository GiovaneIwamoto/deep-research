import logging
from typing import List, Dict, Any
from models.base import QueryResult


def logging_clarification_needed(clarification_question: str) -> None:
    """
    Log the clarification needed.
    """
    logging.info(f"[CLARIFICATION NEEDED]: {clarification_question}\n\n")

def logging_generated_research_brief(research_brief: str) -> None:
    """
    Log the generated research brief.
    """
    logging.info(f"[GENERATED RESEARCH BRIEF]:\n\n{research_brief}\n\n")

def logging_query_generator(queries: List[str]) -> None:
    """
    Log the queries for the query generator.
    """
    logging.info(f"[GENERATED SEARCH QUERIES]:\n\n{queries}\n\n")

def logging_researcher_spawner() -> None:
    """
    Log the researcher spawner.
    """
    logging.info("[RESEARCHER SPAWNER]: Spawning parallel researcher agents.\n")

def logging_search_result_summary(query: str, query_results: QueryResult) -> None:
    """
    Log the search result summary.
    """
    logging.info(f"[QUERY: {query}] [SEARCH RESULT SUMMARY]:\n\n{query_results}\n\n")

def logging_no_content_extracted(query: str, url_link: str) -> None:
    """
    Log the no content extracted from the query.
    """
    logging.warning(f"[NO CONTENT EXTRACTED FROM QUERY]: {query}\n(URL: {url_link})\n\n")

def logging_reflection_analysis(reflection_content: Dict[str, Any]) -> None:
    """
    Log the reflection analysis.
    """
    logging.info(f"[REFLECTION ANALYSIS]:\n\n[KNOWLEDGE GAPS]:\n\n{reflection_content.get('knowledge_gaps', [])}\n\n")
    logging.info(f"[FOLLOW-UP QUERIES]:\n\n{reflection_content.get('follow_up_queries', [])}\n\n")

def logging_final_report_writer(search_results: str) -> None:
    """
    Log the search results for the final report writer.
    """
    logging.info(f"[COMPILED SEARCH RESULTS FOR FINAL SYNTHESIS]:\n\n{search_results}\n\n")