from src.core.sniper.base_sniper import BaseSniper
from src.core.sniper.slurp_sniper import SlurpSniper

class SniperFactory:
    @staticmethod
    def get_engine() -> BaseSniper:
        # Currently only Slurp (Wayland) is supported.
        # Future implementations can check OS/DE and return the appropriate engine.
        return SlurpSniper()
