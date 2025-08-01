"""
Main entrypoint for the Deep Research Agent.
Responsible for collecting user input, building the workflow graph, and executing the workflow.
"""

import dotenv
from datetime import date
from config.logging_config import setup_logging
from interface.input import get_user_input
from core.graph import build_graph


def main():
    """
    Runs the main workflow of the research agent.
    """
    setup_logging()
    dotenv.load_dotenv()
    
    # Collect user input and reflection settings
    user_input, use_reflection, reflection_loops = get_user_input()

    # Get the current date in YYYY-MM-DD format
    current_date = date.today().strftime("%Y-%m-%d")

    # Build the workflow graph
    graph = build_graph()
    
    response = graph.invoke({
        "user_input": user_input,
        "use_reflection": use_reflection,
        "reflection_loops": reflection_loops,
        "current_date": current_date,
    })
    
    print("\n\nFINAL REPORT\n\n")
    print(response['final_report'].content)


if __name__ == "__main__":
    main() 