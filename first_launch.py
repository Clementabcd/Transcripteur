from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QLabel,
    QPushButton,
    QVBoxLayout
)

from PySide6.QtCore import (
    Qt,
    QThread,
    Signal,
    QTimer
)

from model_manager import ModelManager
from utils import get_ffmpeg_path



class DownloadWorker(QThread):

    finished = Signal()
    error = Signal(str)


    def __init__(
        self,
        model_name
    ):

        super().__init__()

        self.model_name = model_name


    def run(self):

        try:

            manager = ModelManager()

            # Télécharge / charge le modèle Whisper
            manager.load_model(
                self.model_name
            )

            # Marque le modèle comme installé
            manager.mark_model_installed()

            # Télécharge FFmpeg si nécessaire
            get_ffmpeg_path()

            self.finished.emit()


        except Exception as e:

            self.error.emit(
                str(e)
            )



class FirstLaunchDialog(QDialog):


    def __init__(self):

        super().__init__()


        self.setWindowTitle(
            "Bienvenue dans EchoScript"
        )


        self.resize(
            450,
            300
        )


        self.worker = None


        # Animation chargement

        self.loading_symbols = [
            "◌",
            "◍",
            "◉",
            "◍"
        ]

        self.loading_index = 0


        self.loading_timer = QTimer()

        self.loading_timer.timeout.connect(
            self.animate_loading
        )



        layout = QVBoxLayout(self)



        title = QLabel(
            "🎙 EchoScript"
        )

        title.setAlignment(
            Qt.AlignCenter
        )


        title.setStyleSheet(
            """
            font-size:28px;
            font-weight:bold;
            """
        )


        layout.addWidget(
            title
        )



        self.info = QLabel(
            """
            Bienvenue !

            Pour fonctionner, EchoScript
            doit télécharger le modèle
            Whisper.

            Modèle :
            large-v3

            Le téléchargement est effectué
            une seule fois.
            """
        )


        self.info.setAlignment(
            Qt.AlignCenter
        )


        layout.addWidget(
            self.info
        )



        self.loading_label = QLabel()

        self.loading_label.setAlignment(
            Qt.AlignCenter
        )


        self.loading_label.hide()


        layout.addWidget(
            self.loading_label
        )



        self.button = QPushButton(
            "Télécharger le modèle"
        )


        self.button.clicked.connect(
            self.download
        )


        layout.addWidget(
            self.button
        )





    def download(self):

        self.button.hide()


        self.loading_label.show()


        self.loading_timer.start(
            250
        )


        self.info.setText(
            "Préparation du modèle Whisper..."
        )


        self.worker = DownloadWorker(
            "large-v3"
        )


        self.worker.finished.connect(
            self.complete
        )


        self.worker.error.connect(
            self.failed
        )


        self.worker.start()





    def animate_loading(self):

        symbol = (
            self.loading_symbols[
                self.loading_index
            ]
        )


        self.loading_index += 1


        if self.loading_index >= len(
            self.loading_symbols
        ):

            self.loading_index = 0



        self.loading_label.setText(
            symbol
            +
            "  Téléchargement du modèle Whisper..."
        )



    def complete(self):

        from PySide6.QtWidgets import QMessageBox
        import sys

        QMessageBox.information(
            self,
            "Installation terminée",
            """
    EchoScript est prêt !

    Le modèle Whisper a été installé avec succès.

    Veuillez fermer puis rouvrir l'application
    pour terminer le premier lancement.
            """
        )


        # Ferme la fenêtre
        self.accept()


        # Ferme complètement l'application
        QApplication.quit()




    def failed(
        self,
        message
    ):

        self.loading_timer.stop()


        self.loading_label.hide()


        self.info.setText(
            "Erreur pendant l'installation :\n\n"
            +
            message
        )


        self.button.setText(
            "Réessayer"
        )


        self.button.show()