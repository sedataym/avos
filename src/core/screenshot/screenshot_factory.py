from src.core.screenshot.base_screenshot import BaseScreenshot
from src.core.screenshot.spectacle_screenshot import SpectacleScreenshot

class ScreenshotFactory:
    @staticmethod
    def get_engine() -> BaseScreenshot:
        # Currently only Spectacle (KDE) is supported.
        # Future implementations can check OS/DE and return the appropriate engine.
        return SpectacleScreenshot()
