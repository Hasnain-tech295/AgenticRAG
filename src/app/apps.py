
from agents.agent import Agent
from config.config import AgentConfig
from config.logger import setup_logger
from fastapi import FastAPI

# setting up logger 
app = FastAPI()
logger = setup_logger("agent")

agent = Agent(
    config=AgentConfig(),
    logger=logger
)

@app.get("/health")
def health():
    return {"status": "ok"}
