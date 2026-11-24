@echo off
cd /d "%~dp0"

python -m pip show uvicorn >nul 2>&1
if errorlevel 1 (
    echo Installing UrbanTwin dependencies...
    python -m pip install -r requirements.txt
)

echo Starting UrbanTwin at http://127.0.0.1:8000
start "" "http://127.0.0.1:8000"
python -m uvicorn main:app --host 127.0.0.1 --port 8000
