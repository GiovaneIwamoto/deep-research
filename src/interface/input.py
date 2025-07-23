"""
Module responsible for collecting user input for the Deep Research Agent.
"""

def get_user_input() -> tuple[str, bool, int]:
    """
    Prompts the user for the research topic, whether to enable reflection, and the number of loops.
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
                    print("Please enter a number greater than or equal to one.")
            except ValueError:
                print("Please enter a valid integer.")
    else:
        use_reflection = False
        reflection_loops = 1
    return user_input, use_reflection, reflection_loops 