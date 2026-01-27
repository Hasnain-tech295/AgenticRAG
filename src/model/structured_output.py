from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class WebSearchOutput(BaseModel):
    """WEb search result"""
    title: str = Field(description="Title of the web search results.")
    content: str = Field(description="Content of each web search request result")
    sources: List[str] = Field("URLs or source of the web search results")
    
class CalculatorOutput(BaseModel):
    """Calculator tool result"""
    query: str = Field(description="Query that user asked")
    output: str = Field(description="tool output")