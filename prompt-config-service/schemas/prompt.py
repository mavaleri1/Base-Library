"""Schemas for prompt generation operations."""

import uuid
from typing import Dict, Any

from pydantic import BaseModel, Field


class GeneratePromptRequest(BaseModel):
    """Schema for prompt generation request."""
    
    user_id: uuid.UUID = Field(..., description="User UUID")
    node_name: str = Field(..., min_length=1, description="LangGraph node name")
    context: Dict[str, Any] = Field(
        default_factory=dict,
        description="Context variables that override user settings"
    )


class GeneratePromptResponse(BaseModel):
    """Schema for prompt generation response."""
    
    prompt: str = Field(..., description="Generated prompt text")
    used_placeholders: Dict[str, str] = Field(
        ...,
        description="Dictionary of placeholders and their resolved values"
    )