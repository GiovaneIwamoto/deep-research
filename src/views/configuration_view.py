"""
Configuration view module for displaying configuration summaries.
"""

from config.system_config import Configuration


def print_configuration_summary(user_config: dict):
    """
    Print a table of the current configuration and its sources.
    """
    print("\n" + "="*60 + "\n" + "CONFIGURATION SUMMARY" + "\n" + "="*60 + "\n")
    
    # Create a temporary config to see what values are being used
    temp_config = {"configurable": user_config}
    config = Configuration.from_runnable_config(temp_config)
    
    # Define configuration categories
    model_configs = {
        "Query Generation Model": config.query_generation_model,
        "Summarization Model": config.summarization_model,
        "Reflection Model": config.reflection_model,
        "Final Report Model": config.final_report_model,
    }
    
    research_configs = {
        "Research Units Initial": config.research_units_initial,
        "Research Units Reflection": config.research_units_reflection,
        "Allow Reflection": str(config.allow_reflection).title(),
        "Reflection Loops": config.reflection_loops,
        "Reasoning Effort": config.reasoning_effort,
    }
    
    system_configs = {
        "Search API": config.search_api.value,
        "Allow Clarification": str(config.allow_clarification).title(),
    }
    
    # Print model configurations
    print("\n[AI MODELS]:")
    for key, value in model_configs.items():
        source = "USER INPUT" if key.lower().replace(" ", "_") in user_config else "ENV/DEFAULT"
        print(f"  {key:<30} {value:<20} [{source}]")
    
    # Print research configurations
    print("\n[RESEARCH SETTINGS]:")
    for key, value in research_configs.items():
        config_key = key.lower().replace(" ", "_")
        source = "USER INPUT" if config_key in user_config else "ENV/DEFAULT"
        print(f"  {key:<30} {value:<20} [{source}]")
    
    # Print system configurations
    print("\n[SYSTEM SETTINGS]:")
    for key, value in system_configs.items():
        config_key = key.lower().replace(" ", "_")
        source = "USER INPUT" if config_key in user_config else "ENV/DEFAULT"
        print(f"  {key:<30} {value:<20} [{source}]")
    
    print("\n" + "="*60 + "\n" + "Priority: USER INPUT > ENV VARIABLES > DEFAULTS" + "\n" + "="*60 + "\n") 