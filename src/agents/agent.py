import os
from openai import OpenAI
from dotenv import load_dotenv
from config.config import AgentConfig
from utils.tools import tool_map, tools
from utils.metrics import AgentMetrics
from utils.ctx_manager import ContextWindowManager, ConversationManager
from datetime import datetime

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
openai_base_url = os.getenv("OPENAI_BASE_URL")

client = OpenAI(
    api_key=openai_api_key,
    base_url=openai_base_url
)

class Agent:
    def __init__(self, config: AgentConfig = AgentConfig()):
        self.model = config.model
        self.max_iterations = config.max_iterations
        self.max_tokens = config.max_tokens_per_call
        self.temperature = config.temperature
        self.max_context_tokens = config.max_context_tokens
        self.allowed_tools = [
            tool for tool in tools 
            if tool["function"]["name"] in config.allowed_tools
        ]
            
        self.require_approval = config.require_approval
        
    def _execute(self, query: str, conversation_id: str):
        metrics = AgentMetrics()
        metrics.start_time = datetime.now()
        
        messages = ConversationManager().get_or_create(conversation_id=conversation_id)
        messages.append({"role": "user", "content": query})
        
        
        for iteration in range(self.max_iterations):
            
            metrics.iterations = iteration + 1
            print(f"\n--- Iteration {iteration + 1}/ {self.max_iterations}")
               
            # Truncate messages 
            messages = ContextWindowManager().truncate_messages(messages=messages, max_tokens=3000)
            print(f"📝 Context: {ContextWindowManager().count_tokens(messages)} tokens, {len(messages)} messages")
            
            try:  
                response = client.chat.completions.create(
                    model=self.model,
                    temperature=self.temperature,
                    tools=self.allowed_tools,
                    tool_choice="auto",
                    messages=messages,
                    max_tokens=self.max_tokens
                )
                
                # Track tokens
                if hasattr(response, 'usage'):
                    metrics.tokens_used = response.usage.total_tokens
                    
                message = response.choices[0].message
                messages.append(message)
                
                # Checking for tool call in LLM response
                if not message.tool_calls:
                    # Finalizing metrics
                    metrics.end_time = datetime.now()
                    messages.append({"role": "assistant", "content": message.content})
                    return {
                        "Output": message.content,
                        "Metrics": metrics
                    }
                
                # Executing tool if tool call
                 
                for tool_call in message.tool_calls:
                    tool_name = tool_call.function.name
                    if tool_name not in [t["function"]["name"] for t in self.allowed_tools]:
                        raise RuntimeError(f"Tool {tool_name} not allowed")
                    
                    print(f" - Callng: {tool_name}")
                    
                    try:
                        func, input_model = tool_map[tool_name]
                        args = input_model.model_validate_json(tool_call.function.arguments)
                        
                        # Log tool call
                        metrics.log_tool_call(tool_name, args.model_dump())
                        
                        result = func(**args.model_dump())
                        
                        messages.append(
                            {
                                "role": "tool",
                                "tool_call_id": tool_call.id,
                                "content": result
                            }
                        )
                        
                        print(f"   ✓ Success")
                        
                    except Exception as e:
                        error_msg = f"Error executing {tool_name}: {str(e)}"
                        print(f"    ✗ {error_msg}")
                        metrics.log_error(error_msg)
                        
                        messages.append(
                            {
                                "role": "tool",
                                "tool_call_id": tool_call.id,
                                "content": error_msg
                            }
                        )
                        
            except Exception as e:
                error_msg = f"Error in iteration {iteration + 1}: {str(e)}"
                metrics.log_error(error_msg)
                print(error_msg)
        
        metrics.end_time = datetime.now()
        return metrics
                
metrics = AgentMetrics()
