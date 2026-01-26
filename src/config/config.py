from pydantic import BaseModel, Field
from typing import List

class AgentConfig(BaseModel):
    """Agent configuration"""
    model: str = "openai/gpt-4o-mini"
    max_iterations: int = Field(default=5, ge=1, le=20)
    max_tokens_per_call: int = Field(default=500, ge=100, le=4000)
    max_context_tokens: int = Field(default=3000)
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    enable_streaming: bool = False
    require_approval: bool = False
    allowed_tools: List[str] = ["TavilySearch", "calculator"]