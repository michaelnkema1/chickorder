@echo off
REM ChickOrder Backend Run Script for Windows

echo 🐔 Starting ChickOrder Backend...

REM Check if virtual environment exists
if not exist "venv" (
    echo Virtual environment not found. Creating one...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if .env file exists
if not exist ".env" (
    echo ⚠️  .env file not found!
    echo Copying .env.example to .env...
    if exist ".env.example" (
        copy .env.example .env
        echo ⚠️  Please update .env with your configuration before running!
    ) else (
        echo ❌ .env.example not found!
        exit /b 1
    )
)

REM Install/update dependencies
echo Checking dependencies...
pip install -q -r requirements.txt

REM Check if database is initialized
echo Checking database...
python -c "from database import SessionLocal; from models import User; db = SessionLocal(); admin = db.query(User).filter(User.is_admin == True).first(); db.close(); exit(0 if admin else 1)" 2>nul
if errorlevel 1 (
    echo Database not initialized. Running init_db.py...
    python init_db.py
)

REM Run the server
echo.
echo 🚀 Starting FastAPI server...
echo API will be available at: http://localhost:8000
echo API docs will be available at: http://localhost:8000/docs
echo Press Ctrl+C to stop the server
echo.

uvicorn main:app --reload --host 0.0.0.0 --port 8000

