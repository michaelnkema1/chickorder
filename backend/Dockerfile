FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Make the startup script executable
RUN chmod +x start.sh

# start.sh: runs alembic upgrade head, seeds the DB, then starts uvicorn
CMD ["./start.sh"]
