"""
Flow control and routing services for the Deep Research Agent project.
"""

import logging
from models.base import ReportState
from config.system_config import Configuration
from langchain_core.runnables import RunnableConfig


def decide_reflection_or_compose(state: ReportState, config: RunnableConfig) -> str:
    """
    Decide whether to continue with reflection or proceed to final report composition
    after the single agent has completed search and summarization.
    """
    configurable = Configuration.from_runnable_config(config)
    
    if configurable.allow_reflection and state.research_loop_count < configurable.reflection_loops:
        return "reflect_on_summary"
    else:
        return "write_final_report" 