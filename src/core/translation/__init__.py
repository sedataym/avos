"""Translation subsystem for Avos."""

from src.core.translation.base_translator import BaseTranslator, TranslationResult
from src.core.translation.google_engine import GoogleEngine
from src.core.translation.deepl_engine import DeepLTranslatorEngine
from src.core.translation.translator_manager import TranslatorManager

__all__ = [
    "BaseTranslator",
    "TranslationResult",
    "GoogleEngine",
    "DeepLTranslatorEngine",
    "TranslatorManager",
]
