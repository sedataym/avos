from deep_translator import GoogleTranslator
from src.core.translation.base_translator import BaseTranslator

class GoogleEngine(BaseTranslator):
    def __init__(self, source='en', target='tr'):
        self.source = source
        self.target = target
        self.translator = GoogleTranslator(source=self.source, target=self.target)

    def set_languages(self, source: str, target: str):
        self.source = source
        self.target = target
        self.translator.source = source
        self.translator.target = target

    def translate(self, text: str) -> str:
        try:
            return self.translator.translate(text)
        except Exception as e:
            print(f"Google Translation Error: {e}")
            return f"Error: {e}"
