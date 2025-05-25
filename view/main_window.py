import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QSizePolicy,
    QGraphicsView,
    QGraphicsScene,
)
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt
from view.game_window import GameWindow
from view.board_item import BoardItem
from utils.config import TILE_IMAGE_PATH


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

        # 🔹 لوگو بالا
        logo_label = QLabel()
        logo_pixmap = QPixmap("resources/images/logo.png").scaledToWidth(
            480, Qt.SmoothTransformation
        )
        logo_label.setPixmap(logo_pixmap)
        logo_label.setAlignment(Qt.AlignCenter)

        # 🔹 تخته راهنما در QGraphicsView (با یک تخته قابل تعامل)
        view = QGraphicsView()
        scene = QGraphicsScene(0, 0, 200, 200)
        view.setScene(scene)
        view.setFixedSize(200, 200)
        view.setStyleSheet("background: transparent; border: none;")
        view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        board = BoardItem(
            face_up_path=TILE_IMAGE_PATH,
            face_down_path="resources/images/backs/4colors/blue.png",
            tile_size=140,
            spacing=0,
        )
        board.setPos(30, 30)
        scene.addItem(board)

        # 🔹 راهنمای چرخش و فلیپ
        label = QLabel("🖱️ Double-click to rotate\n🖱️ Right-click to flip")
        label.setFont(QFont("Arial", 18))
        label.setStyleSheet("color: #111;")

        guide_row = QHBoxLayout()
        guide_row.addWidget(view)
        guide_row.addSpacing(20)
        guide_row.addWidget(label)
        guide_row.addStretch(1)

        guide_column = QVBoxLayout()
        guide_column.addLayout(guide_row)
        guide_column.addStretch(1)
        guide_column.setContentsMargins(40, 0, 0, 0)

        # 🔹 دکمه‌ها
        button_layout = QVBoxLayout()
        button_layout.setSpacing(25)
        button_layout.setContentsMargins(0, 0, 40, 0)
        button_layout.setAlignment(Qt.AlignTop)

        for text, slot in [
            ("Start Manual Game", self.open_manual_game),
            ("AI Game (Coming Soon)", None),
            ("Settings", None),
            ("Exit", self.close),
        ]:
            btn = QPushButton(text)
            btn.setFixedHeight(60)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            if slot:
                btn.clicked.connect(slot)
            else:
                btn.setEnabled(False)
            button_layout.addWidget(btn)

        # 🔹 ترکیب پایین
        bottom_layout = QHBoxLayout()
        bottom_layout.addLayout(guide_column, 1)
        bottom_layout.addLayout(button_layout, 1)

        # 🔹 چیدمان کلی صفحه
        main_layout = QVBoxLayout()
        main_layout.addWidget(logo_label)
        main_layout.addSpacing(30)
        main_layout.addLayout(bottom_layout)

        central.setLayout(main_layout)

        # 🔹 استایل کلی
        self.setStyleSheet(
            """
            QWidget { background-color: white; }
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
        """
        )

    def open_manual_game(self):
        self.game_window = GameWindow()
        self.game_window.show()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainLauncherWindow()
    window.show()
    sys.exit(app.exec_())
