"""
Prompt for summarizing web search results.
"""
from .agent_prompt import agent_prompt

resume_search = agent_prompt + """
Your objective here is to analyze the web search results and make a synthesis of it.
Emphasize the most relevant information based on user's question.

After your work, another agent will use the synthesis to build a final response to the user,
so make sure the synthesis contains only useful information.

Write about maximum of two paragraphs, and use only the information obtained from the web search results.

Here is the web search results:

<SEARCH_RESULTS>
{search_results}
</SEARCH_RESULTS>
"""
