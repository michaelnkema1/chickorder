#!/bin/bash

# ChickOrder Frontend Run Script

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}🐔 Starting ChickOrder Frontend...${NC}"

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo -e "${YELLOW}Dependencies not found. Installing...${NC}"
    npm install
fi

# Run the development server
echo -e "${GREEN}🚀 Starting Vite development server...${NC}"
echo -e "${GREEN}Frontend will be available at: http://localhost:3000${NC}"
echo -e "${GREEN}Press Ctrl+C to stop the server${NC}"
echo ""

npm run dev

