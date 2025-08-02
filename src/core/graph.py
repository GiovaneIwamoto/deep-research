"""
Define the main workflow graph for the Deep Research Agent.
This module only builds and returns the compiled graph, ready to be invoked.
"""

from models.base import ReportState
from services.write_final_report import write_final_report
from services.query_generation import build_first_queries
from services.researcher_spawning import spawn_researchers
from router.flow_control import decide_reflection_or_compose
from services.search_summarize import search_summarize
from services.summary_reflection import reflect_on_summary
from langgraph.graph import START, END, StateGraph

def build_graph() -> StateGraph[ReportState]:
    """
    Builds and returns the LangGraph workflow used by the Deep Research Agent.

    This graph defines the nodes and conditional transitions that control the
    flow of reasoning, searching, reflecting, and final answer generation.
    """
    builder = StateGraph(ReportState)
    
    # Nodes
    builder.add_node("build_first_queries", build_first_queries)
    builder.add_node("search_summarize", search_summarize)
    builder.add_node("reflect_on_summary", reflect_on_summary)
    builder.add_node("write_final_report", write_final_report)
    
    # Edges
    builder.add_edge(START, "build_first_queries")
    builder.add_conditional_edges("build_first_queries", spawn_researchers, ["search_summarize"])
    builder.add_conditional_edges("search_summarize", decide_reflection_or_compose, ["reflect_on_summary", "final_writer"])
    builder.add_conditional_edges("reflect_on_summary", spawn_researchers, ["search_summarize"])
    builder.add_edge("write_final_report", END)
    
    # Compile the graph
    graph = builder.compile()
    return graph 