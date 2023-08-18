from starting_screen import *
from group import EditableLabel

class Card(QWidget):
    card_selected = pyqtSignal(dict, str)
    def __init__(self, card_data : dict, workspace_file_directory):
        super().__init__()
        uic.loadUi(SCRIPT_DIRECTORY + "/" + "ui/group_card.ui",self)
        j = HandleJsonFiles(workspace_file_directory + "/" + card_data["card-fname"])
        self.label.setText(j["card-title"])
        self.card_data = card_data
        self.workspace_file_directory = workspace_file_directory
    

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.card_selected.emit(self.card_data, self.workspace_file_directory)



class WorkSpace(QWidget):
    add_new_card_button: QPushButton
    gridLayout: QGridLayout
    card_selected = pyqtSignal(dict, str)
    label_layout: QVBoxLayout
    go_back_button:QPushButton
    go_back_from_workspace = pyqtSignal(dict, str)
    go_back_to_welcome_screen = pyqtSignal()
    def __init__(self, workspace_file):
        super().__init__()
        self.workspace_file = workspace_file
        self.workspace_json_file = HandleJsonFiles(workspace_file)
        self.init_ui()


    def init_ui(self):
        uic.loadUi(SCRIPT_DIRECTORY + "/" + "ui/workspace.ui",self)
        self.add_new_card_button.clicked.connect(self.add_new_card_method)
        self.next_item_index = 0
        self.scroll_area_bar = self.scrollArea.verticalScrollBar()
        self.title_label = EditableLabel(self, self.workspace_json_file.read_data()["card-title"], 'background:#1e1e1e;font: 63 16pt "JetBrains Mono NL SemiBold";')
        self.label_layout.addWidget(self.title_label)
        self.title_label.title_updated.connect(self.editing_title_finished)
        back_directory = self.workspace_json_file.read_data()["back"]
        if back_directory is not None:
            j = HandleJsonFiles(self.workspace_file[:-6] + back_directory)
            file_type = j.read_data()["type"]
            prev_card_data = {"card-fname":back_directory, "type":file_type}
            self.go_back_button.clicked.connect(lambda : self.go_back_from_workspace.emit(prev_card_data, self.workspace_file[:-6]))
        else:
            self.go_back_button.clicked.connect(self.go_back_to_welcome_screen.emit)
            data = refrences_file.read_data()
            if os.path.abspath(self.workspace_file) in data["ref"]:
                data["ref"].remove(os.path.abspath(self.workspace_file))
            data["ref"].insert(0, os.path.abspath(self.workspace_file))
            refrences_file.save_data(data)


        for card_data in self.workspace_json_file["cards"]:
            card = Card(card_data, self.workspace_file[:-6])
            card.card_selected.connect(lambda card_directory, workspace_directroy: self.card_selected.emit(card_directory, workspace_directroy))
            self.add_widget(card)
        self.layout = self.scrollArea.widget().layout()
        self.scrollArea.widget().setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.scroll_area_bar = self.scrollArea.verticalScrollBar()


    def add_new_card_method(self):
        self.starting_screen = StartingScreen()
        self.starting_screen.setWindowModality(Qt.ApplicationModal)
        self.starting_screen.file_type_choosed.connect(self.create_card_directory)
        self.starting_screen.show()
    

    def create_card_directory(self, file_type):
        card_fname     = get_time()
        card_directory = os.path.abspath(self.workspace_file[:-6] + "/" + card_fname)
        card_data = {"card-fname" : card_fname + "/" + card_fname + ".vnote", "type":file_type}
        os.mkdir(card_directory)
        os.mkdir(card_directory + "/" + card_fname)
        j = HandleJsonFiles(card_directory + "/" + card_fname + ".vnote")
        if file_type == "workspace":
            j.save_data({"type":"workspace", "cards":[], "back":"/../../../" + os.path.basename(self.workspace_file), "card-title":"workspace"})
        else:
            j.save_data({"type":"file-view", "back": "/../../../" + os.path.basename(self.workspace_file), "card-title":"file view"})

        card = Card(card_data, self.workspace_file[:-6])
        card.card_selected.connect(lambda card_directory, workspace_directroy: self.card_selected.emit(card_directory, workspace_directroy))
        self.add_widget(card)
        data = self.workspace_json_file.read_data()
        data["cards"].append(card_data)
        self.workspace_json_file.save_data(data)

    def add_widget(self, widget):
        self.gridLayout.addWidget(widget, self.next_item_index//5, self.next_item_index%5)
        self.scroll_area_bar.setMaximum(self.scroll_area_bar.maximum()+200)
        self.scroll_area_bar.setValue(self.scroll_area_bar.maximum())
        self.next_item_index+=1
    
    def editing_title_finished(self, new_name):
        data = self.workspace_json_file.read_data()
        data["card-title"] = new_name
        self.workspace_json_file.save_data(data)
        self.title_label.title_label.setText(new_name)



if __name__ == "__main__":
    app = QApplication([])
    workspace = WorkSpace(sys.argv[1])
    workspace.showMaximized()
    app.exec_()