import sys
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QApplication, QLabel

import sounddevice as sd
import numpy as np

class OverlayWindow(QLabel):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Overlay")
        self.setStyleSheet("QLabel { color: red; font-size: 72px; }")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setGeometry(1080, 500, 600, 100)
        self.setText("Start!")
        self.show()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_microphone)
        self.timer.start(100)

        self.microphone_active = False

    def check_microphone(self):
        samples = sd.rec(int(0.1 * 44100), samplerate=44100, channels=1, dtype=np.float32)
        sd.wait()

        mean_amplitude = np.mean(np.abs(samples))*10000

        print(mean_amplitude)

        threshold = 500

        if mean_amplitude > threshold:
            self.microphone_active = True
            self.setText("CHILL OUT!")
        else:
            self.microphone_active = False
            self.setText("")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    overlay = OverlayWindow()
    sys.exit(app.exec_())
