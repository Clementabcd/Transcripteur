import json
import platform
from pathlib import Path

import imageio_ffmpeg


APP_NAME = "EchoScript"


# =====================================================
# Gestion des données utilisateur
# =====================================================

def get_app_data_dir():
    """
    Retourne le dossier principal de données utilisateur.
    """

    system = platform.system()

    if system == "Darwin":
        # macOS
        folder = (
            Path.home()
            / "Library"
            / "Application Support"
            / APP_NAME
        )

    elif system == "Windows":
        # Windows
        folder = (
            Path.home()
            / "AppData"
            / "Roaming"
            / APP_NAME
        )

    else:
        # Linux
        folder = (
            Path.home()
            / ".local"
            / "share"
            / APP_NAME
        )


    folder.mkdir(
        parents=True,
        exist_ok=True
    )

    return folder



def get_models_dir():

    folder = (
        get_app_data_dir()
        / "models"
    )

    folder.mkdir(
        parents=True,
        exist_ok=True
    )

    return folder



def get_logs_dir():

    folder = (
        get_app_data_dir()
        / "logs"
    )

    folder.mkdir(
        parents=True,
        exist_ok=True
    )

    return folder



def get_temp_dir():

    folder = (
        get_app_data_dir()
        / "temp"
    )

    folder.mkdir(
        parents=True,
        exist_ok=True
    )

    return folder



def get_exports_dir():

    folder = (
        get_app_data_dir()
        / "exports"
    )

    folder.mkdir(
        parents=True,
        exist_ok=True
    )

    return folder



def get_config_file():

    return (
        get_app_data_dir()
        / "config.json"
    )


# =====================================================
# Configuration
# =====================================================

def load_config():

    config_file = get_config_file()


    if not config_file.exists():

        config = {

            "model": "large-v3",

            "language": "fr",

            "export_format": "txt"

        }

        save_config(config)

        return config



    with open(
        config_file,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)



def save_config(config):

    with open(
        get_config_file(),
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            config,
            f,
            indent=4,
            ensure_ascii=False
        )


# =====================================================
# Export transcription
# =====================================================

def format_time(seconds):

    hours = int(seconds // 3600)

    minutes = int(
        (seconds % 3600) // 60
    )

    secs = int(seconds % 60)

    millis = int(
        (seconds - int(seconds)) * 1000
    )


    return (
        f"{hours:02}:"
        f"{minutes:02}:"
        f"{secs:02},"
        f"{millis:03}"
    )



def export_txt(data):

    text = ""

    for s in data["segments"]:

        text += (
            s["text"]
            + "\n"
        )

    return text



def export_srt(data):

    output = ""

    for i, s in enumerate(
        data["segments"],
        start=1
    ):

        output += (
            f"{i}\n"
            f"{format_time(s['start'])}"
            " --> "
            f"{format_time(s['end'])}\n"
            f"{s['text']}\n\n"
        )


    return output



def export_vtt(data):

    output = "WEBVTT\n\n"


    for s in data["segments"]:

        output += (
            f"{format_time(s['start']).replace(',', '.')}"
            " --> "
            f"{format_time(s['end']).replace(',', '.')}\n"
            f"{s['text']}\n\n"
        )


    return output



def export_json(data):

    return json.dumps(
        data,
        indent=4,
        ensure_ascii=False
    )


# =====================================================
# FFmpeg
# =====================================================

def get_ffmpeg_path():
    """
    Retourne le chemin du FFmpeg fourni par imageio-ffmpeg.
    """

    return imageio_ffmpeg.get_ffmpeg_exe()

def get_lock_file():

    return (
        get_app_data_dir()
        /
        "EchoScript.lock"
    )