from vocie_widgets import *
from image_widgets import *
from text_widgets  import * 

class Group(QWidget):
    activate_mainwindow = pyqtSignal()
    group_is_deleted    = pyqtSignal(str)
    def __init__(self, main_window, group_fname, root, parent_tree):
        super().__init__(main_window)
        self.parent_tree =parent_tree
        self.root = root
        self.main_window = main_window
        self.group_fname = group_fname
        self.group_title = json_file[self.group_fname]["group-title"]
        self.init_ui()


    def init_ui(self):
        uic.loadUi(SCRIPT_DIRECTORY + "\\" + "ui\\group.ui",self)
        self.title_label = EditableLabel(self, self.group_title)
        self.label_layout.addWidget(self.title_label)
        self.title_label.title_updated.connect(self.editing_title_finished)
        self.add_button.clicked.connect(self.add_button_method)
        self.delete_group_button.clicked.connect(self.delete_group_method)


    def add_button_method(self):
        add_items_window = AddDialoge(self, self.group_fname)
        add_items_window.voice_record_added.connect(self.add_record)
        add_items_window.img_from_clib_added.connect(self.add_image)
        add_items_window.separator_is_added.connect(self.add_separator)
        add_items_window.font_changed.connect(self.add_text)
        add_items_window.setWindowModality(Qt.ApplicationModal)
        add_items_window.show()


    def add_record(self, audio_fname):
        QTreeWidgetItem(self.parent_tree, [audio_fname])
        voice_object = VoiceNote(self, self.group_fname, audio_fname)
        self.add_widget(voice_object)


    def add_image(self):
        clipboard = QApplication.clipboard()
        mime_data = clipboard.mimeData()
        if mime_data.hasImage():
            image_fname = get_time() + ".png"
            QTreeWidgetItem(self.parent_tree, [image_fname])
            image = mime_data.imageData()
            img_widget = ImageWidget(self)
            img_widget.set_img(image)
            image.save(USER_FILE_DIRECTORY + "\\" + self.group_fname+ "\\" + image_fname, "PNG")
            self.add_widget(img_widget)
            data = json_file.read_data()
            data[self.group_fname]["items"].append(image_fname)
            json_file.save_data(data)


    def add_text(self, font, text, is_centered):
        if font == "null" and text == "null" and is_centered == False:
            self.activate_mainwindow.emit()
            return
        ref2text = get_time() + ".ref"
        QTreeWidgetItem(self.parent_tree, [text])
        normal_text = NormalText(text, font, self.group_fname, ref2text)
        if is_centered:
            normal_text.label.setAlignment(Qt.AlignCenter)
        self.add_widget(normal_text)
        data = json_file.read_data()
        data[self.group_fname]["items"].append(ref2text)
        data[self.group_fname]["refrences"][ref2text] = {"text":text, "font":font, "is-centered":is_centered}
        json_file.save_data(data)

    
    def add_separator(self):
        separator_name = get_time() + ".separator"
        self.add_widget(QHSeparationLine(self.group_fname, separator_name))
        data = json_file.read_data()
        data[self.group_fname]["items"].append(separator_name)
        json_file.save_data(data)
    

    def load_data(self):
        self.title_label.title_label.setText(self.group_title)
        for item in json_file[self.group_fname]["items"]:
            if item.endswith(".ref"):
                text = json_file[self.group_fname]["refrences"][item]["text"]
                font = json_file[self.group_fname]["refrences"][item]["font"]
                is_centered = json_file[self.group_fname]["refrences"][item]["is-centered"]
                QTreeWidgetItem(self.parent_tree, [text])
                normal_text = NormalText(text, font, self.group_fname, item)
                if is_centered:
                    normal_text.label.setAlignment(Qt.AlignCenter)
                self.add_widget(normal_text)
            
            elif (item.endswith(".wav") or item.endswith(".mp3")):
                QTreeWidgetItem(self.parent_tree, [item])
                voice_object = VoiceNote(self, self.group_fname, item)
                self.add_widget(voice_object)

            elif (item.endswith(".png") or item.endswith(".jpg")):
                QTreeWidgetItem(self.parent_tree, [item])
                img_widget = ImageWidget(self)
                img_widget.load_img(USER_FILE_DIRECTORY + "\\" + self.group_fname  + "\\" +item)
                self.add_widget(img_widget)
            
            elif item.endswith(".separator"):
                separator_object = QHSeparationLine(self.group_fname, item)
                self.add_widget(separator_object)
    

    def add_widget(self, widget):
        self.box_vlayout.addWidget(widget)
        self.activate_mainwindow.emit()


    def editing_title_finished(self, new_group_title):
        self.root.setText(0, new_group_title)
        self.group_title = new_group_title
        data = json_file.read_data()
        data[self.group_fname]["group-title"] = new_group_title
        json_file.save_data(data)
        self.title_label.title_label.setText(new_group_title)
    
    def delete_group_method(self):
        if message_box():
            shutil.rmtree(USER_FILE_DIRECTORY + "\\" + self.group_fname)
            data = json_file.read_data()
            data.pop(self.group_fname)
            json_file.save_data(data)
            self.deleteLater()
            self.group_is_deleted.emit(self.group_fname)

