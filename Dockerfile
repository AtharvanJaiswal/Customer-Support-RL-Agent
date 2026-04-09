FROM python:3.10

WORKDIR /app

RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

# HF Spaces requires port 7860; server.app:app is the FastAPI app
CMD ["uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "7860"]