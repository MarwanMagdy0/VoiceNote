from utiles import *
DEFAULT_FONT = "Arial,16,-1,5,50,0,0,0,0,0,Regular"
initial_font = QFont()
initial_font.fromString(DEFAULT_FONT)

class AddText(QDialog):
    font_changed = pyqtSignal(str, str, bool)
    def __init__(self, parent):
        super().__init__(parent)
        self.workspace_json_file = parent.workspace_json_file
        uic.loadUi(SCRIPT_DIRECTORY + "/" + "ui/add_text.ui", self)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.font_button.clicked.connect(self.choose_font)
        self.save_button.clicked.connect(self.save_text)
        self.text_editor.setFont(initial_font)
        self.text_font = initial_font
    
    def choose_font(self):
        self.text_font, ok = QFontDialog.getFont(initial_font)
        if ok:
            self.text_editor.setFont(self.text_font)
    
    def save_text(self):
        self.font_changed.emit(self.text_font.toString(), self.text_editor.toPlainText(), self.checkbox.isChecked())
        self.close()
    
    def closeEvent(self, event):
        self.font_changed.emit("null", "null", False)
        event.accept()


class NormalText(QWidget):
    def __init__(self, parent_group, text, font_str, group_fname, ref2text):
        super().__init__()
        self.workspace_json_file = parent_group.workspace_json_file
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.ref2text = ref2text
        self.group_fname = group_fname
        layout = QVBoxLayout(self)
        self.label = QLabel(text)
        font = QFont()
        font.fromString(font_str)
        self.label.setFont(font)
        layout.addWidget(self.label)
    
    def mouseDoubleClickEvent(self, event):
        edit_text_window = EditText(self, self.label.text(), self.label.font(), self.group_fname, self.ref2text)
        alignment = self.label.alignment()
        if alignment == Qt.AlignCenter:
            edit_text_window.checkbox.setChecked(True)

        edit_text_window.text_is_deleted.connect(self.deleteLater)
        edit_text_window.setWindowModality(Qt.ApplicationModal)
        edit_text_window.new_text_saved.connect(self.update_text_params)
        edit_text_window.show()
    
    def update_text_params(self, text, font_str, is_centered):
        self.label.setText(text)
        if is_centered:
            self.label.setAlignment(Qt.AlignCenter)
        else:
            self.label.setAlignment(Qt.AlignLeft)
        font = QFont()
        font.fromString(font_str)
        self.label.setFont(font)
        data = self.workspace_json_file.read_data()
        data[self.group_fname]["refrences"][self.ref2text] = {"text":"", "font":"", "is-centered":False}
        data[self.group_fname]["refrences"][self.ref2text]["text"] = text
        data[self.group_fname]["refrences"][self.ref2text]["font"] = font_str
        data[self.group_fname]["refrences"][self.ref2text]["is-centered"] = is_centered
        self.workspace_json_file.save_data(data)

class EditText(QDialog):
    new_text_saved = pyqtSignal(str, str, bool)
    text_is_deleted = pyqtSignal()
    def __init__(self, parent_group, text, text_font, group_fname, ref2text):
        super().__init__(parent_group)
        self.text_font = text_font
        self.ref2text = ref2text
        self.group_fname = group_fname
        self.workspace_json_file = parent_group.workspace_json_file
        uic.loadUi(SCRIPT_DIRECTORY + "/" + "ui/edit_text.ui", self)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.text_editor.setText(text)
        self.text_editor.setFont(self.text_font)
        self.font_button.clicked.connect(self.choose_font)
        self.save_button.clicked.connect(self.save_text)
        self.delete_button.clicked.connect(self.delete_text)
    
    def choose_font(self):
        self.text_font, ok = QFontDialog.getFont(self.text_font)
        if ok:
            self.text_editor.setFont(self.text_font)
    
    def save_text(self):
        self.new_text_saved.emit(self.text_editor.toPlainText(), self.text_font.toString(), self.checkbox.isChecked())
        self.close()
    
    def delete_text(self):
        if message_box():
            data = self.workspace_json_file.read_data()
            print(self.ref2text)
            data[self.group_fname]["refrences"].pop(self.ref2text)
            data[self.group_fname]["items"].remove(self.ref2text)
            self.workspace_json_file.save_data(data)
            self.text_is_deleted.emit()
            self.close()