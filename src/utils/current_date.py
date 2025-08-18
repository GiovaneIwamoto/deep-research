"""
Utility date functions for the Deep Research Agent project.
"""

from datetime import date

def get_current_date() -> str:
    """Get the current date in YYYY-MM-DD format."""
    return date.today().strftime("%Y-%m-%d")