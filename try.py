import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFontDialog

class FontDialogDemo(QWidget):
    def __init__(self, parent=None):
        super(FontDialogDemo, self).__init__(parent)
        
        layout = QVBoxLayout()
        self.btn = QPushButton("Choose Font")
        self.btn.clicked.connect(self.get_font)
        
        layout.addWidget(self.btn)
        self.label = QLabel("Hello")
        layout.addWidget(self.label)
        
        self.setLayout(layout)
        self.setWindowTitle("Font Dialog Demo")
        
    def get_font(self):
        font, ok = QFontDialog.getFont()
        print(font.toString())
        if ok:
            self.label.setFont(font)

def main():
    app = QApplication(sys.argv)
    ex = FontDialogDemo()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
