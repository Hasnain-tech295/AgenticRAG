import tiktoken
from typing import Dict, List
class ContextWindowManager:
    def count_tokens(self, messages: list, model: str = "gpt-4o-mini") -> int:
        """Count tokens in messages"""
        try:
            encoding = tiktoken.encoding_for_model(model)
        except KeyError:
            encoding = tiktoken.get_encoding("cl100k_base")
        
        num_tokens = 0
        for message in messages:
            # Count tokens for each message
            num_tokens += 4  # Every message has overhead
            
            if isinstance(message, dict):
                for key, value in message.items():
                    if value:
                        num_tokens += len(encoding.encode(str(value)))
            else:
                # Handle ChatCompletionMessage objects
                if hasattr(message, 'content') and message.content:
                    num_tokens += len(encoding.encode(message.content))
                if hasattr(message, 'tool_calls') and message.tool_calls:
                    num_tokens += len(encoding.encode(str(message.tool_calls)))
        
        return num_tokens


    def truncate_messages(self, messages: list, max_tokens: int = 3000) -> list:
        """Truncate messages to fit token limit"""
        while self.count_tokens(messages) > max_tokens and len(messages) > 2:
            # Keep system message (index 0) and remove oldest
            messages.pop(1)
            print(f"⚠️  Token limit reached, removed old message")
        
        return messages

class ConversationManager:
    """Manage multi-turn conversation"""
    def __init__(self):
        self.conversations: Dict[str, List[dict]] = {}
        
    def get_or_create(self, conversation_id: str) -> List[dict]:
        """Get conversation history"""
        if conversation_id not in self.conversations:
            self.conversations[conversation_id] = [
                {
                    "role": "system",
                    "content": "You are a helpful assistant"
                }
            ]
            
        return self.conversations[conversation_id]
    
    # Add other stuff to like add message, clear etc