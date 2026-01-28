
from agents.agent import Agent
from config.config import AgentConfig

if __name__ == "__main__":
    config = AgentConfig(
        model="openai/gpt-4o-mini",
        max_iterations=3,
        max_tokens_per_call=256,
        temperature=0.7,
        allowed_tools=["calculator"],
    )
    
    agent = Agent(config)
    
    result = agent.run(
        query="What is 2 + 2?",
        conversation_id="test-123"
    )
    
    print("=" * 20 + " FINAL RESPONSE " + "=" * 20)
    print(result["output"])
    print("=" * 20 + " METRICS " + "=" * 20)
    print(result["metrics"])