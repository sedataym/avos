from src.core.ocr.base_ocr import BaseOCREngine

class EasyOCREngine(BaseOCREngine):
    def __init__(self):
        self.reader = None

    def read_text(self, image_path: str) -> str:
        if self.reader is None:
            import easyocr
            self.reader = easyocr.Reader(['en'], gpu=True)
        
        try:
            res = self.reader.readtext(image_path)
            clean = " ".join([r[1] for r in res])
            return " ".join(clean.split()).strip()
        except Exception as e:
            print(f"EasyOCR Error: {e}")
            return ""
