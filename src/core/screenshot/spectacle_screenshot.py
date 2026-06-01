import os
import subprocess
from PIL import Image
from PySide6.QtCore import QRect
from src.core.screenshot.base_screenshot import BaseScreenshot
from src.config import FULL_SCREEN_TEMP_PATH

class SpectacleScreenshot(BaseScreenshot):
    def capture(self, rect: QRect, output_path: str) -> bool:
        if os.path.exists(FULL_SCREEN_TEMP_PATH):
            os.remove(FULL_SCREEN_TEMP_PATH)
        
        try:
            # Use spectacle for KDE/Wayland
            subprocess.run(
                ["spectacle", "-b", "-f", "-n", "-o", FULL_SCREEN_TEMP_PATH],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True
            )
            
            if not os.path.exists(FULL_SCREEN_TEMP_PATH):
                return False
            
            with Image.open(FULL_SCREEN_TEMP_PATH) as full_img:
                crop = full_img.crop((
                    max(0, rect.x()), 
                    max(0, rect.y()),
                    min(full_img.width, rect.x() + rect.width()),
                    min(full_img.height, rect.y() + rect.height())
                ))
                crop.save(output_path)
            return True
        except Exception as e:
            print(f"Spectacle Capture Error: {e}")
            return False
