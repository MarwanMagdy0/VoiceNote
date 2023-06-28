from PyQt5.QtWidgets import QWidget, QLineEdit, QVBoxLayout, QLabel, QDialog, QApplication
from PyQt5.QtGui import QPixmap, QImage, QIcon
from PyQt5.QtCore import Qt, QTimer, QUrl
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
import os
from PIL import Image
from PyQt5 import uic
import pyaudio
import wave
import time

class VoiceNote(QWidget):
	def __init__(self, parent_group, path):
		super().__init__(parent_group)
		uic.loadUi("ui/voice_note.ui",self)
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


class EditableLabel(QLabel):
	finished = pyqtSignal(str)
	def __init__(self, existing_label):
		super().__init__("Title")
		self.setGeometry(existing_label.geometry())
		layout = existing_label.parentWidget().layout()
		layout.replaceWidget(existing_label, self)

		existing_label.deleteLater()
		self.line_edit = QLineEdit("")
		self.line_edit.hide()
		self.line_edit.editingFinished.connect(self.finish_editing)

	def mouseDoubleClickEvent(self, event):
		if self.line_edit.isHidden():
			self.line_edit.setText(self.text())
			self.line_edit.setParent(self.parentWidget())
			self.line_edit.setGeometry(self.geometry())
			self.line_edit.show()
			self.line_edit.setFocus()
			self.hide()
		else:
			self.setText(self.line_edit.text())
			self.line_edit.hide()
			self.show()
	
	def finish_editing(self):
		"""
		TODO
		dont forget to check if the temp folder is exist and if not create it and update the ui with the new temp group
		"""
		new_text = self.line_edit.text()
		self.line_edit.hide()
		self.setText(new_text)
		self.show()
		self.finished.emit(new_text)
		print("loss focus")


class Group(QWidget):
	on_group_change = pyqtSignal(list)
	def __init__(self, main_window, main_directory : str, group_fname : str, group_data):
		self.main_window = main_window
		super().__init__(main_window)
		self.init_ui()
		self.items = 0
		self.group_fname = group_fname
		self.group_directory = main_directory+ "//" + group_fname
		self.group_data = group_data
		self.group_name = group_data["group-name"]

	def init_ui(self):
		uic.loadUi("ui/group.ui",self)
		self.title_label = EditableLabel(self.title_label)
		self.title_label.finished.connect(self.editing_text_finished)
		self.add_button.clicked.connect(self.add_button_method)

	def add_button_method(self):
		add_items_window = AddDialoge(self, self.group_directory, str(self.items))
		add_items_window.voice_record_added.connect(self.update_audio)
		add_items_window.setWindowModality(Qt.ApplicationModal)
		add_items_window.show()

	def update_audio(self, fname):
		self.add_widget(VoiceNote(self, fname))
		self.on_group_change.emit([self, ".wav"])	

	def load_data(self):
		self.title_label.setText(self.group_name)
		for key, values in self.group_data.items():
			# TODO check if it is str as text will have diffrent fonts and diffrent sizes {"text":{"font-size":5, "data":"helloo", "font-type":"italic", "color":"#000000", "background-color":#ffffff}}
			if (values.endswith(".wav") or values.endswith(".mp3")) and not key == "group-name":
				self.add_widget(VoiceNote(self, self.group_directory  + "//" +values))

			if (values.endswith(".png") or values.endswith(".jpg")) and not key == "group-name":
				self.add_widget(ImageWidget(self, self.group_directory  + "//" +values))
	
	def add_widget(self, widget):
		self.box_vlayout.addWidget(widget)
		self.items += 1

	def editing_text_finished(self, new_group_name):
		self.group_name = new_group_name
		self.on_group_change.emit([self, ""])	

	


class ImageWidget(QWidget):
	def __init__(self, parent_group, file):
		super().__init__(parent_group)
		uic.loadUi("ui/image.ui",self)
		self.set_img(file)
	
	def set_img(self, path):
		pixmap = QPixmap(path)
		self.image.setPixmap(pixmap)


class AddDialoge(QDialog):
	voice_record_added = pyqtSignal(str)
	def __init__(self, parent_group, group_directory, item_index):
		super().__init__(parent_group)
		self.group_directory = group_directory
		self.item_index = item_index
		uic.loadUi("ui/add_items_to_group.ui",self)
		self.record_audio_button.clicked.connect(self.record_audio_method)

	def record_audio_method(self):
		audio_recorder = RecordAudio(self, self.group_directory, self.item_index)
		audio_recorder.audio_added.connect(self.audio_added)
		audio_recorder.setWindowModality(Qt.ApplicationModal)
		audio_recorder.show()
		self.close()
	
	def audio_added(self, fname):
		self.voice_record_added.emit(fname)
	def add_clipboard_image(self):
		clipboard = QApplication.clipboard()
		mime_data = clipboard.mimeData()

		if mime_data.hasImage():
			image = mime_data.imageData()
			pixmap = QPixmap.fromImage(image)
			self.label.setPixmap(pixmap)


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
	def __init__(self, parent_dialoge, group_directory, item_index):
		super().__init__(parent_dialoge)
		uic.loadUi("ui/record_audio.ui",self)
		self.audio_path = group_directory+ "//"+item_index + ".wav"
		self.recorder = AudioRecorderThread(self.audio_path)
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
		self.close()
		self.audio_added.emit(self.audio_path)
	
	def delete_method(self):
		self.recorder.requestInterruption()
		self.recorder.frames.clear()
		self.delete_button.setEnabled(False)
		self.save_button.setEnabled(False)


	
