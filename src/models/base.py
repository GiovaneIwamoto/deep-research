"""
BaseModel classes for the Deep Research Agent project.
All Pydantic models for state and results are defined here.
"""

from pydantic import BaseModel
from typing import List
from typing_extensions import Annotated
import operator

class QueryResult(BaseModel):
    """
    Represents the result of a single web search query, including title, url, and a summary.
    """
    title: str = None
    url: str = None
    summary: str = None

class ReportState(BaseModel):
    """
    Maintains the state of the research workflow, including user input, queries, and results.
    Annotated at queries_results with operator.add to allow for concatenation of lists.
    """
    user_input: str = None
    final_report: str = None
    search_queries: List[str] = []
    queries_results: Annotated[List[QueryResult], operator.add]
    research_loop_count: int = 0
    current_date: str = None