# view/main_window.py

import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QSpacerItem,
    QSizePolicy,
    QHBoxLayout,
)
from PyQt5.QtCore import Qt
from view.game_window import GameWindow


class MainLauncherWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("HipHop")
        self.showMaximized()
        self.setFixedSize(self.size())
        self._init_ui()

    def _init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)

        # محتوای وسط لانچر (نام بازی + دکمه‌ها)
        content_layout = QVBoxLayout()
        content_layout.setAlignment(Qt.AlignCenter)

        title = QLabel("🎮 HipHop")
        title.setAlignment(Qt.AlignCenter)

        btn_manual = QPushButton("Start Manual Game")
        btn_manual.clicked.connect(self.open_manual_game)

        btn_ai = QPushButton("AI Game (Coming Soon)")
        btn_ai.setEnabled(False)

        btn_settings = QPushButton("Settings")
        btn_exit = QPushButton("Exit")
        btn_exit.clicked.connect(self.close)

        for btn in [btn_manual, btn_ai, btn_settings, btn_exit]:
            btn.setFixedHeight(70)
            content_layout.addWidget(btn)
            content_layout.addSpacing(20)

        content_layout.insertWidget(0, title)
        content_layout.addSpacing(40)

        # مرکزچینی عمودی با Spacer بالا و پایین
        outer_layout = QVBoxLayout()
        outer_layout.addStretch(1)
        outer_layout.addLayout(content_layout)
        outer_layout.addStretch(1)

        central.setLayout(outer_layout)

        self.setStyleSheet(
            """
            QWidget {
                background-color: #151c2c;
            }
            QPushButton {
                font-family: "Game Changer";
                font-size: 28px;
                padding: 14px 28px;
                border-radius: 20px;
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                  stop:0 #ffb347, stop:1 #ff704d);
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #ff5722;
            }
            QLabel {
                font-size: 80px;
                font-family: "Game Changer";
                font-weight: bold;
                color: #f1c40f;
            }
        """
        )

    def open_manual_game(self):
        self.game_window = GameWindow()
        self.game_window.show()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainLauncherWindow()
    sys.exit(app.exec_())
