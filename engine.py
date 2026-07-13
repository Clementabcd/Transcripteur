from pathlib import Path
import subprocess
import tempfile

from model_manager import ModelManager
from logger import log_info, log_error


class TranscriptionEngine:

    def __init__(self):

        log_info("Initialisation du moteur")

        self.model_manager = ModelManager()

        self.model = None


    def load_model(self, model_name="large-v3-turbo"):

        try:

            log_info(
                f"Chargement du modèle : {model_name}"
            )

            self.model = (
                self.model_manager
                .load_model(model_name)
            )

            log_info("Modèle chargé avec succès")


        except Exception as e:

            log_error(e)

            raise



    def process(self, file_path):

        try:

            if self.model is None:
                self.load_model()


            file_path = Path(file_path)


            log_info(
                f"Début traitement : {file_path}"
            )


            workdir = Path(
                tempfile.mkdtemp()
            )


            normalized = (
                workdir /
                "normalized.wav"
            )


            self.normalize_audio(
                file_path,
                normalized
            )


            duration = self.get_duration(
                normalized
            )


            log_info(
                f"Durée audio : {duration}s"
            )


            if duration > 1200:

                chunks = self.split_audio(
                    normalized,
                    workdir
                )

            else:

                chunks = [
                    normalized
                ]


            all_segments = []


            for chunk in chunks:

                log_info(
                    f"Transcription : {chunk}"
                )

                segments = self.transcribe(chunk)

                all_segments.extend(
                    segments
                )


            log_info(
                "Transcription terminée"
            )


            return {
                "segments": all_segments,
                "model": "large-v3-turbo"
            }



        except Exception as e:

            log_error(e)

            raise



    def normalize_audio(
        self,
        input_file,
        output_file
    ):

        log_info(
            "Normalisation audio"
        )


        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-i",
                str(input_file),

                "-af",
                "loudnorm=I=-16:TP=-1.5:LRA=11",

                "-ac",
                "1",

                "-ar",
                "16000",

                str(output_file)
            ],

            check=True
        )



    def get_duration(
        self,
        file
    ):

        result = subprocess.run(
            [
                "ffprobe",
                "-v",
                "error",

                "-show_entries",
                "format=duration",

                "-of",
                "csv=p=0",

                str(file)
            ],

            capture_output=True,

            text=True,

            check=True
        )


        return int(
            float(result.stdout)
        )



    def split_audio(
        self,
        file,
        folder
    ):

        log_info(
            "Découpage audio"
        )


        output = folder / "chunk_%03d.wav"


        subprocess.run(
            [
                "ffmpeg",

                "-i",
                str(file),

                "-f",
                "segment",

                "-segment_time",
                "1200",

                str(output)
            ],

            check=True
        )


        return sorted(
            folder.glob(
                "chunk_*.wav"
            )
        )



    def transcribe(
        self,
        file
    ):


        segments, info = self.model.transcribe(
            str(file),
            language="fr"
        )


        result = []


        for segment in segments:

            result.append(
                {
                    "start": segment.start,
                    "end": segment.end,
                    "text": segment.text.strip()
                }
            )


        return result