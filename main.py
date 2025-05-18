# main.py

import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont, QFontDatabase
from controller.main_controller import MainController


def main():
    app = QApplication(sys.argv)

    # ✅ Load custom font
    font_id = QFontDatabase.addApplicationFont(
        "resources/fonts/Game Changer Regular.ttf"
    )
    if font_id == -1:
        print("❌ Failed to load Game Changer font.")
    else:
        family = QFontDatabase.applicationFontFamilies(font_id)[0]
        app.setFont(QFont(family, 12))

    # ✅ Launch main window
    controller = MainController()
    controller.window.show()

    # ✅ Start app
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
