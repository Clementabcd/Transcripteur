from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QFileDialog,
    QTextEdit,
    QProgressBar,
    QFrame,
    QMessageBox,
    QComboBox,
    QDialog,
)

from PySide6.QtCore import Qt

from worker import TranscriptionWorker

from utils import (
    export_txt,
    export_srt,
    export_vtt,
    export_json
)

from utils import load_config, save_config


class DropArea(QFrame):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.parent = parent

        self.setAcceptDrops(True)

        self.setObjectName("dropArea")

        layout = QVBoxLayout(self)

        self.label = QLabel(
            "📁\n\nDéposez un fichier audio ou vidéo\n\nou cliquez ici"
        )

        self.label.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.label)


    def mousePressEvent(self, event):

        self.parent.select_file()


    def dragEnterEvent(self, event):

        if event.mimeData().hasUrls():

            event.acceptProposedAction()


    def dropEvent(self, event):

        files = event.mimeData().urls()

        if files:

            path = files[0].toLocalFile()

            self.parent.load_file(path)



class SettingsDialog(QDialog):


    def __init__(self, config, parent=None):

        super().__init__(parent)


        self.config = config


        self.setWindowTitle(
            "Paramètres"
        )


        self.resize(
            320,
            250
        )


        layout = QVBoxLayout(self)



        layout.addWidget(
            QLabel("Modèle Whisper")
        )


        self.model = QComboBox()


        self.model.addItems(
            [
                "large-v3-turbo",
                "medium",
                "small",
                "base"
            ]
        )


        index = self.model.findText(
            self.config["model"]
        )


        if index >= 0:

            self.model.setCurrentIndex(
                index
            )


        layout.addWidget(
            self.model
        )



        layout.addWidget(
            QLabel("Langue")
        )


        self.language = QComboBox()


        self.language.addItems(
            [
                "fr",
                "en",
                "de",
                "es"
            ]
        )


        self.language.setCurrentText(
            self.config["language"]
        )


        layout.addWidget(
            self.language
        )



        save = QPushButton(
            "Sauvegarder"
        )


        save.clicked.connect(
            self.save
        )


        layout.addWidget(
            save
        )



    def save(self):


        self.config["model"] = (
            self.model.currentText()
        )


        self.config["language"] = (
            self.language.currentText()
        )


        save_config(
            self.config
        )


        self.close()



class MainWindow(QWidget):


    def __init__(self):

        super().__init__()


        self.setWindowTitle(
            "EchoScript"
        )

        self.resize(
            700,
            600
        )


        self.file_path = None

        self.worker = None

        self.config = load_config()


        self.init_ui()

        self.apply_style()


    def closeEvent(self, event):

        from PySide6.QtWidgets import QApplication

        QApplication.quit()

        event.accept()



    def init_ui(self):


        main = QVBoxLayout()

        main.setSpacing(12)


        header = QHBoxLayout()


        title = QLabel(
            "🎙 EchoScript"
        )

        title.setObjectName(
            "title"
        )


        settings = QPushButton(
            "⚙"
        )

        settings.clicked.connect(
            self.open_settings
        )


        header.addWidget(title)

        header.addStretch()

        header.addWidget(settings)



        main.addLayout(
            header
        )


        self.drop = DropArea(
            self
        )


        main.addWidget(
            self.drop
        )


        self.file_label = QLabel()

        self.file_label.hide()


        main.addWidget(
            self.file_label
        )


        self.transcribe = QPushButton(
            "Transcrire"
        )


        self.transcribe.hide()


        self.transcribe.clicked.connect(
            self.start
        )


        main.addWidget(
            self.transcribe
        )



        self.progress = QProgressBar()

        self.progress.hide()


        main.addWidget(
            self.progress
        )



        self.status = QLabel()

        self.status.hide()


        main.addWidget(
            self.status
        )



        self.output = QTextEdit()

        self.output.hide()


        main.addWidget(
            self.output
        )


        export = QHBoxLayout()


        self.format_box = QComboBox()

        self.format_box.addItems(
            [
                "TXT",
                "SRT",
                "VTT",
                "JSON"
            ]
        )

        self.format_box.hide()



        self.save = QPushButton(
            "💾 Enregistrer"
        )


        self.save.hide()


        self.save.clicked.connect(
            self.save_file
        )


        export.addWidget(
            self.format_box
        )


        export.addWidget(
            self.save
        )


        main.addLayout(
            export
        )



        self.setLayout(
            main
        )


    def select_file(self):

        file, _ = QFileDialog.getOpenFileName(
            self,
            "Choisir un fichier",
            "",
            "Audio/Vidéo (*.mp3 *.wav *.m4a *.mp4)"
        )


        if file:

            self.load_file(file)



    def load_file(self, path):

        self.file_path = path


        self.drop.label.setText(
            "🎵\n\n" +
            path.split("/")[-1]
        )


        self.file_label.setText(
            path
        )

        self.file_label.show()


        self.transcribe.show()



    def start(self):


        self.transcribe.hide()


        self.progress.show()

        self.status.show()


        self.worker = TranscriptionWorker(
            self.file_path,
            self.config
        )


        self.worker.progress.connect(
            self.progress.setValue
        )


        self.worker.status.connect(
            self.status.setText
        )


        self.worker.finished.connect(
            self.done
        )


        self.worker.error.connect(
            self.error
        )


        self.worker.start()



    def done(self, data):


        self.status.setText(
            "✅ Transcription terminée"
        )


        self.result_data = data


        self.output.show()


        text = export_txt(
            data
        )


        self.output.setText(
            text
        )


        self.format_box.show()

        self.save.show()



    def error(self, msg):

        QMessageBox.critical(
            self,
            "Erreur",
            msg
        )



    def save_file(self):


        fmt = self.format_box.currentText()


        exporters = {

            "TXT": export_txt,

            "SRT": export_srt,

            "VTT": export_vtt,

            "JSON": export_json

        }


        content = exporters[fmt](
            self.result_data
        )


        extension = fmt.lower()


        file, _ = QFileDialog.getSaveFileName(

            self,

            "Sauvegarder la transcription",

            f"transcription.{extension}",

            f"{fmt} (*.{extension})"

        )


        if file:

            with open(

                file,

                "w",

                encoding="utf-8"

            ) as f:

                f.write(
                    content
                )



    def open_settings(self):

        dialog = SettingsDialog(
            self.config,
            self
        )

        dialog.exec()



    def apply_style(self):

        self.setStyleSheet(
            """

            QWidget {
                background:#f5f5f7;
                font-size:14px;
            }


            #title {
                font-size:24px;
                font-weight:bold;
            }


            #dropArea {

                background:white;

                border:2px dashed #aaaaaa;

                border-radius:18px;

                min-height:180px;

            }


            QPushButton {

                background:#007aff;

                color:white;

                border:none;

                padding:10px 18px;

                border-radius:10px;

            }


            QPushButton:hover {

                background:#005ecb;

            }


            QTextEdit {

                background:white;

                border-radius:12px;

                padding:10px;

            }


            QProgressBar {

                height:14px;

                border-radius:7px;

            }


            """
        )