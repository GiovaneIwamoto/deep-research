"""
Define the main workflow graph for the Deep Research Agent.
This module only builds and returns the compiled graph, ready to be invoked.
"""

from models.base import ReportState
from services.final_report_writer import write_final_report
from services.query_generator import generate_queries
from services.researcher_spawner import spawn_researchers
from router.flow_control import decide_reflection_or_compose
from services.search_summarizer import search_and_summarize
from services.summary_reflector import reflect_on_summary
from langgraph.graph import START, END, StateGraph

def build_graph() -> StateGraph[ReportState]:
    """
    Builds and returns the LangGraph workflow used by the Deep Research Agent.

    This graph defines the nodes and conditional transitions that control the
    flow of reasoning, searching, reflecting, and final answer generation.
    """
    builder = StateGraph(ReportState)
    
    # Nodes
    builder.add_node("generate_queries", generate_queries)
    builder.add_node("search_and_summarize", search_and_summarize)
    builder.add_node("reflect_on_summary", reflect_on_summary)
    builder.add_node("write_final_report", write_final_report)
    
    # Edges
    builder.add_edge(START, "generate_queries")
    builder.add_conditional_edges("generate_queries", spawn_researchers, ["search_and_summarize"])
    builder.add_conditional_edges("search_and_summarize", decide_reflection_or_compose, ["reflect_on_summary", "write_final_report"])
    builder.add_conditional_edges("reflect_on_summary", spawn_researchers, ["search_and_summarize"])
    builder.add_edge("write_final_report", END)
    
    # Compile the graph
    graph = builder.compile()
    return graph 