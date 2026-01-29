# AgenticRAG

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green.svg)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.31-red.svg)](https://streamlit.io/)

An intelligent Retrieval-Augmented Generation (RAG) system with agentic capabilities, built with **FastAPI backend** and **Streamlit frontend**, powered by OpenAI's language models and ChromaDB for vector storage.

## 🏗️ Architecture

This project uses a **decoupled architecture**:
- **Backend**: FastAPI server (port 8000) handles all RAG logic, agent processing, and OpenAI interactions
- **Frontend**: Streamlit app (port 8501) provides an interactive chat interface
- **Communication**: REST API between frontend and backend

## 🚀 Features

### Backend (FastAPI)
- **RESTful API**: Clean API endpoints for chat interactions
- **Agentic RAG Pipeline**: Intelligent document retrieval and response generation
- **ChromaDB Integration**: Persistent vector database for efficient document indexing
- **OpenAI Integration**: Leverages GPT models for natural language understanding
- **Structured Output**: Consistent response formatting with metrics
- **Error Handling**: Comprehensive error handling and logging
- **CORS Support**: Ready for deployment with proper CORS configuration

### Frontend (Streamlit)
- **Modern Chat Interface**: Clean, responsive UI with color-coded messages
- **Real-time Metrics**: Display of iterations, tool calls, tokens, and latencies
- **Conversation Management**: Persistent conversation history within sessions
- **Backend Health Check**: Monitor backend status in real-time
- **New Chat Function**: Easy conversation reset
- **Status Indicators**: Visual feedback for system status and errors

## 📋 Table of Contents

- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [API Documentation](#api-documentation)
- [Development](#development)
- [Contributing](#contributing)
- [License](#license)

## 🛠️ Installation

### Prerequisites

- Python 3.8 or higher
- OpenAI API key

### Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/AgenticRAG.git
   cd AgenticRAG
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   Create a `.env` file in the root directory:
   ```env
   OPENAI_API_KEY=your-openai-api-key-here
   MODEL_NAME=gpt-3.5-turbo
   TEMPERATURE=0.7
   MAX_TOKENS=1000
   CHROMA_DB_PATH=src/chroma_db
   ```

## ⚙️ Configuration

The application uses environment variables for configuration.

### Configuration Options

- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `MODEL_NAME`: OpenAI model to use (default: gpt-3.5-turbo)
- `TEMPERATURE`: Model temperature for response creativity (default: 0.7)
- `MAX_TOKENS`: Maximum tokens in model response (default: 1000)
- `CHROMA_DB_PATH`: Path to ChromaDB storage (default: src/chroma_db)

## 🚀 Usage

### Starting the Application

You need to run **both** the backend and frontend:

#### 1. Start the Backend Server

```bash
# From project root
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

The backend API will be available at:
- API: http://localhost:8000
- API Documentation: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

#### 2. Start the Frontend (in a new terminal)

```bash
# From project root
streamlit run frontend/streamlit_app.py
```

The Streamlit app will automatically open in your browser at http://localhost:8501

### Using the Chat Interface

1. **Check Backend Status**: Ensure the green "Online" badge appears in the sidebar
2. **Start Chatting**: Type your question in the chat input at the bottom
3. **View Responses**: The assistant will process your query via the backend
4. **Monitor Metrics**: Track performance metrics in the sidebar:
   - Iterations taken
   - Tool calls made
   - Processing time
   - Tokens used
   - Search queries executed
   - Tool latencies
5. **New Chat**: Click "🆕 New Chat" to start a fresh conversation
6. **Refresh Status**: Use "🔄 Refresh Backend Status" if connection issues occur

## 🏗️ Project Structure

```
AgenticRAG/
├── backend/
│   └── main.py                # FastAPI application with API endpoints
├── frontend/
│   └── streamlit_app.py       # Streamlit chat interface
├── src/
│   ├── __init__.py
│   ├── config/
│   │   ├── config.py          # Configuration management
│   │   └── logger.py          # Logging configuration
│   ├── rag/
│   │   ├── pipeline.py        # Main RAG pipeline orchestration
│   │   ├── index.py           # Document indexing logic
│   │   ├── retriever.py       # Document retrieval logic
│   │   └── schemas.py         # Data schemas
│   ├── agents/
│   │   └── agent.py           # Agent logic for response generation
│   ├── model/
│   │   └── structured_output.py # Response formatting
│   ├── utils/
│   │   ├── cost_tracker.py    # API cost tracking
│   │   ├── metrics.py         # Performance metrics
│   │   ├── tools.py           # Utility tools
│   │   ├── tool_schema.py     # Tool schemas
│   │   └── ctx_manager.py     # Context management
│   └── chroma_db/             # ChromaDB storage
├── requirements.txt           # Python dependencies
├── README.md                  # This file
├── QUICKSTART.md             # Quick start guide
├── LICENSE                    # MIT License
└── .gitignore                # Git ignore rules
```

## 📡 API Documentation

### Endpoints

#### `GET /`
Root endpoint with API information

#### `GET /health`
Health check endpoint
```json
{
  "status": "healthy",
  "timestamp": "2024-01-30T10:00:00"
}
```

#### `POST /chat`
Process a chat query
```json
// Request
{
  "query": "What is RAG?",
  "conversation_id": "optional-conversation-id"
}

// Response
{
  "output": "RAG stands for...",
  "conversation_id": "abc123...",
  "metrics": {
    "iterations": 3,
    "tool_calls": 2,
    "duration_seconds": 1.5,
    "tokens_used": 450
  },
  "timestamp": "2024-01-30T10:00:00"
}
```

#### `POST /chat/stream` (Coming Soon)
Stream chat responses in real-time

#### `DELETE /conversation/{conversation_id}` (Coming Soon)
Delete a conversation

For interactive API documentation, visit: http://localhost:8000/docs

## 🧪 Development

### Running Tests

```bash
# Add test commands when tests are implemented
pytest
```

### Code Quality

```bash
# Linting
flake8 src/ backend/ frontend/

# Formatting
black src/ backend/ frontend/
```

### Adding New Features

1. **Backend**: Add endpoints in `backend/main.py`
2. **Frontend**: Modify UI in `frontend/streamlit_app.py`
3. **RAG Logic**: Update `src/` modules
4. Update documentation
5. Submit a pull request

### Development Mode

Run both servers with auto-reload:

```bash
# Terminal 1: Backend
uvicorn backend.main:app --reload

# Terminal 2: Frontend
streamlit run frontend/streamlit_app.py
```

### Custom Port Configuration

Backend:
```bash
uvicorn backend.main:app --reload --port 8001
```

Frontend (update BACKEND_URL in streamlit_app.py):
```bash
streamlit run frontend/streamlit_app.py --server.port 8502
```

## 🔒 Security Considerations

For production deployment:
1. Update CORS origins in `backend/main.py` to specific domains
2. Add authentication middleware
3. Use environment variables for sensitive configuration
4. Enable HTTPS
5. Implement rate limiting
6. Add request validation

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Modern, fast web framework
- [Streamlit](https://streamlit.io/) - Beautiful web apps in Python
- [ChromaDB](https://www.trychroma.com/) - Vector database for AI applications
- [OpenAI](https://openai.com/) - AI models and API

## 📞 Support

If you have any questions or need help, please open an issue on GitHub or contact the maintainers.

## 🔄 Recent Updates

- **Architecture Change**: Separated backend (FastAPI) and frontend (Streamlit) for better scalability
- **REST API**: Clean API design with proper endpoints and documentation
- **Health Monitoring**: Real-time backend status checking
- **Enhanced Error Handling**: Better error messages and connection status
- **Improved Deployment**: Independent backend and frontend deployment

---

**Note:** This project is currently in active development. Some features marked with "Coming Soon" are not yet implemented.
