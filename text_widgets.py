from utiles import *


DEFAULT_FONT = "Arial,16,-1,5,50,0,0,0,0,0,Regular"
initial_font = QFont()
initial_font.fromString(DEFAULT_FONT)

class AddText(QDialog):
    font_changed = pyqtSignal(str, str)
    def __init__(self, parent):
        super().__init__(parent)
        uic.loadUi(SCRIPT_DIRECTORY + "\\" + "ui\\add_text.ui", self)
        self.font_button.clicked.connect(self.choose_font)
        self.save_button.clicked.connect(self.save_text)
        self.text_editor.setFont(initial_font)
        self.text_font = initial_font
    
    def choose_font(self):
        self.text_font, ok = QFontDialog.getFont(initial_font)
        if ok:
            self.text_editor.setFont(self.text_font)
    
    def save_text(self):
        self.font_changed.emit(self.text_font.toString(), self.text_editor.toPlainText())
        self.close()

class NormalText(QWidget):
    def __init__(self, text, font_str, group_directory):
        super().__init__()
        self.group_directory = group_directory
        layout = QVBoxLayout(self)
        self.label = QLabel(text)
        self.font = QFont()
        self.font.fromString(font_str)
        self.label.setFont(self.font)
        self.label.setAlignment(Qt.AlignLeft)
        layout.addWidget(self.label)
    
    def mouseDoubleClickEvent(self, event):
        edit_text_window = EditText(self, self.label.text(), self.label.font())
        edit_text_window.setWindowModality(Qt.ApplicationModal)
        edit_text_window.new_text_saved.connect(self.update_text_params)
        edit_text_window.show()
    
    def update_text_params(self, text, font_str):
        self.label.setText(text)
        self.label = QLabel(text)
        self.font = QFont()
        self.font.fromString(font_str)
        data = json_file.read_data()
        data[self.group_directory]["items"].append({"text":text, "font":font_str})
        json_file.save_data(data)
        pass

class EditText(QDialog):
    new_text_saved = pyqtSignal(str, str)
    def __init__(self, parent, text, font):
        super().__init__(parent)
        uic.loadUi(SCRIPT_DIRECTORY + "\\" + "ui\\edit_text.ui", self)
        self.parent_label = parent
        self.delete_button.clicked.connect(self.delete_text)
        self.text_editor.setText(text)
        self.text_editor.setFont(font)
        self.text_font = font
        self.font_button.clicked.connect(self.choose_font)
        self.save_button.clicked.connect(self.save_text)
        # TODO delete button connect to self.delete_text()
        self.text_editor.setFont(initial_font)
    
    def choose_font(self):
        self.text_font, ok = QFontDialog.getFont(self.text_font)
        if ok:
            self.text_editor.setFont(self.text_font)
    
    def save_text(self):
        self.new_text_saved.emit(self.text_editor.toPlainText(), self.text_font.toString())
        # TODO json file saving text 
        self.close()
    
    def delete_text(self):
        # TODO json file deletting text 
        pass