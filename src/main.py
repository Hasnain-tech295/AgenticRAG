import os
from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Dict, Any, Optional
import tiktoken
from pathlib import Path
import json
from datetime import datetime
from tavily import TavilyClient

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
openai_base_url = os.getenv("OPENAI_BASE_URL")

client = OpenAI(
    api_key=openai_api_key,
    base_url=openai_base_url
)

# --------------------------------------------------------
# PYDANTIC MODELS for Tool args
# --------------------------------------------------------
class CalculatorParam(BaseModel):
    expression: str = Field(description="mathematical expression")

# --------------------------------------------------------
# TOOLS
# --------------------------------------------------------
def calculator(expression: str) -> str:
    """Calculate mathematical expression"""
    try:
        return str(eval(expression))
    
    except:
        return "Invalid Expression"
    
# ---------------------------------------------------------
# TOOLS SCHEMA
# ---------------------------------------------------------
tools = [
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "Use this tool to compute mathematical expression",
            "parameters": CalculatorParam.model_json_schema()
        }
    }
]

tool_map = {
    "calculator": (calculator, CalculatorParam)
}

messages = [
            {
                "role": "user",
                "content": "What is 2*4/12+1-9^2"
            }
        ]

for i in range(3):
    response = client.chat.completions.create(
        model="openai/gpt-4o-mini",
        messages=messages,
        max_tokens=20,
        tools=tools,
        tool_choice="auto",
        temperature=0.7
    )

    message = response.choices[0].message
    messages.append(message)
    
    if not message.tool_calls:
        print("="*20+"Final Response"+"="*20)
        print(message.content)
    
    
    for tool_call in message.tool_calls:
        tool_name = tool_call.function.name
        print(f"- Calling: {tool_name}")
        
        try:
            func, input_model = tool_map[tool_name]
            args = input_model.model_validate_json(tool_call.function.arguments)
            
            result = func(**args.model_dump())
            
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result
            })
        except Exception as e:
            error_msg = str(e)
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": error_msg
            })
            
print("Max iteration reached")
            

