from abc import ABC, abstractmethod
import fitz  # PyMuPDF
import docx
import pytesseract
from PIL import Image
from pdf2image import convert_from_path

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
            doc.close()

            if len(text.strip()) < 50:
                images = convert_from_path(file_path)
                for img in images:
                    text += pytesseract.image_to_string(img)
                print(f"Imge Text: {text}")
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
            print(text)
        except Exception as e:
            print(f"Error reading Image {file_path}: {e}")
        return text
