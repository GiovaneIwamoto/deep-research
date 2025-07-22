"""
Main entry point for the Deep Research Agent workflow graph.
Handles user input, logging, and orchestrates the research workflow using the services layer.
"""

from config.logging_config import setup_logging
import logging
import os
import dotenv
from models.base import ReportState
from services import (
    build_first_queries,
    spawn_researchers,
    single_search,
    final_writer,
    reflect_on_summary,
    route_after_single_search
)
from langgraph.graph import START, END, StateGraph


def get_user_input() -> tuple[str, bool, int]:
    """
    Prompt the user for research topic, reflection usage, and number of loops.
    Returns a tuple: (user_input, use_reflection, reflection_loops)
    """
    user_input = input("Enter the research topic or question: ").strip()
    reflection_choice = input("Enable reflection? (y/n): ").strip().lower()
    if reflection_choice in ["y", "yes", "true"]:
        use_reflection = True
        while True:
            try:
                reflection_loops = int(input("How many reflection loops?: ").strip())
                if reflection_loops >= 1:
                    break
                else:
                    print("Please enter a number greater than or equal to 1.")
            except ValueError:
                print("Please enter a valid integer.")
    else:
        use_reflection = False
        reflection_loops = 1
    return user_input, use_reflection, reflection_loops


def main():
    """
    Main entry point for the Deep Research Agent application.
    """
    setup_logging()
    dotenv.load_dotenv()
    # Get user configuration
    user_input, use_reflection, reflection_loops = get_user_input()

    # Build the research workflow graph
    builder = StateGraph(ReportState)
    builder.add_node("build_first_queries", build_first_queries)
    builder.add_node("single_search", single_search)
    builder.add_node("reflect_on_summary", reflect_on_summary)
    builder.add_node("final_writer", final_writer)
    builder.add_edge(START, "build_first_queries")
    builder.add_conditional_edges("build_first_queries", spawn_researchers, ["single_search"])
    builder.add_conditional_edges("single_search", route_after_single_search, ["reflect_on_summary", "final_writer"])
    builder.add_conditional_edges("reflect_on_summary", spawn_researchers, ["single_search"])
    builder.add_edge("final_writer", END)
    graph = builder.compile()

    # Run the workflow
    response = graph.invoke({
        "user_input": user_input,
        "use_reflection": use_reflection,
        "reflection_loops": reflection_loops
    })

    # Print the final report
    print("\n[FINAL REPORT]\n")
    print(response['final_response'].messages[0].content)


if __name__ == "__main__":
    main() 