"""
Research brief generator service for the Deep Research Agent project.
"""

from langchain_openai import ChatOpenAI
from langchain_core.messages import get_buffer_string
from langchain_core.runnables import RunnableConfig

from models.base import DeepResearchState
from config.system_config import Configuration
from templates.prompt_research_brief_generator import research_brief_generator_prompt


def generate_research_brief(state: DeepResearchState, config: RunnableConfig) -> dict:
    """Generate a research brief based on all the conversation history including chatbot messages and clarification attempts."""
    configurable = Configuration.from_runnable_config(config)

    # Configure model
    research_brief_generator_llm = ChatOpenAI(model=configurable.research_brief_generation_model)
    prompt = research_brief_generator_prompt.format(conversation_history=get_buffer_string(state['messages']))
    print(f"\n\nPrompt Research Brief Generator: {prompt}\n\n")
    
    # Invoke model
    response = research_brief_generator_llm.invoke(prompt)
    print(f"\n\nResponse Research Brief Generator: {response.content}\n\n")

    return {"research_brief": response.content}
