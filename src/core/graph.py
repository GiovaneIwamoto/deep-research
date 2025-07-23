"""
Define the main workflow graph for the Deep Research Agent.
This module only builds and returns the compiled graph, ready to be invoked.
"""

from models.base import ReportState
from services.final_writer import final_writer
from services.query_generation import build_first_queries, spawn_researchers, route_after_single_search
from services.search import single_search
from services.reflection import reflect_on_summary
from langgraph.graph import START, END, StateGraph

def build_graph():
    """
    Builds and returns the workflow graph, parameterized by the user input.
    """
    builder = StateGraph(ReportState)
    
    # Nodes
    builder.add_node("build_first_queries", build_first_queries)
    builder.add_node("single_search", single_search)
    builder.add_node("reflect_on_summary", reflect_on_summary)
    builder.add_node("final_writer", final_writer)
    
    # Edges
    builder.add_edge(START, "build_first_queries")
    builder.add_conditional_edges("build_first_queries", spawn_researchers, ["single_search"])
    builder.add_conditional_edges("single_search", route_after_single_search, ["reflect_on_summary", "final_writer"])
    builder.add_conditional_edges("reflect_on_summary", spawn_researchers, ["single_search"])
    builder.add_edge("final_writer", END)
    
    # Compile the graph
    graph = builder.compile()
    return graph 