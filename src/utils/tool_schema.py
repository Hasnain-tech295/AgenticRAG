"""Tools schema definition"""
from pydantic import BaseModel, Field

class Tool:
    def __init__(self, *, name: str, description: str, schema: BaseModel):
        self.name = name
        self.description = description
        self.schema = schema.model_json_schema()
        
        self.openai_tool_schema = {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.schema
            }
        }
        