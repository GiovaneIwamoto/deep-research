"""
Prompt for building the final response.
"""
from .agent_prompt import agent_prompt

build_final_response = agent_prompt + """
Your objective here is to develop a final response to the user using the reports made during
the web search, with their syntesis.

The response should contain something between 3 and 5 paragraphs.

Here is the web search results:

<SEARCH_RESULTS>
{search_results}
</SEARCH_RESULTS>

You must add reference citations with the number of the citation (e.g. [1], [2], etc.) at the end of each paragraph.
"""
