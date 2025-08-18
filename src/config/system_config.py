"""
System configuration for the Deep Research Agent.

This module defines the configuration system that manages all settings for the research
workflow, including model selections, research parameters, and system behavior.

Inspired by: https://github.com/langchain-ai/open_deep_research/blob/main/src/open_deep_research/configuration.py
Adapted and rewritten for this specific use case.
"""

import os
from enum import Enum
from typing import Any, Optional, Dict
from pydantic import BaseModel, Field
from langchain_core.runnables import RunnableConfig


class SearchEngine(Enum):
    """Available search engine options for web research."""
    TAVILY = "tavily"
    NONE = "none"


class Configuration(BaseModel):
    """
    Main configuration class for the Deep Research Agent.
    
    This class manages all configuration parameters including model selections,
    research behavior settings, and system preferences. Configuration values
    are loaded with priority: User Input > Environment Variables > Defaults.
    """

    # Chatbot Model
    chatbot_model: str = Field(
        default="gpt-4.1-mini",
        metadata={
            "x_oap_ui_config": {
                "type": "text",
                "default": "openai:gpt-4.1-mini",
                "description": "Model for the chatbot"
            }
        }
    )

    # User Topic Clarification Model
    user_topic_clarification_model: str = Field(
        default="gpt-4.1-mini",
        metadata={
            "x_oap_ui_config": {
                "type": "text",
                "default": "openai:gpt-4.1-mini",
                "description": "Model for clarifying the user's research topic"
            }
        }
    )

    # Research Brief Generation Model
    research_brief_generation_model: str = Field(
        default="gpt-4.1-mini",
        metadata={
            "x_oap_ui_config": {
                "type": "text",
                "default": "openai:gpt-4.1-mini",
                "description": "Model for generating a research brief"
            }
        }
    )

    # Query Generation Model
    query_generation_model: str = Field(
        default="gpt-4.1-mini",
        metadata={
            "x_oap_ui_config": {
                "type": "text",
                "default": "openai:gpt-4.1-mini",
                "description": "Model for generating search queries"
            }
        }
    )

    # Summarization Model
    summarization_model: str = Field(
        default="gpt-4.1-mini",
        metadata={
            "x_oap_ui_config": {
                "type": "text",
                "default": "openai:gpt-4.1-mini",
                "description": "Model for summarizing search results"
            }
        }
    )

    # Reflection Model
    reflection_model: str = Field(
        default="o4-mini",
        metadata={
            "x_oap_ui_config": {
                "type": "text",
                "default": "openai:o4-mini",
                "description": "Model for reflecting on summaries"
            }
        }
    )

    # Final Report Model
    final_report_model: str = Field(
        default="gpt-4.1",
        metadata={
            "x_oap_ui_config": {
                "type": "text",
                "default": "openai:gpt-4.1",
                "description": "Model for writing the final report"
            }
        }
    )

    # Reasoning Effort
    reasoning_effort: str = Field(
        default="medium",
        metadata={
            "x_oap_ui_config": {
                "type": "select",
                "default": "medium",
                "description": "Reasoning effort for the reflection model",
                "options": [
                    {"label": "Low", "value": "low"},
                    {"label": "Medium", "value": "medium"},
                    {"label": "High", "value": "high"}
                ]
            }
        }
    )

    # Research Units for Initial Search
    research_units_initial: int = Field(
        default=3,
        metadata={
            "x_oap_ui_config": {
                "type": "slider",
                "default": 3,
                "min": 1,
                "max": 10,
                "description": "Number of research units to spawn for initial search queries."
            }
        }
    )

    # Research Units for Reflection
    research_units_reflection: int = Field(
        default=2,
        metadata={
            "x_oap_ui_config": {
                "type": "slider",
                "default": 2,
                "min": 1,
                "max": 5,
                "description": "Number of research units to spawn at each reflection loop."
            }
        }
    )

    # Allow Clarification
    allow_clarification: bool = Field(
        default=True,
        metadata={
            "x_oap_ui_config": {
                "type": "boolean",
                "default": True,
                "description": "Whether to allow the researcher to ask the user clarifying questions before starting research"
            }
        }
    )

    # Allow Reflection
    allow_reflection: bool = Field(
        default=True,
        metadata={
            "x_oap_ui_config": {
                "type": "boolean",
                "default": True,
                "description": "Whether to allow the researcher to reflect on the summaries and generate follow-up queries."
            }
        }
    )

    # Reflection Loops
    reflection_loops: int = Field(
        default=1,
        metadata={
            "x_oap_ui_config": {
                "type": "slider",
                "default": 1,
                "min": 1,
                "max": 5,
                "step": 1,
                "description": "Maximum number of reflection loops to allow the researcher to conduct."
            }
        }
    )

    # Search API
    search_api: SearchEngine = Field(
        default=SearchEngine.TAVILY,
        metadata={
            "x_oap_ui_config": {
                "type": "select",
                "default": "tavily",
                "description": "Search API engine to use for research.",
                "options": [
                    {"label": "Tavily", "value": SearchEngine.TAVILY.value},
                    {"label": "None", "value": SearchEngine.NONE.value}
                ]
            }
        }
    )


    @classmethod
    def from_runnable_config(cls, config: Optional[RunnableConfig] = None) -> "Configuration":
        """
        Create a Configuration instance from a RunnableConfig.
        
        Configuration values are loaded with the following priority:
        1. User input from configurable
        2. Environment variables
        3. Default values
        
        Args:
            config: Optional RunnableConfig containing user preferences
            
        Returns:
            Configuration: Configured instance with resolved values
        """
        configurable = config.get("configurable", {}) if config else {}
        field_names = list(cls.model_fields.keys())
        values: Dict[str, Any] = {}
        
        for field_name in field_names:
            # Priority 1: User input from configurable
            if field_name in configurable:
                values[field_name] = configurable[field_name]
            
            # Priority 2: Environment variables
            elif os.environ.get(field_name.upper()):
                values[field_name] = os.environ.get(field_name.upper())
            
            # Priority 3: Defaults handled by Pydantic
        return cls(**{k: v for k, v in values.items() if v is not None})

    class Config:
        """Pydantic configuration settings."""
        arbitrary_types_allowed = True