from abc import ABC, abstractmethod
from PySide6.QtCore import QRect

class BaseScreenshot(ABC):
    @abstractmethod
    def capture(self, rect: QRect, output_path: str) -> bool:
        """Captures a screenshot of the specified region."""
        pass
