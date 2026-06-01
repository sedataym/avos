import os
import tempfile

OCR_ENGINES = ["Tesseract", "EasyOCR"]
TRANSLATION_ENGINES = ["Google", "DeepL"]
LANGUAGES = {
    "Auto": "auto",
    "English": "en",
    "Turkish": "tr",
    "German": "de",
    "French": "fr",
    "Japanese": "ja",
    "Korean": "ko",
    "Chinese": "zh",
    "Russian": "ru",
    "Arabic": "ar",
    "Hebrew": "he",
    "Vietnamese": "vi",
    "Thai": "th",
    "Spanish": "es"
}

# Map UI language codes to Tesseract/EasyOCR language codes
OCR_LANG_MAPPING = {
    "en": {"tess": "eng", "easy": "en"},
    "tr": {"tess": "tur", "easy": "tr"},
    "ru": {"tess": "rus", "easy": "ru"},
    "ar": {"tess": "ara", "easy": "ar"},
    "he": {"tess": "heb", "easy": "he"},
    "de": {"tess": "deu", "easy": "de"},
    "fr": {"tess": "fra", "easy": "fr"},
    "ja": {"tess": "jpn", "easy": "ja"},
    "ko": {"tess": "kor", "easy": "ko"},
    "zh": {"tess": "chi_sim", "easy": "ch_sim"},
    "vi": {"tess": "vie", "easy": "vi"},
    "th": {"tess": "tha", "easy": "th"},
    "es": {"tess": "spa", "easy": "es"}
}

SETTINGS_FILE = "settings.pkl"
PRESETS_FILE = "presets.pkl"

# Temp Files
TEMP_DIR = tempfile.gettempdir()
IMG_PATH = os.path.join(TEMP_DIR, "avos_snapshot.png")
FULL_SCREEN_TEMP_PATH = os.path.join(TEMP_DIR, "avos_full_snap.png")
SOCKET_PATH = os.path.join(TEMP_DIR, "avos.sock")
SLURP_TEMP_PATH = os.path.join(TEMP_DIR, "slurp_final.txt")