class AddDialoge(QDialog):
    voice_record_added  = pyqtSignal(str)
    img_from_clib_added = pyqtSignal()
    font_changed = pyqtSignal(str, str, bool)
    separator_is_added = pyqtSignal()
    def __init__(self, parent_group, group_fname):
        super().__init__(parent_group)
        self.group_fname = group_fname
        uic.loadUi(SCRIPT_DIRECTORY + "\\" + "ui\\add_items_to_group.ui",self)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.img_from_clib.setLayoutDirection(Qt.RightToLeft)
        self.img_from_camera.setLayoutDirection(Qt.RightToLeft)
        self.record_audio_button.setLayoutDirection(Qt.RightToLeft)
        self.add_text_button.setLayoutDirection(Qt.RightToLeft)
        self.separator_button.setLayoutDirection(Qt.RightToLeft)

        self.img_from_clib.clicked.connect(self.add_clipboard_image)
        self.img_from_camera.clicked.connect(self.add_camera_img_method)
        self.record_audio_button.clicked.connect(self.record_audio_method)
        self.add_text_button.clicked.connect(self.add_text_method)
        self.separator_button.clicked.connect(self.add_separator_method)

    def record_audio_method(self):
        self.close()
        audio_recorder = RecordAudio(self, self.group_fname)
        audio_recorder.audio_added.connect(lambda audio_name: self.voice_record_added.emit(audio_name))
        audio_recorder.setWindowModality(Qt.ApplicationModal)
        audio_recorder.show()
    
    def add_clipboard_image(self):
        self.img_from_clib_added.emit()
        self.close()
    
    def add_text_method(self):
        add_text = AddText(self)
        add_text.font_changed.connect(lambda font, text, is_centered : self.font_changed.emit(font, text, is_centered))
        add_text.setWindowModality(Qt.ApplicationModal)
        add_text.show()
        self.close()

    def add_camera_img_method(self):
        self.close()
    
    def add_separator_method(self):
        self.separator_is_added.emit()
        self.close()



class EditableLabel(QWidget):
    title_updated = pyqtSignal(str)
    def __init__(self, group_object, title):
        super().__init__(group_object)
        uic.loadUi(SCRIPT_DIRECTORY + "\\" + "ui\\label_edit.ui",self)
        self.line_edit.editingFinished.connect(self.finish_editing)
        self.line_edit.hide()
    def mouseDoubleClickEvent(self, event):
        if self.line_edit.isHidden():
            self.title_label.hide()
            self.line_edit.setText(self.title_label.text())
            self.line_edit.show()
            self.line_edit.setFocus()
        else:
            self.title_label.setText(self.line_edit.text())
            self.title_label.show()
            self.line_edit.hide()
    
    def finish_editing(self):
        new_text = self.line_edit.text()
        self.line_edit.hide()
        self.title_label.setText(new_text)
        self.title_label.show()
        self.title_updated.emit(new_text)