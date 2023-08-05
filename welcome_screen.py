from utiles import *
from starting_screen import *
class WelcomeScreen(QWidget):
    create_new_selected = pyqtSignal(str)
    recent_layout: QVBoxLayout
    change_view = pyqtSignal(dict, str)
    def __init__(self):
        super().__init__()
        uic.loadUi(SCRIPT_DIRECTORY + "\\" + "ui\\welcome_screen.ui",self)
        self.create_new_button.clicked.connect(self.create_new_method)
        for item in refrences_file["ref"]:
            ref_button = QPushButton(parent = self, text=os.path.basename(item)[:-6])
            ref_button.clicked.connect(lambda _, path=item: self.ref_button_clicked(path))
            self.recent_layout.addWidget(ref_button)

    def create_new_method(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Create Vnote", "", "VNote Files (*.vnote);;All Files (*)", options=options)
        if file_name:
            push_list(sys.argv, file_name)
            starting_screen = StartingScreen()
            starting_screen.file_type_choosed.connect(lambda file_type: self.create_new_selected.emit(file_type))
            starting_screen.show()
    
    def ref_button_clicked(self, path):
        print(path)
        j = HandleJsonFiles(path)
        data = {
            "card-fname": os.path.basename(path),
            "type": j["type"]
        }
        self.change_view.emit(data, os.path.dirname(path))

    

if __name__ == "__main__":
    app = QApplication([])
    w = WelcomeScreen()
    w.show()
    app.exec_()