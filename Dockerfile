FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the backend contents directly to /app so 'app' is the top-level package
COPY backend/ ./
COPY frontend/ ./frontend/

EXPOSE 8000

# Start uvicorn from the /app directory
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]


