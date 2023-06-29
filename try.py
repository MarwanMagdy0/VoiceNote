from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFontDialog
from PyQt5.QtGui import QFont

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Choose Font Example")
        self.setGeometry(100, 100, 300, 200)

        button = QPushButton("Choose Font", self)
        button.move(100, 80)
        button.clicked.connect(self.openFontDialog)

    def openFontDialog(self):
        # Create a default font with Monospace and 16 pixels
        default_font = QFont("Monospace", 20)

        # Open the "Choose Font" dialog with the default font as the initial selection
        font, ok = QFontDialog.getFont(default_font)

        if ok:
            # Set the chosen font as the new default font
            QApplication.setFont(font)
            print("Selected Font:", font.toString())

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
