import sys
from PySide6.QtWidgets import QApplication
from gui import MainWindow
from first_launch import FirstLaunchDialog
from model_manager import ModelManager


def main():

    app = QApplication(sys.argv)


    manager = ModelManager()


    if not manager.model_exists(
        "large-v3-turbo"
    ):

        dialog = FirstLaunchDialog()

        result = dialog.exec()

        if result != 1:
            return



    window = MainWindow()

    window.show()


    sys.exit(
        app.exec()
    )


if __name__ == "__main__":
    main()