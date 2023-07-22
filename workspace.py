from starting_screen import *
from group import EditableLabel

class Card(QWidget):
    card_selected = pyqtSignal(dict)
    def __init__(self, card_data : dict):
        super().__init__()
        uic.loadUi(SCRIPT_DIRECTORY + "\\" + "ui\\group_card.ui",self)
        j = HandleJsonFiles(card_data["directory"])
        self.label.setText(j["card-title"])
        self.card_data = card_data
    

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.card_selected.emit(self.card_data)



class WorkSpace(QWidget):
    add_new_card_button: QPushButton
    gridLayout: QGridLayout
    card_selected = pyqtSignal(dict)
    label_layout: QVBoxLayout
    go_back_button:QPushButton
    go_back_from_workspace = pyqtSignal(dict)
    def __init__(self, workspace_file):
        super().__init__()
        self.workspace_file = workspace_file
        self.workspace_json_file = HandleJsonFiles(workspace_file)
        self.init_ui()


    def init_ui(self):
        uic.loadUi(SCRIPT_DIRECTORY + "\\" + "ui\\workspace.ui",self)
        self.add_new_card_button.clicked.connect(self.add_new_card_method)
        self.next_item_index = 0
        self.scroll_area_bar = self.scrollArea.verticalScrollBar()
        self.title_label = EditableLabel(self, self.workspace_json_file.read_data()["card-title"], 'background:#1e1e1e;font: 63 16pt "JetBrains Mono NL SemiBold";')
        self.label_layout.addWidget(self.title_label)
        self.title_label.title_updated.connect(self.editing_title_finished)
        back_directory = self.workspace_json_file.read_data()["back"]
        if back_directory is not None:
            j = HandleJsonFiles(back_directory)
            file_type = j.read_data()["type"]
            prev_card_data = {"directory":back_directory, "type":file_type}
            self.go_back_button.clicked.connect(lambda data: self.go_back_from_workspace.emit(prev_card_data))

        for card_data in self.workspace_json_file["cards"]:
            card = Card(card_data)
            card.card_selected.connect(lambda card_directory: self.card_selected.emit(card_directory))
            self.add_widget(card)


    def add_new_card_method(self):
        self.starting_screen = StartingScreen()
        self.starting_screen.setWindowModality(Qt.ApplicationModal)
        self.starting_screen.file_type_choosed.connect(self.create_card_directory)
        self.starting_screen.show()
    

    def create_card_directory(self, file_type):
        card_directory = self.workspace_file[:-6] + "\\" + get_time()
        card_fname     = get_time()
        card_data = {"directory" :  card_directory + "\\" + card_fname + ".vnote", "type":file_type}
        os.mkdir(card_directory)
        os.mkdir(card_directory + "\\" + card_fname)
        j = HandleJsonFiles(card_directory + "\\" + card_fname + ".vnote")
        if file_type == "workspace":
            j.save_data({"type":"workspace", "cards":[], "back":self.workspace_file, "card-title":"Title"})
        else:
            j.save_data({"type":"file-view", "card-title":"Title", "back":self.workspace_file})

        card = Card(card_data)
        card.card_selected.connect(lambda card_directory: self.card_selected.emit(card_directory))
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