"""
Logging configuration for the Deep Research Agent project.
Call setup_logging() at the start of your application to configure logging.
"""

import logging

def setup_logging():
    """
    Configure logging for the project with INFO level and a clear format.
    """
    logging.basicConfig(
        level=logging.INFO,
        format='[%(levelname)s] %(message)s'
    ) 