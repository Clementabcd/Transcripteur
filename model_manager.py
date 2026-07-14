from faster_whisper import WhisperModel

from utils import (
    get_models_dir,
    load_config,
    save_config
)


class ModelManager:


    def __init__(self):

        self.models_dir = get_models_dir()



    def model_exists(self, model_name):

        """
        Vérifie si le modèle a déjà été installé.
        Le modèle est géré par le cache Hugging Face,
        donc on utilise la configuration EchoScript.
        """

        config = load_config()

        return config.get(
            "model_installed",
            False
        )



    def mark_model_installed(self):

        """
        Enregistre que le modèle a été téléchargé.
        """

        config = load_config()

        config["model_installed"] = True

        save_config(config)



    def load_model(self, model_name):

        print(
            f"Chargement du modèle : {model_name}"
        )


        model = WhisperModel(

            model_name,

            device="auto",

            compute_type="auto"

        )


        return model