from group import *

class FileView(QWidget):
    go_back = pyqtSignal(dict)
    back_button : QPushButton
    title_layout : QVBoxLayout
    def __init__(self, workspace_file):
        super().__init__()
        self.workspace_json_file = HandleJsonFiles(workspace_file)
        self.groups = []
        self.init_ui()
        

    def init_ui(self):
        uic.loadUi(SCRIPT_DIRECTORY + "\\" + "ui\\load.ui",self)
        self.title_label = EditableLabel(self, self.workspace_json_file.read_data()["card-title"], 'background:#1e1e1e;font: 63 16pt "JetBrains Mono NL SemiBold";')
        self.title_label.title_updated.connect(self.editing_title_finished)
        self.title_layout.addWidget(self.title_label)
        back_directory = self.workspace_json_file.read_data()["back"]
        if back_directory is not None:
            j = HandleJsonFiles(back_directory)
            file_type = j.read_data()["type"]
            self.back_button.clicked.connect(lambda data: self.go_back.emit({"directory":back_directory, "type":file_type}))
        else:
            self.back_button.setEnabled(False)
        self.treeWidget.itemClicked.connect(self.handle_item_clicked)
        self.add_new_group_button.clicked.connect(self.create_new_group)
        self.setWindowIcon(QIcon(SCRIPT_DIRECTORY + "\\" + 'ui\\data\\icon.png'))
        self.layout = self.scrollArea.widget().layout()
        self.scrollArea.widget().setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.scroll_area_bar = self.scrollArea.verticalScrollBar()
        self.load_directory_to_ui()

    def load_directory_to_ui(self):
        keys = [key for key in self.workspace_json_file.keys() if key != "type" and key != "card-title" and key != "back"]
        for group_fname in keys:
            root = QTreeWidgetItem(self.treeWidget.invisibleRootItem(), [self.workspace_json_file[group_fname]["group-title"]])
            group = Group(self, group_fname, root, self.treeWidget.topLevelItem(len(self.groups)))
            group.group_is_deleted.connect(self.delete_group)
            self.layout.addWidget(group)
            group.load_data()
            group.activate_mainwindow.connect(self.activateWindow)
            self.scroll_area_bar.setMaximum(2147483647)
            self.scroll_area_bar.setValue(self.scroll_area_bar.maximum())
            self.groups.append(group)
    

    def create_new_group(self):
        group_fname = get_time()
        group_directory = self.workspace_json_file.file_directory + "\\" + group_fname
        root = QTreeWidgetItem(self.treeWidget.invisibleRootItem(), [f"Title"])
        self.workspace_json_file[group_fname] = init_group
        os.mkdir(group_directory)
        group = Group(self, group_fname, root, self.treeWidget.topLevelItem(len(self.groups)))
        group.group_is_deleted.connect(self.delete_group)
        self.layout.addWidget(group)
        self.scroll_area_bar.setMaximum(self.scroll_area_bar.maximum()+200)
        self.scroll_area_bar.setValue(self.scroll_area_bar.maximum())
        self.groups.append(group)
            

    def delete_group(self, group_fname):
        group_index = 0
        for i, group in enumerate(self.groups):
            if group.group_fname == group_fname:
                group_index = i
                break
        
        self.groups.pop(group_index)
        self.treeWidget.takeTopLevelItem(group_index) 


    def handle_item_clicked(self, item, column):
        index = self.treeWidget.indexOfTopLevelItem(item)
        if index != -1:
            self.scroll_area_bar.setValue(self.groups[index].y())
    
    def editing_title_finished(self, new_name):
        data = self.workspace_json_file.read_data()
        data["card-title"] = new_name
        self.workspace_json_file.save_data(data)
        self.title_label.title_label.setText(new_name)
        
