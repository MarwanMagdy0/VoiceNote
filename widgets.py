from PyQt5.QtWidgets import QWidget, QLineEdit, QVBoxLayout, QLabel, QDialog, QApplication, QTreeWidgetItem, QFontDialog
from PyQt5.QtGui import QPixmap, QImage, QIcon, QFont
from PyQt5.QtCore import Qt, QTimer, QUrl
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
import os
from PIL import Image
from PyQt5 import uic
import pyaudio
import wave
from utiles import *


class VoiceNote(QWidget):
    def __init__(self, parent_group, path):
        super().__init__(parent_group)
        uic.loadUi(SCRIPT_DIRECTORY + "//" + "ui//voice_note.ui",self)
        self.path = path
        self.init_audio()
        self.pushButton.clicked.connect(self.toggle_playback)
        self.horizontalSlider.sliderMoved.connect(self.set_position)

    def init_audio(self):
        self.media_player = QMediaPlayer()
        audio_url = QUrl.fromLocalFile(self.path)
        self.media_player.setMedia(QMediaContent(audio_url))
        self.timer = QTimer(self)
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.update_slider)
        self.media_player.durationChanged.connect(self.update_duration_label)
        self.horizontalSlider.wheelEvent = self.ignore_wheel

    def ignore_wheel(self, event):
        event.ignore()
    def set_position(self, position):
        self.media_player.setPosition(position)

    def toggle_playback(self):
        if self.media_player.state() == QMediaPlayer.PlayingState:
            self.media_player.pause()
            self.pushButton.setIcon(QIcon("ui/data/play.png"))
            self.timer.stop()
        else:
            self.media_player.play()
            self.pushButton.setIcon(QIcon("ui/data/pause.png"))
            self.timer.start()

    def update_slider(self):
        if self.media_player.duration() > 0:
            self.horizontalSlider.setMaximum(self.media_player.duration())
            self.horizontalSlider.setValue(self.media_player.position())
            self.update_duration_label()

    def update_duration_label(self):
            duration = self.media_player.duration() // 1000
            elapsed = self.media_player.position() // 1000
            remaining = duration - elapsed
            remaining_minutes = remaining // 60
            remaining_seconds = remaining % 60
            self.duration_label.setText(f"{remaining_minutes}:{remaining_seconds:02}")


class EditableLabel(QWidget):
    title_updated = pyqtSignal(str)
    def __init__(self, group_object, title):
        super().__init__(group_object)
        uic.loadUi(SCRIPT_DIRECTORY + "//" + "ui/label_edit.ui",self)
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


class ImageWidget(QWidget):
    def __init__(self, parent_group):
        super().__init__(parent_group)
        uic.loadUi(SCRIPT_DIRECTORY + "//" + "ui/image.ui",self)
    
    def set_img(self, image_from_object):
        pixmap = QPixmap.fromImage(image_from_object)
        self.image.setPixmap(pixmap)
    
    def load_img(self, path):
        pixmap = QPixmap(path)
        self.image.setPixmap(pixmap)


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
        uic.loadUi(SCRIPT_DIRECTORY + "//" + "ui/group.ui",self)
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
        voice_object = VoiceNote(self,self.group_directory+ "//" + audio_name)
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
            image.save(self.group_directory+ "//" + image_fname, "PNG")
            self.add_widget(img_widget)
            data = json_file.read_data()
            data[self.group_directory]["items"].append(image_fname)
            json_file.save_data(data)


    def add_text(self, font, text):
        text_font = QFont()
        text_font.fromString(font)
        QTreeWidgetItem(self.parent_tree, [text])
        label = QLabel(self, text=text)
        label.setFont(text_font)
        label.setAlignment(Qt.AlignLeft)
        self.add_widget(label)
        data = json_file.read_data()
        data[self.group_directory]["items"].append({"text":text, "font":font})
        json_file.save_data(data)


    def load_data(self):
        self.title_label.title_label.setText(self.group_title)
        for item in json_file[self.group_directory]["items"]:
            if type(item) == dict:
                QTreeWidgetItem(self.parent_tree, [item["text"]])
                text_font = QFont()
                text_font.fromString(item["font"])
                label = QLabel(self, text=item["text"])
                label.setFont(text_font)
                label.setAlignment(Qt.AlignLeft)
                self.add_widget(label)
            
            elif (item.endswith(".wav") or item.endswith(".mp3")):
                QTreeWidgetItem(self.parent_tree, [item])
                voice_object = VoiceNote(self, self.group_directory + "//" + item)
                self.add_widget(voice_object)

            elif (item.endswith(".png") or item.endswith(".jpg")):
                QTreeWidgetItem(self.parent_tree, [item])
                img_widget = ImageWidget(self)
                img_widget.load_img(self.group_directory  + "//" +item)
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
        uic.loadUi(SCRIPT_DIRECTORY + "//" + "ui/add_items_to_group.ui",self)
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

DEFAULT_FONT = "Arial,16,-1,5,50,0,0,0,0,0,Regular"
initial_font = QFont()
initial_font.fromString(DEFAULT_FONT)

class AddText(QDialog):
    font_changed = pyqtSignal(str, str)
    def __init__(self, parent):
        super().__init__(parent)
        uic.loadUi(SCRIPT_DIRECTORY + "//" + "ui/add_text.ui", self)
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


class AudioRecorderThread(QThread):
    audio_finished = pyqtSignal()

    def __init__(self, fname):
        super().__init__()
        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.frames = []
        self.fname = fname
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 44100
        self.CHUNK = 1024
        self.stream = self.audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=self.CHUNK)

    def run(self):
        while not self.isInterruptionRequested():
            data = self.stream.read(self.CHUNK)
            self.frames.append(data)
            
    def save(self):
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()
        wave_file = wave.open(f"{self.fname}", 'wb')
        wave_file.setnchannels(1)
        wave_file.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
        wave_file.setframerate(44100)
        wave_file.writeframes(b''.join(self.frames))
        wave_file.close()


class RecordAudio(QDialog):
    audio_added = pyqtSignal(str)
    def __init__(self, parent_dialoge, group_directory):
        super().__init__(parent_dialoge)
        self.group_directory = group_directory
        uic.loadUi(SCRIPT_DIRECTORY + "//" + "ui/record_audio.ui",self)
        self.audio_file_name = get_time() + ".wav"
        self.recorder = AudioRecorderThread(group_directory+ "//"+ self.audio_file_name)
        self.record_button.clicked.connect(self.toggle_record_state)
        self.save_button.clicked.connect(self.save_audio)
        self.delete_button.clicked.connect(self.delete_method)
        self.recording = False
    
    def toggle_record_state(self):
        if not self.recording:
            self.recording = True
            self.record_button.setIcon(QIcon("ui/data/red_mic.png"))
            self.save_button.setEnabled(False)
            self.delete_button.setEnabled(False)
            self.recorder.start()
        else:
            self.recording = False
            self.recorder.requestInterruption()
            self.record_button.setIcon(QIcon("ui/data/mic.png"))
            self.save_button.setEnabled(True)
            self.delete_button.setEnabled(True)

    def save_audio(self):
        self.recorder.requestInterruption()
        self.recorder.save()
        self.audio_added.emit(self.audio_file_name)
        data = json_file.read_data()
        data[self.group_directory]["items"].append(self.audio_file_name)
        json_file.save_data(data)
        self.close()
    
    def delete_method(self):
        self.recorder.requestInterruption()
        self.recorder.frames.clear()
        self.delete_button.setEnabled(False)
        self.save_button.setEnabled(False)

