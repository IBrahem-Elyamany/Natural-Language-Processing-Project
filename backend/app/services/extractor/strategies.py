from abc import ABC, abstractmethod
import fitz  # PyMuPDF
import docx
import pytesseract
from PIL import Image

class ExtractionStrategy(ABC):
    @abstractmethod
    def extract(self, file_path: str) -> str:
        """Extract text from the given file."""
        pass

class PdfExtractionStrategy(ExtractionStrategy):
    def extract(self, file_path: str) -> str:
        text = ""
        try:
            doc = fitz.open(file_path)
            for page in doc:
                text += page.get_text()
        except Exception as e:
            print(f"Error reading PDF {file_path}: {e}")
        return text

class DocxExtractionStrategy(ExtractionStrategy):
    def extract(self, file_path: str) -> str:
        text = ""
        try:
            doc = docx.Document(file_path)
            text = "\n".join([para.text for para in doc.paragraphs])
        except Exception as e:
            print(f"Error reading DOCX {file_path}: {e}")
        return text

class ImageExtractionStrategy(ExtractionStrategy):
    def extract(self, file_path: str) -> str:
        text = ""
        try:
            img = Image.open(file_path)
            text = pytesseract.image_to_string(img)
        except Exception as e:
            print(f"Error reading Image {file_path}: {e}")
        return text
