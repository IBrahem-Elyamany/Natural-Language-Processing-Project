# ROMI

## Features

- Upload CVs in PDF format
- Match CVs against job descriptions using Sentence Transformer model
- Use ChromaDB for vector storage and retrieval
- Evaluate candidates using LLM (gemini flash 2.5)

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

