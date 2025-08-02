"""
Search and summarization services for the Deep Research Agent project.
"""

import logging
from models.base import QueryResult
from templates.summary_web_search import summary_web_search_prompt
from tavily import TavilyClient
from langchain_openai import ChatOpenAI
from typing import Dict, Any


def search_summarize(data: Dict[str, Any]) -> Dict[str, Any]:
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

    # Summarize the content using an LLM
    default_llm_openai = ChatOpenAI(model="gpt-4.1-mini-2025-04-14")

    # If the content is not empty, summarize it using an LLM
    if len(url_extraction["results"]) > 0:
        raw_content = url_extraction["results"][0]["raw_content"]

        prompt = summary_web_search_prompt.format(current_date=current_date, page_content=raw_content)
        llm_result = default_llm_openai.invoke(prompt)
        
        # Create the query result
        query_results = QueryResult(
            title=results["results"][0]["title"],
            url=url,
            summary=llm_result.content
        )
        logging.info(f"\nQuery: {query}\n\nSearch result summary:\n{query_results}\n")

    else:
        query_results = QueryResult(
            title=results["results"][0]["title"],
            url=url,
            summary="No content could be extracted from the provided URL."
        )
        logging.warning(f"\nNo content extracted for query: {query} (URL: {url})\n")
    return {"queries_results": [query_results]} 