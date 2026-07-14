from pathlib import Path
import subprocess
import tempfile

from model_manager import ModelManager
from logger import log_info, log_error

from utils import get_ffmpeg_path


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
        
        allowed_extensions = [
            ".mp3",
            ".wav",
            ".m4a",
            ".flac",
            ".ogg",
            ".aac",
            ".mp4",
            ".mov",
            ".mkv"
        ]


        input_file = Path(input_file)


        if input_file.suffix.lower() not in allowed_extensions:

            raise ValueError(
                "Format non pris en charge.\n"
                "Veuillez sélectionner un fichier audio ou vidéo."
            )


        log_info(
            "Normalisation audio"
        )

        def get_ffmpeg():
            return get_ffmpeg_path()

        subprocess.run(
            [
                get_ffmpeg(),
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

        ffmpeg = get_ffmpeg_path()


        result = subprocess.run(
            [
                ffmpeg,

                "-i",

                str(file)

            ],

            stdout=subprocess.PIPE,

            stderr=subprocess.PIPE,

            text=True
        )


        output = result.stderr


        import re


        match = re.search(
            r"Duration:\s(\d+):(\d+):(\d+\.\d+)",
            output
        )


        if not match:
            return 0


        hours = int(match.group(1))

        minutes = int(match.group(2))

        seconds = float(match.group(3))


        return (
            hours * 3600
            +
            minutes * 60
            +
            seconds
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

        ffmpeg = get_ffmpeg_path()


        subprocess.run(
            [
                ffmpeg,

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