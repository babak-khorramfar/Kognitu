# main.py

import sys
from PyQt5.QtWidgets import QApplication
from controller.main_controller import MainController


def main():
    """
    Entry point of the application.
    Creates the QApplication, instantiates the controller,
    and starts the event loop.
    """
    app = QApplication(sys.argv)
    controller = MainController()
    controller.window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
