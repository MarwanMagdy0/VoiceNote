import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtGui import QPixmap

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.label = QLabel(self)
        self.setCentralWidget(self.label)
        self.setWindowTitle('Clipboard Image Example')
        self.show()

        clipboard = QApplication.clipboard()
        clipboard.dataChanged.connect(self.updateImageFromClipboard)

    def updateImageFromClipboard(self):
        clipboard = QApplication.clipboard()
        mime_data = clipboard.mimeData()

        if mime_data.hasImage():
            image = mime_data.imageData()
            pixmap = QPixmap.fromImage(image)
            self.label.setPixmap(pixmap)
    
    def saveAsPng(self):
        pixmap = self.label.pixmap()
        if pixmap is not None:
            save_path = "path.png"
            if save_path:
                pixmap.save(save_path, "PNG")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
