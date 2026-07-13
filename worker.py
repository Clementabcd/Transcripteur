from PySide6.QtCore import QThread, Signal

from engine import TranscriptionEngine


class TranscriptionWorker(QThread):

    progress = Signal(int)
    status = Signal(str)

    finished = Signal(object)
    error = Signal(str)


    def __init__(
        self,
        file_path,
        config
    ):
        super().__init__()

        self.file_path = file_path
        self.config = config


    def run(self):

        try:

            self.status.emit(
                "Initialisation du moteur..."
            )

            engine = TranscriptionEngine()


            self.status.emit(
                "Vérification du modèle Whisper..."
            )

            if self.config["model"]:

                self.status.emit(
                    f"Modèle : {self.config['model']}"
                )


            engine.load_model(
                self.config["model"]
            )


            self.progress.emit(10)


            self.status.emit(
                "Traitement audio..."
            )


            result = engine.process(
                self.file_path
            )


            self.progress.emit(100)


            self.status.emit(
                "Transcription terminée"
            )


            self.finished.emit(
                result
            )


        except Exception as e:

            self.error.emit(
                str(e)
            )