@echo off
echo ========================================
echo    Agentic RAG - Startup Script
echo ========================================
echo.

REM Check if .env file exists
if not exist .env (
    echo Error: .env file not found!
    echo Please create a .env file with your OPENAI_API_KEY
    echo Example:
    echo   OPENAI_API_KEY=your-key-here
    echo   MODEL_NAME=gpt-3.5-turbo
    pause
    exit /b 1
)

echo [OK] .env file found
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python not found in PATH
    pause
    exit /b 1
)

echo [OK] Python found
echo.

REM Check if required packages are installed
python -c "import fastapi, uvicorn, streamlit" 2>nul
if errorlevel 1 (
    echo Error: Required packages not installed
    echo Run: pip install -r requirements.txt
    pause
    exit /b 1
)

echo [OK] Dependencies installed
echo.

REM Start backend in new window
echo Starting FastAPI Backend on port 8000...
start "Backend Server" cmd /k "uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000"

REM Wait for backend to start
timeout /t 3 /nobreak >nul

REM Check if backend is running
curl -s http://localhost:8000/health >nul 2>&1
if errorlevel 1 (
    echo Warning: Backend might not be fully started yet
) else (
    echo [OK] Backend started successfully
    echo   API: http://localhost:8000
    echo   Docs: http://localhost:8000/docs
)
echo.

REM Start frontend in new window
echo Starting Streamlit Frontend on port 8501...
start "Frontend Server" cmd /k "streamlit run frontend/streamlit_app.py"

timeout /t 3 /nobreak >nul

echo.
echo ========================================
echo   Both servers are starting!
echo ========================================
echo.
echo Backend: http://localhost:8000
echo Frontend: http://localhost:8501
echo API Docs: http://localhost:8000/docs
echo.
echo Close the terminal windows to stop the servers
echo.
pause
