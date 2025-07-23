"""
Main entrypoint for the Deep Research Agent.
Responsible for collecting user input, building the workflow graph, and executing the workflow.
"""

import dotenv
from config.logging_config import setup_logging
from interface.input import get_user_input
from core.graph import build_graph


def main():
    """
    Runs the main workflow of the research agent.
    """
    setup_logging()
    dotenv.load_dotenv()
    user_input, use_reflection, reflection_loops = get_user_input()
    graph = build_graph(user_input, use_reflection, reflection_loops)
    response = graph.invoke({
        "user_input": user_input,
        "use_reflection": use_reflection,
        "reflection_loops": reflection_loops
    })
    print("\n\nFINAL REPORT\n\n")
    print(response['final_response'].messages[0].content)


if __name__ == "__main__":
    main() 