#!/usr/bin/env python3
import sys
import os
import time
import subprocess
import re
import threading
from threading import Lock
from PySide6.QtCore import QThread, Signal, Slot, Qt, QRect, QTimer
from PySide6.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QPushButton, QComboBox
from PySide6.QtGui import QGuiApplication
from PIL import Image, ImageOps, ImageEnhance
from deep_translator import GoogleTranslator

IMG_PATH = "/tmp/pyside_ocr_snapshot.png"
FULL_SCREEN_PATH = "/tmp/wayland_full_snap.png"

class OCRWorker(QThread):
    new_translation = Signal(str)

    def __init__(self):
        super().__init__()
        self.capture_rect = QRect(560, 750, 800, 140)
        self.lock = Lock()
        self.running = False
        self.translator = GoogleTranslator(source='en', target='tr')
        self.ocr_engine = "Tesseract"
        self.easy_reader = None
        self.last_text = ""
        self._translation_lock = Lock()
        self._is_translating = False

    def set_rect(self, qrect):
        with self.lock:
            self.capture_rect = QRect(qrect)
            self.last_text = ""
            print(f"OCRWorker: Yeni bölge: {qrect.x()},{qrect.y()} {qrect.width()}x{qrect.height()}")

    def set_engine(self, engine):
        with self.lock:
            self.ocr_engine = engine
            self.last_text = ""
            print(f"OCRWorker: Motor: {engine}")

    def stop(self):
        self.running = False
        self.wait()

    def _async_translate(self, text):
        with self._translation_lock: self._is_translating = True
        try:
            translated = self.translator.translate(text)
            self.new_translation.emit(translated)
        except Exception as e: print(f"Çeviri Hatası: {e}")
        finally:
            with self._translation_lock: self._is_translating = False

    def run(self):
        self.running = True
        print(f"OCRWorker: DÖNGÜ BAŞLADI. Motor: {self.ocr_engine}")
        while self.running:
            try:
                start_total = time.perf_counter()
                with self.lock:
                    rect = QRect(self.capture_rect)
                    engine = self.ocr_engine
                
                with self._translation_lock: translating = self._is_translating

                if rect.width() < 10 or rect.height() < 10:
                    time.sleep(0.5); continue

                # 1. Capture (Spectacle - Wayland için en güvenlisi)
                if os.path.exists(FULL_SCREEN_PATH): os.remove(FULL_SCREEN_PATH)
                subprocess.run(["spectacle", "-b", "-f", "-n", "-o", FULL_SCREEN_PATH], 
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                
                if not os.path.exists(FULL_SCREEN_PATH):
                    time.sleep(0.5); continue
                
                # 2. Prep (Crop & Filter)
                with Image.open(FULL_SCREEN_PATH) as full_img:
                    crop = full_img.crop((max(0, rect.x()), max(0, rect.y()),
                                         min(full_img.width, rect.x() + rect.width()),
                                         min(full_img.height, rect.y() + rect.height())))
                    
                    if engine == "Tesseract":
                        img = crop.resize((crop.width * 2, crop.height * 2), Image.Resampling.NEAREST)
                        img = ImageOps.grayscale(img)
                        img = ImageOps.autocontrast(img)
                        img = img.point(lambda x: 0 if x < 128 else 255, '1')
                        img = ImageOps.invert(img.convert('L'))
                        img = ImageOps.expand(img, border=10, fill='white')
                        img.save(IMG_PATH)
                    else:
                        crop.save(IMG_PATH)

                # 3. OCR
                clean = ""
                if engine == "Tesseract":
                    cfg = ["tesseract", IMG_PATH, "stdout", "--oem", "1", "--psm", "3", "-l", "eng",
                           "-c", "tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.,!?'\"- "]
                    text = subprocess.run(cfg, capture_output=True, text=True).stdout
                    clean = re.sub(r'[^a-zA-Z0-9.,!?\'\"\-\s]', '', text)
                else:
                    if self.easy_reader is None:
                        import easyocr
                        self.easy_reader = easyocr.Reader(['en'], gpu=True)
                    res = self.easy_reader.readtext(IMG_PATH)
                    clean = " ".join([r[1] for r in res])
                
                clean = " ".join(clean.split()).strip()

                # 4. API (Asenkron)
                if len(clean) > 2 and clean != self.last_text and not translating:
                    self.last_text = clean
                    threading.Thread(target=self._async_translate, args=(clean,), daemon=True).start()
                    print(f"[{engine}] Metin: {clean} | Süre: {time.perf_counter()-start_total:.2f}s")

            except Exception as e: print(f"Döngü Hatası: {e}")
            time.sleep(0.3)

class TransparentOverlay(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AVOS_TRANSLATION_OVERLAY")
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.WindowDoesNotAcceptFocus | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WA_ShowWithoutActivating)
        self.resize(800, 200)
        self.layout = QVBoxLayout(self); self.layout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel("Çeviri burada görünecek.")
        self.label.setWordWrap(True); self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("color: white; font-size: 20px; font-weight: bold; background: rgba(0,0,0,180); border-radius: 6px; padding: 10px;")
        self.layout.addWidget(self.label)
        self.set_mode(False)
        self.timer = QTimer(self); self.timer.timeout.connect(self.raise_); self.timer.start(2000)

    @Slot(str)
    def update_text(self, text): self.label.setText(text); self.raise_()

    def set_mode(self, scan):
        self.setAttribute(Qt.WA_TransparentForMouseEvents, scan)
        self.setCursor(Qt.ArrowCursor if scan else Qt.SizeAllCursor)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if event.position().x() > self.width() - 20 and event.position().y() > self.height() - 20:
                self.windowHandle().startSystemResize(Qt.RightEdge | Qt.BottomEdge)
            else: self.windowHandle().startSystemMove()
            event.accept()

class ControlPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.worker = OCRWorker()
        self.overlay = TransparentOverlay()
        self.setWindowTitle("Evrensel MORT Paneli")
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("OCR Motoru:"))
        self.combo = QComboBox(); self.combo.addItems(["Tesseract", "EasyOCR"])
        self.combo.currentTextChanged.connect(self.worker.set_engine); layout.addWidget(self.combo)
        
        self.btn_reg = QPushButton("🖼 Bölge Seç")
        self.btn_reg.setStyleSheet("background-color: #1565C0; color: white; font-weight: bold; padding: 10px;")
        self.btn_reg.clicked.connect(self.select_region); layout.addWidget(self.btn_reg)
        
        self.btn_start = QPushButton("▶ Taramayı Başlat")
        self.btn_start.setStyleSheet("background-color: #2E7D32; color: white; font-weight: bold; padding: 10px;")
        self.btn_start.clicked.connect(self.start); layout.addWidget(self.btn_start)
        
        self.btn_stop = QPushButton("■ Durdur")
        self.btn_stop.setStyleSheet("background-color: #C62828; color: white; font-weight: bold; padding: 10px;")
        self.btn_stop.clicked.connect(self.stop); layout.addWidget(self.btn_stop)
        
        self.show(); self.overlay.show()
        self.worker.new_translation.connect(self.overlay.update_text)

    def select_region(self):
        import tempfile
        t_out = os.path.join(tempfile.gettempdir(), "slurp_final.txt")
        if os.path.exists(t_out): os.remove(t_out)
        try:
            self.hide(); QApplication.processEvents(); time.sleep(0.2)
            os.system(f"slurp -f '%x,%y %w,%h' > {t_out} 2>/dev/null &")
            start = time.time()
            output = ""
            while time.time() - start < 30:
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
                    self.worker.set_rect(QRect(x, y, w, h))
                    self.overlay.label.setText(f"Bölge: {x},{y} {w}x{h}")
        except Exception as e: print(f"Hata: {e}")
        finally: 
            if os.path.exists(t_out): os.remove(t_out)
            self.show()

    def start(self): 
        self.overlay.set_mode(True)
        if not self.worker.isRunning(): self.worker.start()

    def stop(self): self.worker.stop(); self.overlay.set_mode(False)

if __name__ == "__main__":
    os.environ["QT_QPA_PLATFORM"] = "xcb"
    app = QApplication(sys.argv)
    panel = ControlPanel()
    sys.exit(app.exec())
