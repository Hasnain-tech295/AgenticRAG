# Quick Start Guide

## Getting Started in 3 Steps

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Set Up Environment Variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your-openai-api-key-here
MODEL_NAME=gpt-3.5-turbo
TEMPERATURE=0.7
MAX_TOKENS=1000
CHROMA_DB_PATH=src/chroma_db
```

### Step 3: Run the Application

You need **two terminals** - one for backend, one for frontend:

#### Terminal 1: Start Backend Server

```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

**Output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

#### Terminal 2: Start Frontend

```bash
streamlit run frontend/streamlit_app.py
```

**Output:**
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

The Streamlit app will automatically open in your browser! 🎉

## Using the Application

### 1. Check Backend Status
- Look for the green "● Online" badge in the sidebar
- If it shows "Offline", make sure the backend server is running

### 2. Start Chatting
- Type your question in the chat input at the bottom
- Press Enter or click the send button
- Wait for the response (you'll see a "🤔 Thinking..." spinner)

### 3. View Metrics
The sidebar shows performance metrics:
- **Iterations**: How many reasoning steps the agent took
- **Tool Calls**: Number of tools used (calculator, RAG search, etc.)
- **Duration**: Processing time in seconds
- **Tokens**: OpenAI API tokens consumed
- **Search Queries**: List of searches performed
- **Tool Latencies**: Performance of each tool

### 4. New Conversation
Click "🆕 New Chat" to start fresh

## Architecture Overview

```
┌─────────────────────┐         HTTP Requests         ┌─────────────────────┐
│                     │ ──────────────────────────────>│                     │
│  Streamlit Frontend │                                │   FastAPI Backend   │
│   (Port 8501)       │<────────────────────────────── │    (Port 8000)      │
│                     │         JSON Responses         │                     │
└─────────────────────┘                                └─────────────────────┘
         │                                                       │
         │                                                       │
         │ Display UI                                           │ Process Logic
         │                                                       │
         v                                                       v
   ┌──────────┐                                           ┌──────────┐
   │  Browser │                                           │  Agent   │
   └──────────┘                                           │  + RAG   │
                                                          │ + OpenAI │
                                                          └──────────┘
```

## Available Endpoints

Once the backend is running, you can access:

- **API Root**: http://localhost:8000/
- **Health Check**: http://localhost:8000/health
- **Interactive API Docs**: http://localhost:8000/docs (Swagger UI)
- **Alternative Docs**: http://localhost:8000/redoc

## Testing the API Directly

You can test the backend API without the Streamlit frontend:

### Using cURL

```bash
# Health check
curl http://localhost:8000/health

# Chat request
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What is RAG?", "conversation_id": "test-123"}'
```

### Using Python requests

```python
import requests

# Health check
response = requests.get("http://localhost:8000/health")
print(response.json())

# Chat
response = requests.post(
    "http://localhost:8000/chat",
    json={
        "query": "What is RAG?",
        "conversation_id": "test-123"
    }
)
print(response.json())
```

## Common Issues & Solutions

### Issue: "Backend is not running"

**Solution**: Start the backend server first:
```bash
uvicorn backend.main:app --reload
```

### Issue: "Port already in use"

**Backend (8000):**
```bash
uvicorn backend.main:app --reload --port 8001
```
Then update `BACKEND_URL` in `frontend/streamlit_app.py` to `http://localhost:8001`

**Frontend (8501):**
```bash
streamlit run frontend/streamlit_app.py --server.port 8502
```

### Issue: "ModuleNotFoundError: No module named 'src'"

**Solution**: Make sure you're running commands from the project root directory where the `src/` folder exists.

### Issue: "OpenAI API key not found"

**Solution**: 
1. Create `.env` file in project root
2. Add: `OPENAI_API_KEY=your-key-here`
3. Restart both servers

### Issue: Connection timeout

**Solution**: The query might be complex. Wait a bit longer or check backend logs for errors.

## Next Steps

### 1. Add Documents to RAG System

```python
from src.rag.pipeline import RAGPipeline
from src.config.config import RagConfig

# Initialize RAG pipeline
rag = RAGPipeline(RagConfig())

# Add documents
documents = [
    {
        "content": "Your document content here...",
        "source": "document1.pdf",
        "title": "Important Document"
    },
    {
        "content": "More content...",
        "source": "document2.pdf",
        "title": "Another Document"
    }
]

rag.ingest_documents(documents)
```

### 2. Customize the Frontend

Edit `frontend/streamlit_app.py`:
- Change colors in the CSS section
- Add new metrics to the sidebar
- Modify the chat message display
- Add file upload functionality

### 3. Extend the Backend API

Edit `backend/main.py`:
- Add new endpoints
- Implement streaming responses
- Add authentication
- Create conversation history endpoints

### 4. Configure Agent Behavior

Edit `src/config/config.py`:
- Change model (gpt-4, gpt-3.5-turbo, etc.)
- Adjust temperature and max_tokens
- Enable/disable specific tools
- Modify max iterations

## Production Deployment

### Option 1: Docker (Recommended)

Create `docker-compose.yml`:
```yaml
version: '3.8'

services:
  backend:
    build: .
    command: uvicorn backend.main:app --host 0.0.0.0 --port 8000
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    
  frontend:
    build: .
    command: streamlit run frontend/streamlit_app.py --server.port 8501
    ports:
      - "8501:8501"
    depends_on:
      - backend
```

Run:
```bash
docker-compose up
```

### Option 2: Cloud Deployment

**Backend** (FastAPI):
- Deploy to: AWS Lambda, Google Cloud Run, Heroku, Railway
- Use: Gunicorn + Uvicorn workers

**Frontend** (Streamlit):
- Deploy to: Streamlit Cloud, Heroku, Railway
- Update `BACKEND_URL` to production backend URL

## Troubleshooting Tips

1. **Check logs**: Both servers print useful error messages
2. **Verify ports**: Make sure 8000 and 8501 are free
3. **Test backend first**: Use the `/health` endpoint
4. **Check .env file**: Ensure it's in the root directory
5. **Restart both servers**: After making changes

## Resources

- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **Streamlit Docs**: https://docs.streamlit.io/
- **OpenAI API**: https://platform.openai.com/docs/
- **ChromaDB**: https://docs.trychroma.com/

---

Need help? Open an issue on GitHub!
