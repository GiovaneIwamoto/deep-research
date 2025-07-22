"""
Prompt for building search queries.
"""
from .agent_prompt import agent_prompt

build_queries = agent_prompt + """
Your first objective is to build a list of queries that
will be used to find answers to the user's question.

Build only 2 queries, each query should be a single sentence.
"""
