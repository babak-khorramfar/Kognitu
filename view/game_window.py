# view/game_window.py

from PyQt5.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QComboBox,
    QPushButton,
    QGraphicsView,
)
from PyQt5.QtCore import Qt, QTimer, QEvent
from view.board_scene import BoardScene
from model.layout import Layout
from utils.config import TILE_IMAGE_PATH


class GameWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kognitu - Manual Game")
        self.showMaximized()
        self.setFixedSize(self.size())

        self.view = QGraphicsView()
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scene = BoardScene(tile_image_path=TILE_IMAGE_PATH)
        self.view.setScene(self.scene)

        self._init_ui()

    def _init_ui(self):
        sidebar = QVBoxLayout()
        sidebar.setAlignment(Qt.AlignTop)

        label_type = QLabel("Board Type:")
        self.combo_type = QComboBox()
        self.combo_type.addItems(["4-color", "9-color"])
        self.combo_type.currentIndexChanged.connect(self.update_count_options)

        label_count = QLabel("Board Count:")
        self.combo_count = QComboBox()
        self.update_count_options()

        btn_generate = QPushButton("Generate Layout")
        btn_generate.clicked.connect(self._do_layout)

        for widget in [
            label_type,
            self.combo_type,
            label_count,
            self.combo_count,
            btn_generate,
        ]:
            sidebar.addWidget(widget)
            sidebar.addSpacing(10)

        layout = QHBoxLayout()
        layout.addLayout(sidebar, 1)
        layout.addWidget(self.view, 5)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.view.viewport().installEventFilter(self)

    def update_count_options(self):
        self.combo_count.clear()
        board_type = self.combo_type.currentText()
        if board_type == "4-color":
            self.combo_count.addItems(["4", "8", "12"])
        else:
            self.combo_count.addItems(["9", "18"])

    def _do_layout(self):
        count = int(self.combo_count.currentText())
        board_type = self.combo_type.currentText()
        w = self.view.viewport().width()
        h = self.view.viewport().height()
        self.scene.auto_layout(count, w, h, board_type=board_type)

    def eventFilter(self, source, event):
        if source is self.view.viewport() and event.type() == QEvent.Resize:
            QTimer.singleShot(50, self._do_layout)
        return super().eventFilter(source, event)

    def closeEvent(self, event):
        from view.main_window import MainLauncherWindow

        self.launcher = MainLauncherWindow()
        self.launcher.show()
        event.accept()
