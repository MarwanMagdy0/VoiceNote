from utiles import *

class VoiceNote(QWidget):
    def __init__(self, parent_group, group_fname, audio_fname):
        super().__init__(parent_group)
        uic.loadUi(SCRIPT_DIRECTORY + "\\" + "ui\\voice_note.ui",self)
        self.group_fname = group_fname
        self.audio_fname = audio_fname
        self.init_audio()
        self.play_pause_button.clicked.connect(self.toggle_playback)
        self.horizontalSlider.sliderMoved.connect(self.set_position)
        self.delete_button.clicked.connect(self.delete_widget)

    def init_audio(self):
        self.media_player = QMediaPlayer()
        audio_url = QUrl.fromLocalFile(USER_FILE_DIRECTORY + "\\" + self.group_fname + "\\" + self.audio_fname)
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
            self.play_pause_button.setIcon(QIcon(SCRIPT_DIRECTORY + "\\" + "ui\\data\\play.png"))
            self.timer.stop()
        else:
            self.media_player.play()
            self.play_pause_button.setIcon(QIcon(SCRIPT_DIRECTORY + "\\" + "ui\\data\\pause.png"))
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
    

    def delete_widget(self):
        if message_box():
            self.deleteLater()
            data = json_file.read_data()
            data[self.group_fname]["items"].remove(self.audio_fname)
            json_file.save_data(data)
            os.remove(USER_FILE_DIRECTORY + "\\" + self.group_fname + "\\" + self.audio_fname)


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
    def __init__(self, parent_dialoge, group_fname):
        super().__init__(parent_dialoge)
        self.group_fname = group_fname
        uic.loadUi(SCRIPT_DIRECTORY + "\\" + "ui\\record_audio.ui",self)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.audio_file_name = get_time() + ".wav"
        self.recorder = AudioRecorderThread(USER_FILE_DIRECTORY + "\\" + group_fname+ "\\"+ self.audio_file_name)
        self.record_button.clicked.connect(self.toggle_record_state)
        self.save_button.clicked.connect(self.save_audio)
        self.delete_button.clicked.connect(self.delete_method)
        self.recording = False
    
    def toggle_record_state(self):
        if not self.recording:
            self.recording = True
            self.record_button.setIcon(QIcon(SCRIPT_DIRECTORY + "\\" + "ui\\data\\red_mic.png"))
            self.save_button.setEnabled(False)
            self.delete_button.setEnabled(False)
            self.recorder.start()
        else:
            self.recording = False
            self.recorder.requestInterruption()
            self.record_button.setIcon(QIcon(SCRIPT_DIRECTORY + "\\" + "ui\\data\\mic.png"))
            self.save_button.setEnabled(True)
            self.delete_button.setEnabled(True)

    def save_audio(self):
        self.recorder.requestInterruption()
        self.recorder.save()
        self.audio_added.emit(self.audio_file_name)
        data = json_file.read_data()
        data[self.group_fname]["items"].append(self.audio_file_name)
        json_file.save_data(data)
        self.close()
    
    def delete_method(self):
        self.recorder.requestInterruption()
        self.recorder.frames.clear()
        self.delete_button.setEnabled(False)
        self.save_button.setEnabled(False)

