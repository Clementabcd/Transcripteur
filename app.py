import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QDialog
from gui import MainWindow
from first_launch import FirstLaunchDialog
from model_manager import ModelManager


def main():

    app = QApplication(sys.argv)


    manager = ModelManager()


    if not manager.model_exists(
        "large-v3"
    ):

        dialog = FirstLaunchDialog()

        result = dialog.exec()

        if result != QDialog.Accepted:
            sys.exit(0)



    window = MainWindow()

    window.show()


    exit_code = app.exec()

    sys.exit(exit_code)


if __name__ == "__main__":
    main()