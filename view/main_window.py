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
from PyQt5.QtCore import Qt, QTimer
from view.game_window import GameWindow
from view.board_item import BoardItem
from utils.config import TILE_IMAGE_PATH


class MainLauncherWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("HipHop")

        screen = QApplication.primaryScreen()
        rect = screen.geometry()
        self.setGeometry(rect)
        self.setFixedSize(rect.width(), rect.height())

        self._init_ui()

    def _init_ui(self):
        # 🔹 پس‌زمینه با QLabel به‌صورت پوششی
        bg_label = QLabel(self)
        bg_label.setPixmap(
            QPixmap("resources/images/bg.jpg").scaled(
                self.width(),
                self.height(),
                Qt.KeepAspectRatioByExpanding,
                Qt.SmoothTransformation,
            )
        )
        bg_label.setGeometry(0, 0, self.width(), self.height())
        bg_label.lower()

        # 🔹 مرکز اصلی برنامه
        central = QWidget(self)
        central.setStyleSheet("background: transparent;")
        self.setCentralWidget(central)

        # 🔹 لوگو
        logo_label = QLabel()
        logo_pixmap = QPixmap("resources/images/logo.png").scaledToWidth(
            600, Qt.SmoothTransformation
        )
        logo_label.setPixmap(logo_pixmap)
        logo_label.setAlignment(Qt.AlignCenter)

        # 🔹 دکمه‌ها
        button_layout = QVBoxLayout()
        button_layout.setSpacing(20)
        button_layout.setAlignment(Qt.AlignCenter)

        for text, slot, icon in [
            ("Start Game", self.open_manual_game, ""),
            # ("AI Game (Coming Soon)", None, "🤖"),
            # ("Settings", None, "⚙️"),
            ("Exit", self.close, ""),
        ]:
            btn = QPushButton(f"{icon} {text}")
            btn.setFixedHeight(60)
            btn.setFixedWidth(400)
            btn.setFont(QFont("Arial", 18))
            btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            btn.setStyleSheet(
                """
                QPushButton {
                    border-radius: 20px;
                    font-weight: bold;
                    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #fcd34d, stop:1 #f97316);
                    color: white;
                }
                QPushButton:hover {
                    background-color: #ff7f50;
                }
            """
            )
            if slot:
                btn.clicked.connect(slot)
            else:
                btn.setEnabled(False)
            button_layout.addWidget(btn)

        # 🔹 تخته راهنما
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

        guide_label = QLabel("🖱️ Double-click to rotate\n🖱️ Right-click to flip")
        guide_label.setFont(QFont("Arial", 18))
        guide_label.setStyleSheet("color: #111;")

        guide_row = QHBoxLayout()
        guide_row.addSpacing(50)
        guide_row.addWidget(view)
        guide_row.addSpacing(20)
        guide_row.addWidget(guide_label)
        guide_row.addStretch()

        # 🔹 چیدمان نهایی
        main_layout = QVBoxLayout()
        main_layout.addSpacing(30)
        main_layout.addWidget(logo_label, alignment=Qt.AlignCenter)
        main_layout.addSpacing(20)
        main_layout.addLayout(button_layout)
        main_layout.addSpacing(20)  # ⬅ فاصله کمتر برای بالا آوردن راهنما
        main_layout.addLayout(guide_row)
        main_layout.addSpacing(300)  # ⬅ فاصله پایین‌تر برای جلوگیری از چسبیدن به لبه

        central.setLayout(main_layout)

        # تأخیر کوتاه برای اطمینان از اعمال سایز صحیح
        QTimer.singleShot(100, self._adjust_background)

    def _adjust_background(self):
        bg_label = self.findChild(QLabel)
        if bg_label:
            bg_label.setPixmap(
                QPixmap("resources/images/bg.jpg").scaled(
                    self.width(),
                    self.height(),
                    Qt.KeepAspectRatioByExpanding,
                    Qt.SmoothTransformation,
                )
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
