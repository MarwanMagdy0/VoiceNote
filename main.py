from PyQt5.QtWidgets import QMainWindow, QApplication ,QLabel ,QPushButton, QSizePolicy
from PyQt5 import uic
from widgets import *
import sys
class UI(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("load.ui",self)
        layout = self.scrollArea.widget().layout()
        self.scrollArea.widget().setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        group = Group(self)
        layout.addWidget(group)
        group.box_vlayout.addWidget(VoiceNote(self, "output.wav"))        

        group.box_vlayout.addWidget(VoiceNote(self, "kaf.mp3"))        
        group.box_vlayout.addWidget(ImageWidget(self, "img.png"))
        group = Group(self)
        layout.addWidget(group)
        group.box_vlayout.addWidget(VoiceNote(self, "kaf.mp3"))        

        group.box_vlayout.addWidget(VoiceNote(self, "kaf.mp3"))
        group.box_vlayout.addWidget(ImageWidget(self, "img.png"))

app = QApplication(sys.argv)
wind = UI()
wind.show()
app.exec_()
