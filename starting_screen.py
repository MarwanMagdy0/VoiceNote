from utiles import *

class StartingScreen(QDialog):
    worksapce_button: QPushButton
    fileview_button: QPushButton
    file_type_choosed = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        uic.loadUi(SCRIPT_DIRECTORY + "/" + "ui/starting_screen.ui",self)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setWindowTitle("choose")
        self.worksapce_button.clicked.connect(lambda: self.create("workspace"))
        self.fileview_button.clicked.connect (lambda: self.create("file-view"))
        self.file_type = None

    def create(self, file_type):
        self.file_type_choosed.emit(file_type)
        self.close()
