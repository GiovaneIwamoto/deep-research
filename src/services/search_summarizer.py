"""
Search and summarize services for the Deep Research Agent project.
"""

import logging
from typing import Dict, Any
from tavily import TavilyClient
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableConfig

from models.base import QueryResult
from utils.current_date import get_current_date
from config.system_config import Configuration
from templates.prompt_web_search_summarizer import web_search_summarizer_prompt

def search_and_summarize(data: Dict[str, Any], config: RunnableConfig) -> Dict[str, Any]:
    """Perform a web search for the given query, extract content, and summarize it using an LLM."""
    configurable = Configuration.from_runnable_config(config)
    
    # Get query
    query = data["query"]

    # Tavily search
    tavily_client = TavilyClient()
    results = tavily_client.search(query, max_results=1, include_raw_content=False)

    # Extract url link and content
    url_link = results["results"][0]["url"]
    url_content = tavily_client.extract(url_link)
    
    # If the content is not empty summarize it
    if len(url_content["results"]) > 0:
        raw_content = url_content["results"][0]["raw_content"]

        # Configure model
        summarizer_llm = ChatOpenAI(model=configurable.summarization_model)

        # Invoke model
        prompt = web_search_summarizer_prompt.format(current_date=get_current_date(), page_content=raw_content)
        response = summarizer_llm.invoke(prompt)
        
        # Create query result object
        query_results = QueryResult(
            title=results["results"][0]["title"],
            url=url_link,
            summary=response.content
        )
        logging.info(f"Query: {query}\n\n[Search Result Summary]:\n\n{query_results}\n\n")

    else:
        query_results = QueryResult(
            title=results["results"][0]["title"],
            url=url_link,
            summary="No content could be extracted from the provided URL."
        )
        logging.warning(f"[No content extracted from query]: {query}\n(URL: {url_link})\n\n")

    return {"queries_results": [query_results]}
