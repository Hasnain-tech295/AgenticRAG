
from ..agents.agent import Agent
from ..config.config import AgentConfig
from ..config.logger import setup_logger
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uuid

# setting up logger
app = FastAPI()
logger = setup_logger("agent")

agent = Agent(
    config=AgentConfig(),
    logger=logger
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/chat", response_class=HTMLResponse)
async def chat(request: Request, query: str = Form(...), conversation_id: str = Form(None)):
    if not conversation_id:
        conversation_id = str(uuid.uuid4())

    try:
        result = agent.run(query, conversation_id)
        response = result.get("output", "No response generated")
        metrics = result.get("metrics", {})
    except Exception as e:
        response = f"Error: {str(e)}"
        metrics = {}

    return templates.TemplateResponse("index.html", {
        "request": request,
        "query": query,
        "response": response,
        "conversation_id": conversation_id,
        "metrics": metrics
    })
