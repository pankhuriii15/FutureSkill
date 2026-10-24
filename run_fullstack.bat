@echo off
echo ======================================================================
echo Multimodal Construction Intelligence Platform
echo Starting FastAPI Backend and React + Vite Frontend...
echo ======================================================================

start "FastAPI Backend" cmd /k ".\venv\Scripts\activate && uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload"
timeout /t 2 /nobreak >nul
start "React Vite Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo Platform launched successfully!
echo Backend API Docs: http://127.0.0.1:8000/docs
echo Frontend Web UI:  http://127.0.0.1:5173
echo ======================================================================
pause
