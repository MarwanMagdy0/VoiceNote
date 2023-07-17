from group import *

class FileView(QWidget):
    def __init__(self, workspace_file):
        super().__init__()
        self.workspace_json_file = HandleJsonFiles(workspace_file)
        self.groups = []
        self.init_ui()
        

    def init_ui(self):
        uic.loadUi(SCRIPT_DIRECTORY + "\\" + "ui\load.ui",self)
        self.treeWidget.itemClicked.connect(self.handle_item_clicked)
        self.add_new_group_button.clicked.connect(self.create_new_group)
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(lambda: self.add_new_group_button.setEnabled(True))
        self.setWindowIcon(QIcon(SCRIPT_DIRECTORY + "\\" + 'ui\\data\\icon.png'))
        self.layout = self.scrollArea.widget().layout()
        self.scrollArea.widget().setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.scroll_area_bar = self.scrollArea.verticalScrollBar()
        self.load_directory_to_ui()


    def load_directory_to_ui(self):
        for group_fname in self.workspace_json_file.keys():
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
        self.add_new_group_button.setEnabled(False)
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
        self.timer.start()
            

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
        
