#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}   Agentic RAG - Startup Script${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo -e "${RED}Error: .env file not found!${NC}"
    echo "Please create a .env file with your OPENAI_API_KEY"
    echo "Example:"
    echo "  OPENAI_API_KEY=your-key-here"
    echo "  MODEL_NAME=gpt-3.5-turbo"
    exit 1
fi

echo -e "${GREEN}✓ .env file found${NC}"

# Check if required packages are installed
echo "Checking dependencies..."
python -c "import fastapi, uvicorn, streamlit" 2>/dev/null
if [ $? -ne 0 ]; then
    echo -e "${RED}Error: Required packages not installed${NC}"
    echo "Run: pip install -r requirements.txt"
    exit 1
fi
echo -e "${GREEN}✓ Dependencies installed${NC}"
echo ""

# Function to cleanup background processes
cleanup() {
    echo ""
    echo -e "${BLUE}Shutting down servers...${NC}"
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    exit 0
}

# Set trap to cleanup on exit
trap cleanup SIGINT SIGTERM

# Start backend
echo -e "${BLUE}Starting FastAPI Backend on port 8000...${NC}"
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000 > backend.log 2>&1 &
BACKEND_PID=$!

# Wait for backend to start
echo "Waiting for backend to start..."
sleep 3

# Check if backend is running
curl -s http://localhost:8000/health > /dev/null
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Backend started successfully${NC}"
    echo "  API: http://localhost:8000"
    echo "  Docs: http://localhost:8000/docs"
else
    echo -e "${RED}✗ Backend failed to start. Check backend.log${NC}"
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi
echo ""

# Start frontend
echo -e "${BLUE}Starting Streamlit Frontend on port 8501...${NC}"
streamlit run frontend/streamlit_app.py > frontend.log 2>&1 &
FRONTEND_PID=$!

echo "Waiting for frontend to start..."
sleep 3

echo -e "${GREEN}✓ Frontend started successfully${NC}"
echo "  URL: http://localhost:8501"
echo ""

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  Both servers are running!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "Backend logs: tail -f backend.log"
echo "Frontend logs: tail -f frontend.log"
echo ""
echo -e "${BLUE}Press Ctrl+C to stop both servers${NC}"
echo ""

# Wait for user interrupt
wait
