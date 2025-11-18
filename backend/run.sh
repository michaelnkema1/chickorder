#!/bin/bash

# ChickOrder Backend Run Script

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}🐔 Starting ChickOrder Backend...${NC}"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Virtual environment not found. Creating one...${NC}"
    python3 -m venv venv
fi

# Activate virtual environment
echo -e "${GREEN}Activating virtual environment...${NC}"
source venv/bin/activate

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}⚠️  .env file not found!${NC}"
    echo -e "${YELLOW}Copying .env.example to .env...${NC}"
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo -e "${RED}⚠️  Please update .env with your configuration before running!${NC}"
    else
        echo -e "${RED}❌ .env.example not found!${NC}"
        exit 1
    fi
fi

# Install/update dependencies
echo -e "${GREEN}Checking dependencies...${NC}"
pip install -q -r requirements.txt

# Check if database is initialized (check for admin user)
echo -e "${GREEN}Checking database...${NC}"
python3 -c "from database import SessionLocal; from models import User; db = SessionLocal(); admin = db.query(User).filter(User.is_admin == True).first(); db.close(); exit(0 if admin else 1)" 2>/dev/null
if [ $? -ne 0 ]; then
    echo -e "${YELLOW}Database not initialized. Running init_db.py...${NC}"
    python3 init_db.py
fi

# Run the server
echo -e "${GREEN}🚀 Starting FastAPI server...${NC}"
echo -e "${GREEN}API will be available at: http://localhost:8000${NC}"
echo -e "${GREEN}API docs will be available at: http://localhost:8000/docs${NC}"
echo -e "${GREEN}Press Ctrl+C to stop the server${NC}"
echo ""

uvicorn main:app --reload --host 0.0.0.0 --port 8000

