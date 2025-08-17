"""
Chatbot workflow for the Deep Research Agent project.
"""

from typing import Literal
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage, get_buffer_string
from langchain_core.runnables import RunnableConfig
from langgraph.types import Command

from models.base import ChatbotState, ChatbotResponse
from config.system_config import Configuration
from templates.prompt_chatbot import chatbot_prompt


def chatbot_conversation(state: ChatbotState, config: RunnableConfig) -> Command[Literal["chatbot", "run_deep_research"]]:
    """Manages the chatbot conversation and detects when user provides a research topic."""
    
    messages = state["messages"]
    configurable = Configuration.from_runnable_config(config)

    # Greeting message
    if len(messages) == 1 and isinstance(messages[0], AIMessage):
        print(f"\nAgent: {messages[0].content}\n")

    # User input
    user_input = input("You: ").strip()

    # Add user message to state and messages
    messages.append(HumanMessage(content=user_input))
    
    # Model with structured output
    chatbot_llm = ChatOpenAI(model=configurable.chatbot_model)
    llm_with_structured_output = chatbot_llm.with_structured_output(ChatbotResponse)

    # Prompt with conversation history
    prompt = chatbot_prompt.format(conversation_history_chatbot=get_buffer_string(messages))
    response = llm_with_structured_output.invoke(prompt)

    # AI response
    print(f"\nAgent: {response.response_message}\n")

    # Append AI response to messages
    messages.append(AIMessage(content=response.response_message))
    state["messages"] = messages

    if response.should_start_research:
        return Command(goto="run_deep_research", update={"research_topic": response.research_topic})
    
    return Command(goto="chatbot")
