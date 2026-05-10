from app.services.llm.provider.ollama import OllamaProvider
from app.services.llm.provider.gemini import GeminiProvider
from app.services.llm.tempelate.prompts import Prompts
from app.core.config import settings


def _default_provider():
    if settings.llm_provider == "gemini":
        return GeminiProvider()
    return OllamaProvider()


class LLMService:
    def __init__(self, provider=None):
        self.provider = provider or _default_provider()

    def extract_job_details(self, user_input: str) -> tuple[str, int]:
        """
        Extracts Job Description and top N candidates requested from user input.
        Returns: (job_description, top_n)
        """
        prompt = Prompts.extract_jd_and_n(user_input)
        response = self.provider.generate(prompt)

        try:
            # Parse output format: JD: [text] | N: [number]
            parts = response.split("|")
            jd_text = parts[0].replace("JD:", "").strip()
            top_n = int(parts[1].replace("N:", "").strip())
        except Exception:
            # Fallback if parsing fails
            jd_text = user_input
            top_n = settings.default_top_n

        return jd_text, top_n

    def evaluate_candidates(self, jd_text: str, top_n: int, context_docs: str) -> str:
        """
        Generates an HR evaluation report of the candidates based on the job description.
        """
        prompt = Prompts.evaluate_candidates(jd_text, top_n, context_docs)
        report = self.provider.generate(prompt)
        return report
