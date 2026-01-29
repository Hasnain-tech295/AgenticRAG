# Architecture Documentation

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         User's Browser                           │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ HTTP (Port 8501)
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Streamlit Frontend                            │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  • Chat Interface                                         │  │
│  │  • Metrics Display                                        │  │
│  │  • Session Management                                     │  │
│  │  • Backend Health Check                                   │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ REST API (POST /chat)
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      FastAPI Backend                             │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  API Endpoints:                                           │  │
│  │  • POST /chat - Process queries                          │  │
│  │  • GET /health - Health check                            │  │
│  │  • GET /docs - Interactive API docs                      │  │
│  └──────────────────────────────────────────────────────────┘  │
│                             │                                    │
│                             ▼                                    │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                    Agent System                           │  │
│  │  ┌────────────────────────────────────────────────────┐  │  │
│  │  │  Reasoning Loop:                                   │  │  │
│  │  │  1. Analyze query                                  │  │  │
│  │  │  2. Select tools                                   │  │  │
│  │  │  3. Execute tools                                  │  │  │
│  │  │  4. Synthesize response                            │  │  │
│  │  └────────────────────────────────────────────────────┘  │  │
│  └──────────────────────────────────────────────────────────┘  │
│                             │                                    │
│              ┌──────────────┼──────────────┐                    │
│              │              │              │                     │
│              ▼              ▼              ▼                     │
│  ┌───────────────┐  ┌──────────┐  ┌─────────────┐             │
│  │  RAG Search   │  │Calculator│  │  Web Search │             │
│  │    Tool       │  │   Tool   │  │    Tool     │             │
│  └───────┬───────┘  └──────────┘  └─────────────┘             │
│          │                                                       │
│          ▼                                                       │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              RAG Pipeline                                 │  │
│  │  ┌────────────────┐  ┌──────────────┐  ┌──────────────┐ │  │
│  │  │  Document      │  │   Vector     │  │  Response    │ │  │
│  │  │  Indexing      │─>│  Retrieval   │─>│  Generation  │ │  │
│  │  └────────────────┘  └──────────────┘  └──────────────┘ │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      External Services                           │
│  ┌──────────────────┐              ┌──────────────────────┐     │
│  │   OpenAI API     │              │     ChromaDB         │     │
│  │   (GPT Models)   │              │  (Vector Storage)    │     │
│  └──────────────────┘              └──────────────────────┘     │
└─────────────────────────────────────────────────────────────────┘
```

## Request Flow

```
1. User Input
   │
   ├──> Streamlit captures message
   │
2. API Request
   │
   ├──> POST /chat to FastAPI backend
   │    {
   │      "query": "What is RAG?",
   │      "conversation_id": "abc-123"
   │    }
   │
3. Backend Processing
   │
   ├──> Agent receives query
   │    │
   │    ├──> Reasoning Loop
   │    │    │
   │    │    ├──> Analyze: Determine approach
   │    │    │
   │    │    ├──> Tool Selection: Choose RAG search
   │    │    │
   │    │    ├──> Tool Execution:
   │    │    │    • Query ChromaDB
   │    │    │    • Retrieve relevant docs
   │    │    │    • Calculate relevance
   │    │    │
   │    │    ├──> OpenAI API Call
   │    │    │    • Send context + query
   │    │    │    • Generate response
   │    │    │
   │    │    └──> Synthesize final answer
   │    │
   │    └──> Return result with metrics
   │
4. API Response
   │
   ├──> FastAPI returns JSON
   │    {
   │      "output": "RAG stands for...",
   │      "conversation_id": "abc-123",
   │      "metrics": {
   │        "iterations": 2,
   │        "tool_calls": 1,
   │        "duration_seconds": 1.5,
   │        "tokens_used": 350
   │      }
   │    }
   │
5. Frontend Display
   │
   └──> Streamlit renders message
        • Update chat history
        • Display metrics in sidebar
        • Show response to user
