from PyQt5.QtWidgets import QMainWindow, QApplication ,QLabel ,QPushButton, QSizePolicy, QTreeWidgetItem
from PyQt5 import QtGui, uic
from file_view import *
from workspace import *
from welcome_screen import *
from pathlib import Path
import PyQt5
os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = os.fspath(Path(PyQt5.__file__).resolve().parent / "Qt5" / "plugins")

if len(sys.argv) > 1:
    if not sys.argv[1].endswith(".vnote"):
        sys.exit()
                
class MainWindow(QMainWindow):
    stackedWidget: QStackedWidget
    def __init__(self):
        super().__init__()
        self.init_ui()
        if len(sys.argv) == 1:
            self.setWindowTitle("Welcome Screen")
            self.welcome_screen()
            self.showMaximized()
            
        elif len(sys.argv) > 1:
            self.check_if_vnote_is_empty()
            

    def init_ui(self):
        uic.loadUi(SCRIPT_DIRECTORY + "/" + "ui/main_window.ui",self)
        self.setWindowIcon(QIcon(SCRIPT_DIRECTORY + "/" + 'ui/data/icon.png'))

    
    def welcome_screen(self):
        welcome_screen_widget = WelcomeScreen()
        welcome_screen_widget.create_new_selected.connect(self.created_first_form)
        welcome_screen_widget.change_view.connect(self.card_selected)
        self.update_stacked(welcome_screen_widget)
    

    def check_if_vnote_is_empty(self):
        with open(sys.argv[1], "r") as f:
            if f.read() == "":
                self.starting_screen = StartingScreen()
                self.starting_screen.file_type_choosed.connect(self.created_first_form)
                self.starting_screen.show()
                
            else: # if there is a current vnote form
                self.load_from_vnote(sys.argv[1])


    def created_first_form(self, file_type):
        file_json = HandleJsonFiles(sys.argv[1])

        if file_type == "workspace":
            file_json.save_data({"type":"workspace", "cards":[], "card-title":"WorkSpace", "back":None})

        else:
            file_json.save_data({"type":"file-view", "back":None, "card-title":"file view"})

        if not os.path.isdir(sys.argv[1][:-6]):
            os.mkdir(sys.argv[1][:-6])
        
        self.load_from_vnote(sys.argv[1])


    def load_from_vnote(self, path):
        self.workspace_json_file = HandleJsonFiles(path)
        if self.workspace_json_file.read_data().get("type") == None:
            data = self.workspace_json_file.read_data()
            data["type"] = "file-view"
            data["card-title"] = "file view"
            data["back"] = None
            self.workspace_json_file.save_data(data)

        if self.workspace_json_file["type"] == "workspace":
            w = WorkSpace(path)
            w.go_back_to_welcome_screen.connect(self.welcome_screen)
            w.card_selected.connect(self.card_selected)
            w.go_back_from_workspace.connect(self.card_selected)
            self.update_stacked(w)

        else:
            file_view = FileView(path)
            file_view.go_back.connect(self.card_selected)
            file_view.go_back_to_welcome_screen.connect(self.welcome_screen)
            self.update_stacked(file_view)
        self.showMaximized()


    def card_selected(self, card_data: dict, directory):
        self.setWindowTitle(os.path.abspath(card_data["card-fname"]).split("/")[-1])
        current_widget = self.stackedWidget.widget(0)
        if current_widget is not None:
            current_widget: QWidget
            current_widget.deleteLater()

        if card_data["type"] == "workspace":
            w = WorkSpace(os.path.normpath(directory) + "/" + card_data["card-fname"])
            w.card_selected.connect(self.card_selected)
            w.go_back_from_workspace.connect(self.card_selected)
            w.go_back_to_welcome_screen.connect(self.welcome_screen)
            self.update_stacked(w)

        elif card_data["type"] == "file-view":
            print(os.path.normpath(directory) + "/" + card_data["card-fname"])
            file_view = FileView(os.path.normpath(directory) + "/" + card_data["card-fname"])
            file_view.go_back.connect(self.card_selected)
            file_view.go_back_to_welcome_screen.connect(self.welcome_screen)
            self.update_stacked(file_view)

        

    def update_stacked(self, widget):
        window_size[0] = self.width()
        window_size[1] = self.height()
        self.stackedWidget.addWidget(widget)
        self.stackedWidget.setCurrentWidget(widget)


app = QApplication([])
collector = GarbageCollector()
collector.start()
wind = MainWindow()
app.exec_()

collector.stop()

os._exit(0)