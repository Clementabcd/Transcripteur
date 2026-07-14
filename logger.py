import logging

from utils import get_logs_dir


# Création du dossier logs utilisateur
LOG_FILE = (
    get_logs_dir()
    /
    "app.log"
)


logging.basicConfig(
    filename=str(LOG_FILE),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)



def log_error(error):

    logging.error(
        str(error),
        exc_info=True
    )



def log_info(message):

    logging.info(message)