```

## Component Responsibilities

### Frontend (Streamlit)
- **UI/UX**: Renders chat interface
- **State Management**: Manages conversation history
- **API Client**: Makes HTTP requests to backend
- **Metrics Display**: Shows performance data
- **Error Handling**: Displays user-friendly error messages

### Backend (FastAPI)
- **API Endpoints**: Exposes RESTful API
- **Request Validation**: Validates incoming requests
- **Agent Orchestration**: Manages agent lifecycle
- **Response Formatting**: Structures API responses
- **CORS Handling**: Manages cross-origin requests
- **Logging**: Records all operations

### Agent System
- **Query Analysis**: Understands user intent
- **Tool Selection**: Chooses appropriate tools
- **Reasoning Loop**: Iteratively solves problems
- **Context Management**: Maintains conversation state
- **Metrics Collection**: Tracks performance

### RAG Pipeline
- **Document Indexing**: Processes and stores documents
- **Vector Search**: Finds relevant information
- **Context Retrieval**: Fetches matching documents
- **Response Generation**: Creates informed answers

## Data Flow

### Chat Request
```
Frontend → Backend → Agent → Tools → OpenAI → Agent → Backend → Frontend
```

### Document Ingestion
```
Documents → Indexer → Embeddings → ChromaDB
```

### RAG Search
```
Query → Embedding → ChromaDB Search → Retrieved Docs → Context
```

## Scalability Considerations

### Horizontal Scaling

**Backend**:
- Multiple FastAPI instances behind load balancer
- Stateless design allows easy replication
- Shared ChromaDB or distributed vector DB

**Frontend**:
- Multiple Streamlit instances
- Session state in external store (Redis)
- Load balancing with sticky sessions

### Vertical Scaling

- Increase worker count in Uvicorn
- Optimize ChromaDB index size
- Use faster embedding models
- Cache frequent queries

## Security Architecture

```
┌─────────────────────────────────────────┐
│          Security Layers                 │
├─────────────────────────────────────────┤
│  1. API Authentication (Future)          │
│     • JWT tokens                         │
│     • API keys                           │
├─────────────────────────────────────────┤
│  2. Rate Limiting                        │
│     • Per-user limits                    │
│     • Global limits                      │
├─────────────────────────────────────────┤
│  3. Input Validation                     │
│     • Pydantic models                    │
│     • SQL injection prevention           │
├─────────────────────────────────────────┤
│  4. CORS Configuration                   │
│     • Allowed origins                    │
│     • Allowed methods                    │
├─────────────────────────────────────────┤
│  5. Environment Variables                │
│     • Secret management                  │
│     • No hardcoded credentials           │
└─────────────────────────────────────────┘
```

## Deployment Options

### Development
- Local: Both servers on localhost
- Hot reload enabled
- Debug logging active

### Staging
- Backend: Cloud Run / Heroku
- Frontend: Streamlit Cloud
- Shared ChromaDB instance

### Production
- Backend: Kubernetes cluster
- Frontend: CDN + Streamlit Cloud
- ChromaDB: Managed service or cluster
- Load balancer + Auto-scaling
- Monitoring + Alerting

## Technology Stack

```
┌─────────────────────────────────────────┐
│             Frontend                     │
│  • Streamlit 1.31                       │
│  • Python requests library              │
│  • Session state management             │
└─────────────────────────────────────────┘
           ▲
           │ HTTP/REST
           ▼
┌─────────────────────────────────────────┐
│              Backend                     │
│  • FastAPI 0.109                        │
│  • Uvicorn ASGI server                  │
│  • Pydantic validation                  │
└─────────────────────────────────────────┘
           ▲
           │
           ▼
┌─────────────────────────────────────────┐
│            Core Logic                    │
│  • OpenAI GPT models                    │
│  • ChromaDB 0.4.22                      │
│  • Custom RAG pipeline                  │
│  • Agent system                         │
└─────────────────────────────────────────┘
```

## Performance Metrics

### Monitored Metrics
- **Iterations**: Reasoning steps taken
- **Tool Calls**: Number of tool invocations
- **Duration**: Total processing time
- **Tokens**: OpenAI API token usage
- **Latency**: Per-tool execution time

### Optimization Targets
- Query response time: < 3 seconds
- Tool selection accuracy: > 90%
- Context retrieval relevance: > 80%
- Token efficiency: < 500 tokens/query

## Future Enhancements

1. **Streaming Responses**: Real-time token streaming
2. **Authentication**: User accounts and sessions
3. **Conversation History**: Persistent storage
4. **Multi-tenancy**: Isolated user data
5. **Advanced RAG**: Hybrid search, reranking
6. **Observability**: Detailed metrics and tracing
