"""
Main entrypoint for the Deep Research Agent.
Responsible for collecting user input, building the workflow graph, and executing the workflow.
"""

import dotenv
from datetime import date
from config.logging_config import setup_logging
from interface.user_input import get_user_input
from views.configuration_view import print_configuration_summary
from core.graph import build_graph


def main():
    """
    Runs the main workflow of the research agent.
    """
    setup_logging()
    dotenv.load_dotenv()
    
    # Collect user input and configuration preferences
    user_input, user_config = get_user_input()

    # Print configuration summary
    print_configuration_summary(user_config)

    # Get the current date in YYYY-MM-DD format
    current_date = date.today().strftime("%Y-%m-%d")

    # Build the workflow graph
    graph = build_graph()
    
    # Create configurable dict with user preferences
    configurable = user_config
    
    response = graph.invoke({
        "user_input": user_input,
        "current_date": current_date,
    }, config={"configurable": configurable})
    
    print("\n\nFINAL REPORT\n\n")
    print(response['final_report'].content)


if __name__ == "__main__":
    main() 