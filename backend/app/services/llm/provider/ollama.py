import requests
from app.services.llm.provider.base import LLMProvider
from app.core.config import settings

class OllamaProvider(LLMProvider):
    def __init__(self, base_url: str = settings.ollama_base_url, model: str = settings.ollama_model):
        self.base_url = base_url
        self.model = model

    def generate(self, prompt: str) -> str:
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=
                {
                    "model": self.model,
                    "prompt": prompt, 
                    "stream": False
                }
            )
            response.raise_for_status()
            return response.json().get("response", "")
        except requests.exceptions.RequestException as e:
            print(f"Error calling Ollama: {e}")
            return f"Error: Could not connect to LLM provider. {str(e)}"
