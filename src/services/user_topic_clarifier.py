from typing import Literal
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage, get_buffer_string
from langchain_core.runnables import RunnableConfig
from langgraph.types import Command

from config.system_config import Configuration
from models.base import DeepResearchState, UserTopicClarification
from templates.prompt_user_topic_clarifier import user_topic_clarifier_prompt


def clarify_user_topic(state: DeepResearchState, config: RunnableConfig) -> Command[Literal["generate_research_brief", "clarify_user_topic"]]:
    """Clarifies the user's research topic by interacting with an LLM."""
    
    messages = state["messages"]
    configurable = Configuration.from_runnable_config(config)
    
    # If clarification is not allowed, go to generate research brief
    if not configurable.allow_clarification:
        return Command(goto="generate_research_brief")

    # Model with structured output
    user_topic_clarifier_llm = ChatOpenAI(model=configurable.user_topic_clarification_model)
    llm_with_structured_output = user_topic_clarifier_llm.with_structured_output(UserTopicClarification)

    # Prompt with conversation history
    prompt = user_topic_clarifier_prompt.format(conversation_history=get_buffer_string(messages))    
    response = llm_with_structured_output.invoke(prompt)

    # If the user needs clarification, ask for it
    if response.need_clarification:
        messages.append(AIMessage(content=response.clarify_question))
        print(f"\nClarification needed: {response.clarify_question}\n")

        user_input = input("\nYou: ").strip()
        messages.append(HumanMessage(content=user_input))

        return Command(goto="clarify_user_topic")
    else:
        messages.append(AIMessage(content=response.acknowledgement_message))
        # The research topic is now the acknowledgement message
        return Command(goto="generate_research_brief", update={"research_topic": response.acknowledgement_message})
