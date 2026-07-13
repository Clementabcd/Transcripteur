from pathlib import Path

from faster_whisper import WhisperModel

from utils import get_models_dir



class ModelManager:


    def __init__(self):

        self.models_dir = get_models_dir()



    def model_exists(
        self,
        model_name
    ):

        model_path = (
            self.models_dir /
            model_name
        )

        return model_path.exists()



    def load_model(
        self,
        model_name
    ):


        model_path = (
            self.models_dir /
            model_name
        )


        if model_path.exists():

            print(
                f"Chargement du modèle local : {model_name}"
            )


            return WhisperModel(

                str(model_path),

                device="auto",

                compute_type="auto"

            )


        print(
            f"Téléchargement du modèle : {model_name}"
        )


        model = WhisperModel(

            model_name,

            device="auto",

            compute_type="auto"

        )


        return model