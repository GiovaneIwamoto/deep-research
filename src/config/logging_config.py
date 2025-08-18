"""
Logging configuration for the Deep Research Agent.

This module provides centralized logging configuration for the entire research
workflow. It sets up consistent logging format and levels across all components.
"""

import logging
from typing import Optional


def setup_logging(level: Optional[int] = None) -> None:
    """
    Configure logging for the Deep Research Agent.
    
    Sets up a consistent logging format and level across all components
    of the research workflow. The default level is INFO.
    
    Args:
        level: Optional logging level (defaults to logging.INFO)
    """
    log_level = level or logging.INFO
    
    logging.basicConfig(
        level=log_level,
        format='[%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Suppress verbose logging from external libraries
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("openai").setLevel(logging.WARNING) 