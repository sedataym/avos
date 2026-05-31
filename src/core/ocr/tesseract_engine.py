import subprocess
import re
from src.core.ocr.base_ocr import BaseOCREngine

class TesseractEngine(BaseOCREngine):
    def read_text(self, image_path: str) -> str:
        cfg = [
            "tesseract", image_path, "stdout", 
            "--oem", "1", "--psm", "3", "-l", "eng",
            "-c", "tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.,!?'\"- "
        ]
        try:
            result = subprocess.run(cfg, capture_output=True, text=True, check=True)
            text = result.stdout
            clean = re.sub(r'[^a-zA-Z0-9.,!?\'\"\-\s]', '', text)
            return " ".join(clean.split()).strip()
        except Exception as e:
            print(f"Tesseract Error: {e}")
            return ""
