import sys
import cv2
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import QThread, pyqtSignal, Qt

class CameraThread(QThread):
    frame_captured = pyqtSignal(QImage)

    def __init__(self):
        super().__init__()
        self.cap = cv2.VideoCapture(0)

    def run(self):
        while not self.isInterruptionRequested():
            ret, frame = self.cap.read()
            if ret:
                rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgb_image.shape
                bytes_per_line = ch * w
                q_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
                self.frame_captured.emit(q_image)
            cv2.waitKey(1)
        print("closed")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Camera Viewer")
        self.setGeometry(100, 100, 640, 480)

        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(self.label)

        central_widget = QWidget(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.camera_thread = CameraThread()
        self.camera_thread.frame_captured.connect(self.update_image)
        self.camera_thread.start()

    def update_image(self, image):
        pixmap = QPixmap.fromImage(image)
        self.label.setPixmap(pixmap)

    def closeEvent(self, event):
        self.camera_thread.requestInterruption()
        self.camera_thread.wait()
        self.camera_thread.deleteLater()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
