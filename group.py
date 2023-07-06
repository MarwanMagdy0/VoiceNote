from vocie_widgets import *
from image_widgets import *
from text_widgets  import * 

class Group(QWidget):
    activate_mainwindow = pyqtSignal()
    def __init__(self, main_window, group_directory, root, parent_tree):
        super().__init__(main_window)
        self.parent_tree =parent_tree
        self.root = root
        self.main_window = main_window
        self.group_directory = group_directory
        self.group_title = json_file[self.group_directory]["group-title"]
        self.init_ui()


    def init_ui(self):
        uic.loadUi(SCRIPT_DIRECTORY + "\\" + "ui\\group.ui",self)
        self.title_label = EditableLabel(self, self.group_title)
        self.label_layout.addWidget(self.title_label)
        self.title_label.title_updated.connect(self.editing_title_finished)
        self.add_button.clicked.connect(self.add_button_method)


    def add_button_method(self):
        add_items_window = AddDialoge(self, self.group_directory)
        add_items_window.voice_record_added.connect(self.add_record)
        add_items_window.img_from_clib_added.connect(self.add_image)
        add_items_window.font_changed.connect(self.add_text)
        add_items_window.setWindowModality(Qt.ApplicationModal)
        add_items_window.show()


    def add_record(self, audio_name):
        QTreeWidgetItem(self.parent_tree, [audio_name])
        voice_object = VoiceNote(self,self.group_directory+ "\\" + audio_name)
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
            image.save(self.group_directory+ "\\" + image_fname, "PNG")
            self.add_widget(img_widget)
            data = json_file.read_data()
            data[self.group_directory]["items"].append(image_fname)
            json_file.save_data(data)


    def add_text(self, font, text):
        """
        TODO we need to separate text to be a stand alone class
        """
        QTreeWidgetItem(self.parent_tree, [text])
        normal_text = NormalText(text, font, self.group_directory)
        self.add_widget(normal_text)
        data = json_file.read_data()
        data[self.group_directory]["items"].append({"text":text, "font":font})
        json_file.save_data(data)
    

    def load_data(self):
        self.title_label.title_label.setText(self.group_title)
        for item in json_file[self.group_directory]["items"]:
            if type(item) == dict:
                text = item["text"]
                font = item["font"]
                QTreeWidgetItem(self.parent_tree, [text])
                normal_text = NormalText(text, font, self.group_directory)
                self.add_widget(normal_text)
            
            elif (item.endswith(".wav") or item.endswith(".mp3")):
                QTreeWidgetItem(self.parent_tree, [item])
                voice_object = VoiceNote(self, self.group_directory + "\\" + item)
                self.add_widget(voice_object)

            elif (item.endswith(".png") or item.endswith(".jpg")):
                QTreeWidgetItem(self.parent_tree, [item])
                img_widget = ImageWidget(self)
                img_widget.load_img(self.group_directory  + "\\" +item)
                self.add_widget(img_widget)
    

    def add_widget(self, widget):
        self.box_vlayout.addWidget(widget)
        self.activate_mainwindow.emit()


    def editing_title_finished(self, new_group_title):
        self.root.setText(0, new_group_title)
        self.group_title = new_group_title
        data = json_file.read_data()
        data[self.group_directory]["group-title"] = new_group_title
        json_file.save_data(data)
        self.title_label.title_label.setText(new_group_title)



class AddDialoge(QDialog):
    voice_record_added  = pyqtSignal(str)
    img_from_clib_added = pyqtSignal()
    font_changed = pyqtSignal(str, str)
    def __init__(self, parent_group, group_file_name):
        super().__init__(parent_group)
        self.group_file_name = group_file_name
        uic.loadUi(SCRIPT_DIRECTORY + "\\" + "ui\\add_items_to_group.ui",self)
        self.img_from_clib.clicked.connect(self.add_clipboard_image)
        self.img_from_camera.clicked.connect(self.add_camera_img_method)
        self.record_audio_button.clicked.connect(self.record_audio_method)
        self.add_text_button.clicked.connect(self.add_text_method)

    def record_audio_method(self):
        self.close()
        audio_recorder = RecordAudio(self, self.group_file_name)
        audio_recorder.audio_added.connect(lambda audio_name: self.voice_record_added.emit(audio_name))
        audio_recorder.setWindowModality(Qt.ApplicationModal)
        audio_recorder.show()
    
    def add_clipboard_image(self):
        self.img_from_clib_added.emit()
        self.close()
    
    def add_text_method(self):
        add_text = AddText(self)
        add_text.font_changed.connect(lambda font, text : self.font_changed.emit(font, text))
        add_text.setWindowModality(Qt.ApplicationModal)
        add_text.show()
        self.close()

    def add_camera_img_method(self):
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