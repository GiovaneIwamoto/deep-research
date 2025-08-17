"""
Main workflow graph definition for the Deep Research Agent.

This module defines the complete LangGraph workflow that orchestrates research process, including:
Chatbot interaction, Topic clarification, Research brief generation, Research execution, Reflection and Report generation.
"""

from langgraph.graph import START, END, StateGraph

from models.base import ChatbotState, DeepResearchState
from router.flow_control import decide_reflection_or_compose
from services.chatbot import chatbot_conversation
from services.final_report_writer import write_final_report
from services.query_generator import generate_queries
from services.research_brief_generator import generate_research_brief
from services.researcher_spawner import spawn_researchers
from services.search_summarizer import search_and_summarize
from services.summary_reflector import reflect_on_summary
from services.user_topic_clarifier import clarify_user_topic


def build_deep_research_graph() -> StateGraph[DeepResearchState]:
    """
    Builds the deep research graph for the main research workflow.
    This graph handles the core research process of clarifying the user's topic, generating a research brief, generating queries, searching and summarizing the results, reflecting on the summaries, and writing the final report.
    
    Returns:
        StateGraph[DeepResearchState]: Compiled deep research workflow graph
    """
    # Initialize the graph
    deep_research_graph = StateGraph(DeepResearchState)
    
    # Nodes
    deep_research_graph.add_node("clarify_user_topic", clarify_user_topic)
    deep_research_graph.add_node("generate_research_brief", generate_research_brief)
    deep_research_graph.add_node("generate_queries", generate_queries)
    deep_research_graph.add_node("search_and_summarize", search_and_summarize)
    deep_research_graph.add_node("reflect_on_summary", reflect_on_summary)
    deep_research_graph.add_node("write_final_report", write_final_report)
    
    # Edges
    deep_research_graph.add_edge(START, "clarify_user_topic")
    deep_research_graph.add_edge("clarify_user_topic", "generate_research_brief")
    deep_research_graph.add_edge("generate_research_brief", "generate_queries")
    deep_research_graph.add_edge("write_final_report", END)


    # Conditional Edge - Generate Queries
    deep_research_graph.add_conditional_edges("generate_queries", spawn_researchers, ["search_and_summarize"])
    
    # Conditional Edge - Decide Reflection or Compose
    deep_research_graph.add_conditional_edges("search_and_summarize", decide_reflection_or_compose, ["reflect_on_summary", "write_final_report"])
    
    # Conditional Edge - Reflect on Summary
    deep_research_graph.add_conditional_edges("reflect_on_summary", spawn_researchers, ["search_and_summarize"])
        
    return deep_research_graph.compile()


def build_chatbot_graph() -> StateGraph[ChatbotState]:
    """
    Builds the chatbot graph that allows the user to interact with the agent and start the research process.
    This graph manages the complete user experience from initial conversation through research execution and final report delivery.
    
    Returns:
        StateGraph[ChatbotState]: Compiled chatbot workflow graph
    """
    # Initialize the graph
    chatbot_graph = StateGraph(ChatbotState)
    
    # Build Deep Research Graph
    deep_research_graph = build_deep_research_graph()
    
    # Nodes
    chatbot_graph.add_node("chatbot", chatbot_conversation)
    chatbot_graph.add_node("run_deep_research", deep_research_graph)
    
    # Edges
    chatbot_graph.add_edge(START, "chatbot")
    chatbot_graph.add_edge("run_deep_research", END)

    return chatbot_graph.compile()


def build_graph() -> StateGraph[ChatbotState]:
    """Builds and returns the complete LangGraph workflow for the Deep Research Agent."""
    return build_chatbot_graph()
