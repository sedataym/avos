from dataclasses import dataclass
from abc import ABC, abstractmethod

@dataclass
class OCRResult:
    text: str
    confidence: float = 0.0

class BaseOCREngine(ABC):
    @abstractmethod
    def read_text(self, image_path: str) -> str:
        """Reads text from image and returns cleaned text."""
        pass
