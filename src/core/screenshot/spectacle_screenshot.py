import os
import subprocess
from PIL import Image
from PySide6.QtCore import QRect
from src.core.screenshot.base_screenshot import BaseScreenshot

class SpectacleScreenshot(BaseScreenshot):
    def __init__(self):
        self.full_screen_temp = "/tmp/avos_full_snap.png"

    def capture(self, rect: QRect, output_path: str) -> bool:
        if os.path.exists(self.full_screen_temp):
            os.remove(self.full_screen_temp)
        
        try:
            # Use spectacle for KDE/Wayland
            subprocess.run(
                ["spectacle", "-b", "-f", "-n", "-o", self.full_screen_temp],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True
            )
            
            if not os.path.exists(self.full_screen_temp):
                return False
            
            with Image.open(self.full_screen_temp) as full_img:
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
