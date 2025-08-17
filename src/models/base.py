"""
Base model classes for the Deep Research Agent project.

This module defines all Pydantic models used for state management and structured outputs
throughout the research workflow. These models ensure type safety and data validation.
"""

import operator
from pydantic import BaseModel, Field
from typing import List, Optional, Annotated
from langgraph.graph import MessagesState


# Structured Outputs

class ChatbotResponse(BaseModel):
    """
    Structured output for chatbot conversation analysis.
    
    This model represents the analysis of user input to determine if a research
    topic has been provided and the appropriate response to give.
    """
    should_start_research: bool = Field(description="Whether the user has provided a research topic and research should begin")
    research_topic: str = Field(description="The user's research topic that was provided")
    response_message: str = Field(description="The response message to display to the user")

class UserTopicClarification(BaseModel):
    """
    Structured output for user topic clarification process.
    
    This model represents the decision made by the topic clarifier agent
    regarding whether the user's research topic needs further clarification.
    """
    need_clarification: bool = Field(description="Whether the user's topic needs further clarification")
    clarify_question: str = Field(description="Specific question to ask the user for clarification")
    acknowledgement_message: str = Field(description="Message acknowledging the topic and confirming research will start")

class QueryResult(BaseModel):
    """
    Structured output for web search results.

    This model stores the structured data from web search results including
    the source information and extracted content summary.
    """
    title: Optional[str] = Field(description="Title of the web page or article")
    url: Optional[str] = Field(description="URL of the source")
    summary: Optional[str] = Field(description="Extracted and summarized content from the source")


# State models

class ChatbotState(MessagesState):
    """State management for the chatbot workflow."""
    should_start_research: bool
    research_topic: str

class DeepResearchState(MessagesState):
    """State management for the deepresearch workflow."""
    current_date: Optional[str]
    research_topic: Optional[str]
    research_brief: Optional[str]
    search_queries: List[str] = []
    queries_results: Annotated[List[QueryResult], operator.add]
    final_report: Optional[str]
    research_loop_count: int = 0
    