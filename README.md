# ROMI

## Features

- Upload CVs in PDF, DOCX, and image formats (PNG, JPG, JPEG) using a Strategy Pattern-based text extractor
- Match CVs against job descriptions using Sentence Transformer model
- Use ChromaDB for vector storage and retrieval
- Evaluate candidates using LLM (Gemini Flash 2.5)
- Automated system evaluation suite (accuracy, edge cases, cross-category confusion, hallucination detection, ranking quality) based on ground truth datasets

## Tech Stack

- FastAPI
- Sentence Transformers
- ChromaDB
- Ollama
- Docker
- GeminiApi

## Installation

copy .env.example to .env
then add your google AI Studio api key 
```bash
cp ./backend/.env.example ./backend/.env
```

```bash
sudo bash ./config.sh
docker-compose up --build
```

if using locall ollama
uncomment ollama image in docker compose
```bash
docker-compose up --build ollama
docker-compose exec ollama ollama pull mistral 
```

## Frontend → Backend Connection

The frontend uses a Vite proxy so all API calls go through `/api/` which is rewritten and forwarded to the FastAPI backend:

```
Frontend  →  /api/v1/search  →  Vite proxy strips /api  →  backend:8000/v1/search
```

In your frontend code, use `/api/` as the base path:
```js
// Example: search CVs
fetch("/api/v1/search", {
  method: "POST",
  body: formData,
});
```

No need to hardcode the backend URL — the proxy handles it in both dev and Docker.

## API Documentation

To explore and test the project APIs (including matching and automated evaluation endpoints), open the interactive Swagger UI at:
👉 **http://localhost:8001/docs**
