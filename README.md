# AgenticRAG

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green.svg)](https://fastapi.tiangolo.com/)

An intelligent Retrieval-Augmented Generation (RAG) system with agentic capabilities, built with FastAPI and powered by OpenAI's language models and ChromaDB for vector storage.

## 🚀 Features

- **Agentic RAG Pipeline**: Intelligent document retrieval and response generation
- **FastAPI Backend**: High-performance REST API with automatic OpenAPI documentation
- **ChromaDB Integration**: Persistent vector database for efficient document indexing and retrieval
- **OpenAI Integration**: Leverages GPT models for natural language understanding and generation
- **Structured Output**: Consistent response formatting for better API consumption
- **Configurable**: Environment-based configuration for easy deployment
- **Logging**: Comprehensive logging setup for monitoring and debugging
- **Cost Tracking**: Built-in utilities for monitoring API usage costs
- **Metrics Collection**: Query metrics and performance tracking

## 📋 Table of Contents

- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Project Structure](#project-structure)
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
   ```bash
   export OPENAI_API_KEY="your-openai-api-key-here"
   # Optional: Configure other settings
   export MODEL_NAME="gpt-3.5-turbo"
   export TEMPERATURE="0.7"
   export MAX_TOKENS="1000"
   export CHROMA_DB_PATH="src/chroma_db"
   ```

## ⚙️ Configuration

The application uses environment variables for configuration. Create a `.env` file in the root directory:

```env
OPENAI_API_KEY=your-openai-api-key-here
MODEL_NAME=gpt-3.5-turbo
TEMPERATURE=0.7
MAX_TOKENS=1000
CHROMA_DB_PATH=src/chroma_db
```

### Configuration Options

- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `MODEL_NAME`: OpenAI model to use (default: gpt-3.5-turbo)
- `TEMPERATURE`: Model temperature for response creativity (default: 0.7)
- `MAX_TOKENS`: Maximum tokens in model response (default: 1000)
- `CHROMA_DB_PATH`: Path to ChromaDB storage (default: src/chroma_db)

## 🚀 Usage

### Running the Application

Start the FastAPI server:

```bash
python src/main.py
```

The API will be available at `http://localhost:8000`

### API Documentation

Once running, visit `http://localhost:8000/docs` for interactive API documentation powered by Swagger UI.

## 📡 API Endpoints

### GET /
Returns a welcome message.

**Response:**
```json
{
  "message": "Welcome to AgenticRAG"
}
```

### POST /query
Processes a query through the RAG pipeline.

**Request Body:**
```json
{
  "query": "Your question here"
}
```

**Response:**
```json
{
  "response": "Generated response based on retrieved documents"
}
```

## 🏗️ Project Structure

```
AgenticRAG/
├── src/
│   ├── main.py                 # Application entry point
│   ├── app/
│   │   └── apps.py            # FastAPI application setup
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
├── LICENSE                    # MIT License
└── .gitignore                 # Git ignore rules
```

## 🧪 Development

### Running Tests

```bash
# Add test commands when tests are implemented
pytest
```

### Code Quality

```bash
# Linting
flake8 src/

# Formatting
black src/
```

### Adding New Features

1. Create a new branch: `git checkout -b feature/your-feature-name`
2. Implement your changes
3. Add tests if applicable
4. Update documentation
5. Submit a pull request

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

- [FastAPI](https://fastapi.tiangolo.com/) - Modern, fast web framework for building APIs
- [ChromaDB](https://www.trychroma.com/) - Vector database for AI applications
- [OpenAI](https://openai.com/) - AI models and API

## 📞 Support

If you have any questions or need help, please open an issue on GitHub or contact the maintainers.

---

**Note:** This project is currently in active development. Some features marked with TODO comments are not yet implemented.