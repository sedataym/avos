import os
from deep_translator import DeeplTranslator
from src.core.translation.base_translator import BaseTranslator

class DeepLTranslatorEngine(BaseTranslator):
    def __init__(self, api_key=None, source='en', target='tr'):
        # If API key not provided, look for DEEPL_API_KEY env variable
        self.api_key = api_key or os.getenv("DEEPL_API_KEY", "YOUR_DEEPL_API_KEY")
        self.source = source
        self.target = target
        self._translator = None

    def set_languages(self, source: str, target: str):
        self.source = source
        self.target = target
        if self._translator:
            self._translator.source = source
            self._translator.target = target

    @property
    def translator(self):
        if self._translator is None:
            try:
                self._translator = DeeplTranslator(
                    api_key=self.api_key,
                    source=self.source,
                    target=self.target
                )
            except Exception as e:
                print(f"DeepL Initialization Error: {e}")
        return self._translator

    def translate(self, text: str) -> str:
        if not self.api_key or self.api_key == "YOUR_DEEPL_API_KEY":
            return "Error: DeepL API key is missing. Please define DEEPL_API_KEY."
            
        try:
            if self.translator:
                return self.translator.translate(text)
            return "Error: DeepL could not be initialized."
        except Exception as e:
            print(f"DeepL Translation Error: {e}")
            return f"Error: {e}"
