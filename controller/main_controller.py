# controller/main_controller.py

from PyQt5.QtWidgets import QApplication
from view.main_window import MainWindow


class MainController:
    """
    The MainController initializes the MainWindow and
    provides access to application-wide operations.
    """

    def __init__(self):
        # Create the main window, passing this controller
        self.window = MainWindow(controller=self)

    # Optional: اگر بخواهید متدی برای اجرای کامل داشته باشید
    def run(self):
        """
        Show the window and start the Qt event loop.
        """
        self.window.show()
        return QApplication.instance().exec_()
