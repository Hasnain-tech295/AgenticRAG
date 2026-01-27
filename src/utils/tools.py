# --------------------------------------------------------
# PYDANTIC MODELS for Tool args
# --------------------------------------------------------
from pydantic import BaseModel, Field
from utils.tool_schema import Tool

class CalculatorParam(BaseModel):
    expression: str = Field(description="mathematical expression")
    
class WebSearchParam(BaseModel):
    query: str
# --------------------------------------------------------
# TOOLS
# --------------------------------------------------------
def calculator(expression: str) -> str:
    """Calculate mathematical expression"""
    try:
        return str(eval(expression))
    
    except:
        return "Invalid Expression"
    
def web_search(query) -> str:
    """Web search not implemented yet."""
    pass
# ----------------------------------------------------------
# OPENAI TOOL Schema
# ----------------------------------------------------------
    
calculator_tool = Tool(
    name="calculator",
    description="Tool for mathematical calculation",
    schema=CalculatorParam
).openai_tool_schema

web_search_tool = Tool(
    name="web_search",
    description="Use this tool to search web for factual or upto date info.",
    schema=WebSearchParam
).openai_tool_schema

tools = [
    calculator_tool,
    web_search_tool,
]

tool_map = {
    "calculator": (calculator, CalculatorParam),
    "web_search": (web_search, WebSearchParam)
}