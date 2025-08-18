"""
User configuration preferences for the Deep Research Agent project.
"""

def get_user_configuration() -> dict:
    """Gets configuration preferences for the user."""
    
    print("\nDeep Research Agent Configuration\n")
    
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
    
    return user_config
