"""
Flow control and routing services for the Deep Research Agent project.
"""

import logging
from models.base import ReportState


def decide_reflection_or_compose(state: ReportState) -> str:
    """
    Decide whether to continue with reflection or proceed to final report composition
    after the single agent has completed search and summarization.
    """
    if state.use_reflection and state.research_loop_count < state.reflection_loops:
        return "reflect_on_summary"
    else:
        return "write_final_report" 