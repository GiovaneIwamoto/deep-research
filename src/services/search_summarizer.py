"""
Search and summarize services for the Deep Research Agent project.
"""

import logging
from models.base import QueryResult
from templates.prompt_web_search_summarizer import web_search_summarizer_prompt
from config.system_config import Configuration
from langchain_core.runnables import RunnableConfig
from tavily import TavilyClient
from langchain_openai import ChatOpenAI
from typing import Dict, Any


def search_and_summarize(data: Dict[str, Any], config: RunnableConfig) -> Dict[str, Any]:
    """
    Perform a web search for the given query, extract content, and summarize it using an LLM.
    This function represents a single agent that handles both search and summarization tasks.
    """
    # Get the query and current date from the data
    query = data["query"]
    current_date = data["current_date"]

    # Initialize the Tavily client
    tavily_client = TavilyClient()

    # Search for the query
    results = tavily_client.search(query, max_results=1, include_raw_content=False)

    # Extract the url from the results
    url = results["results"][0]["url"]
    url_extraction = tavily_client.extract(url)

    # Use configuration from RunnableConfig
    configurable = Configuration.from_runnable_config(config)
    model_name = configurable.summarization_model

    # Summarize the content using an LLM
    summarization_llm = ChatOpenAI(model=model_name)

    # If the content is not empty, summarize it using an LLM
    if len(url_extraction["results"]) > 0:
        raw_content = url_extraction["results"][0]["raw_content"]

        prompt = web_search_summarizer_prompt.format(current_date=current_date, page_content=raw_content)
        llm_result = summarization_llm.invoke(prompt)
        
        # Create the query result
        query_results = QueryResult(
            title=results["results"][0]["title"],
            url=url,
            summary=llm_result.content
        )
        logging.info(f"QUERY: {query}\n\n[SEARCH RESULT SUMMARY]:\n\n{query_results}\n\n")

    else:
        query_results = QueryResult(
            title=results["results"][0]["title"],
            url=url,
            summary="No content could be extracted from the provided URL."
        )
        logging.warning(f"[NO CONTENT EXTRACTED FROM QUERY]: {query}\n(URL: {url})\n\n")

    return {"queries_results": [query_results]} 