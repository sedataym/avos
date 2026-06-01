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
    "Russian": "ru"
}

SETTINGS_FILE = "settings.pkl"
PRESETS_FILE = "presets.pkl"

# Temp Files
TEMP_DIR = tempfile.gettempdir()
IMG_PATH = os.path.join(TEMP_DIR, "avos_snapshot.png")
FULL_SCREEN_TEMP_PATH = os.path.join(TEMP_DIR, "avos_full_snap.png")
SOCKET_PATH = os.path.join(TEMP_DIR, "avos.sock")
SLURP_TEMP_PATH = os.path.join(TEMP_DIR, "slurp_final.txt")
