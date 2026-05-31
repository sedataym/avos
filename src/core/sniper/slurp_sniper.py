import os
import time
from PySide6.QtCore import QRect
from PySide6.QtWidgets import QApplication
from src.core.sniper.base_sniper import BaseSniper

class SlurpSniper(BaseSniper):
    def get_region(self) -> QRect | None:
        """Selects a region on the screen using slurp."""
        import tempfile
        t_out = os.path.join(tempfile.gettempdir(), "slurp_final.txt")
        if os.path.exists(t_out):
            os.remove(t_out)
        
        try:
            # Run slurp and write output to file
            os.system(f"slurp -f '%x,%y %w,%h' > {t_out} 2>/dev/null &")
            start = time.time()
            output = ""
            while time.time() - start < 30: # 30 seconds timeout
                QApplication.processEvents()
                if os.path.exists(t_out) and os.path.getsize(t_out) > 0:
                    time.sleep(0.1)
                    with open(t_out, "r") as f:
                        output = f.read().strip()
                    break
                time.sleep(0.1)
            
            if output:
                p = output.split()
                if len(p) >= 2:
                    x, y = map(int, p[0].split(","))
                    w, h = map(int, p[1].split(","))
                    return QRect(x, y, w, h)
        except Exception as e:
            print(f"Region Selection Error (slurp): {e}")
        finally:
            if os.path.exists(t_out):
                os.remove(t_out)
        return None
