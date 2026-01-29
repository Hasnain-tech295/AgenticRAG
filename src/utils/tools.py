# --------------------------------------------------------
# PYDANTIC MODELS for Tool args
# --------------------------------------------------------
from pydantic import BaseModel, Field
from utils.tool_schema import Tool
from rag.pipeline import RAGPipeline
from config.config import RagConfig

config = RagConfig()

rag_pipeline = RAGPipeline(config=config)

class CalculatorParam(BaseModel):
    expression: str = Field(description="mathematical expression")
    
class WebSearchParam(BaseModel):
    query: str
    
class RagSearchParam(BaseModel):
    query: str
    k: int = Field(default=5, ge=1, le=10)
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

def rag_search(query: str, k: int = 5) -> str:
    """Retrieve relevant documents for a query"""
    chunks = rag_pipeline.retrieve(query=query, top_k=k)
    
    context = "\n\n".join(
        f"[Source: {c['metadata'].get('source', 'unknown')}]\n{c['text']}"
        for c in chunks
    )
    
    return context

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

rag_search_tool = Tool(
    name="rag_search",
    description="Tool for rag search",
    schema=RagSearchParam
).openai_tool_schema

tools = [
    calculator_tool,
    web_search_tool,
    rag_search_tool
]

tool_map = {
    "calculator": (calculator, CalculatorParam),
    "web_search": (web_search, WebSearchParam),
    "rag_search": (rag_search, RagSearchParam)
}