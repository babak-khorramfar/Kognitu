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
    QFrame,
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
        # پس‌زمینه
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

        # مرکز برنامه
        central = QWidget(self)
        central.setStyleSheet("background: transparent;")
        self.setCentralWidget(central)

        # لوگو
        logo_label = QLabel()
        logo_pixmap = QPixmap("resources/images/logo.png").scaledToWidth(
            600, Qt.SmoothTransformation
        )
        logo_label.setPixmap(logo_pixmap)
        logo_label.setAlignment(Qt.AlignCenter)

        # دکمه‌ها
        button_layout = QVBoxLayout()
        button_layout.setSpacing(20)
        button_layout.setAlignment(Qt.AlignCenter)
        for text, slot in [
            ("Start Game", self.open_manual_game),
            ("Exit", self.close),
        ]:
            btn = QPushButton(text)
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
            btn.clicked.connect(slot)
            button_layout.addWidget(btn)

        # --- راهنما ---

        view = QGraphicsView()
        scene = QGraphicsScene(0, 0, 250, 250)
        view.setScene(scene)
        view.setFixedSize(250, 250)
        view.setStyleSheet("background: transparent; border: none;")
        view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        board = BoardItem(
            face_up_path=TILE_IMAGE_PATH,
            face_down_path="resources/images/backs/4colors/blue.png",
            tile_size=170,
            spacing=0,
        )
        board.setPos(40, 30)
        scene.addItem(board)

        rotate_icon = QLabel()
        rotate_icon.setPixmap(
            QPixmap("resources/images/rotate.png").scaled(
                120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
        )
        flip_icon = QLabel()
        flip_icon.setPixmap(
            QPixmap("resources/images/flip.png").scaled(
                120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
        )

        icons_layout = QVBoxLayout()
        icons_layout.setSpacing(12)
        icons_layout.addWidget(rotate_icon)
        icons_layout.addWidget(flip_icon)
        icons_layout.addStretch(1)

        guide_layout = QHBoxLayout()
        guide_layout.setSpacing(30)
        guide_layout.addWidget(view)
        guide_layout.addLayout(icons_layout)

        # فریم راهنما (کادر شیشه‌ای)
        guide_frame = QFrame()
        guide_frame.setLayout(guide_layout)
        guide_frame.setStyleSheet(
            """
            QFrame {
                background-color: rgba(255,255,255,0.65);  /* نیمه شفاف */
                border-radius: 32px;
                border: 2px solid rgba(120,120,120,0.18);
                /* برای شبیه‌سازی shadow میتونی کمی border کمرنگ‌تر بذاری */
            }
        """
        )
        guide_frame.setFixedHeight(270)  # میتونی با توجه به سایز کل تنظیم کنی
        guide_frame.setFixedWidth(420)  # یا بزرگتر

        # وسط‌چینی کل محتوا با Spacer
        main_layout = QVBoxLayout()
        main_layout.addStretch(1)
        main_layout.addWidget(logo_label, alignment=Qt.AlignHCenter)
        main_layout.addWidget(guide_frame, alignment=Qt.AlignLeft | Qt.AlignBottom)
        main_layout.addSpacing(12)
        main_layout.addLayout(button_layout)
        main_layout.addSpacing(30)
        main_layout.addLayout(guide_layout)
        main_layout.addStretch(2)  # <-- راهنما پایین‌تر ولی داخل صفحه

        central.setLayout(main_layout)

        # بک‌گراند ری‌سایز
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
