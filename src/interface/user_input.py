"""
Module responsible for collecting user input for the Deep Research Agent.
"""

def get_user_input() -> tuple[str, dict]:
    """
    Prompts the user for the research topic and configuration preferences.
    Returns a tuple: (user_input, user_config)
    """
    # Ask for the research topic
    user_input = input("Enter the research topic or question: ").strip()
    
    # Ask for reflection preferences
    reflection_choice = input("Enable reflection? (y/n): ").strip().lower()
    
    user_config = {}
    
    # If the user wants to enable reflection ask for the number of loops
    if reflection_choice in ["y", "yes", "true"]:
        user_config["allow_reflection"] = True
        while True:
            try:
                reflection_loops = int(input("How many reflection loops?: ").strip())
                if reflection_loops >= 1:
                    user_config["reflection_loops"] = reflection_loops
                    break
                else:
                    print("Please enter a number greater than or equal to one.")
            except ValueError:
                print("Please enter a valid integer.")
    else:
        user_config["allow_reflection"] = False
        user_config["reflection_loops"] = 1
    
    return user_input, user_config 