"""
Main entrypoint for the Deep Research Agent project.
"""

import dotenv
from config.logging_config import setup_logging
from interface.user_configuration import get_user_configuration
from views.configuration_view import print_configuration_summary
from core.graph import build_graph

def main():
    # Setup logging
    setup_logging()
    
    # Load environment variables
    dotenv.load_dotenv()
    
    # Collect and print user configuration preferences
    user_config = get_user_configuration()
    print_configuration_summary(user_config)

    # Build the workflow graph and invoke it
    graph = build_graph()
    
    initial_state = {"messages": []}

    response = graph.invoke(initial_state, config={"configurable": user_config})
    print(response['final_report'])

if __name__ == "__main__":
    main() 