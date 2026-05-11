import os
from typing import Dict
from app.services.extractor.strategies import (
    ExtractionStrategy,
    PdfExtractionStrategy,
    DocxExtractionStrategy,
    ImageExtractionStrategy
)

class TextExtractorService:
    """
    Context class for text extraction. It uses the strategy pattern to
    dynamically select the right extraction logic based on the file extension.
    """
    def __init__(self):
        self._strategies: Dict[str, ExtractionStrategy] = {
            ".pdf": PdfExtractionStrategy(),
            ".docx": DocxExtractionStrategy(),
            ".png": ImageExtractionStrategy(),
            ".jpg": ImageExtractionStrategy(),
            ".jpeg": ImageExtractionStrategy(),
        }

    def extract_text(self, file_path: str) -> str:
        _, ext = os.path.splitext(file_path)
        ext = ext.lower()

        strategy = self._strategies.get(ext)
        if not strategy:
            print(f"Unsupported file type: {ext}")
            return ""

        return strategy.extract(file_path)
