import requests
from app.services.llm.provider.base import LLMProvider
from app.core.config import settings


class GeminiProvider(LLMProvider):
    def __init__(
        self,
        base_url: str = settings.gemini_base_url,
        api_key: str = settings.gemini_api_key,
        model: str = settings.gemini_model,
    ):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.model = model

    def generate(self, prompt: str) -> str:
        url = f"{self.base_url}/v1beta/models/{self.model}:generateContent"

        headers = {
            "Content-Type": "application/json",
            "X-goog-api-key": self.api_key,
        }

        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": prompt}
                    ]
                }
            ]
        }

        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()

            # Extract text from Gemini response structure
            candidates = data.get("candidates", [])
            if candidates:
                parts = candidates[0].get("content", {}).get("parts", [])
                if parts:
                    return parts[0].get("text", "")

            return ""

        except requests.exceptions.RequestException as e:
            print(f"Error calling Gemini: {e}")
            return f"Error: Could not connect to Gemini. {str(e)}"
