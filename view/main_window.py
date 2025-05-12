# view/main_window.py

import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
    QSpinBox,
    QLabel,
    QGraphicsView,
)
from PyQt5.QtCore import QTimer, QEvent, Qt
from model.layout import Layout
from view.board_scene import BoardScene
from utils.config import TILE_IMAGE_PATH


class MainWindow(QMainWindow):
    def __init__(self, controller=None):
        # والد را خالی صدا می‌زنیم، نه controller!
        super().__init__()
        self.controller = controller

        self.setWindowTitle("Kognitu")
        # پنجره تمام‌صفحه و غیرقابل کوچک‌شدن
        self.setWindowFlags(
            Qt.Window
            | Qt.CustomizeWindowHint
            | Qt.WindowTitleHint
            | Qt.WindowCloseButtonHint
        )
        self.showFullScreen()

        self.view = QGraphicsView()
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scene = None

        self._init_ui()

    def _init_ui(self):
        lbl = QLabel("Number of Boards:")
        self.spin = QSpinBox()
        self.spin.setRange(1, 100)
        self.spin.setValue(4)

        btn = QPushButton("Auto Layout")
        btn.clicked.connect(self.on_generate)

        ctl = QHBoxLayout()
        ctl.addWidget(lbl)
        ctl.addWidget(self.spin)
        ctl.addWidget(btn)

        lay = QVBoxLayout()
        lay.addLayout(ctl)
        lay.addWidget(self.view)

        container = QWidget()
        container.setLayout(lay)
        self.setCentralWidget(container)

        # وقتی viewport تغییر اندازه می‌دهد، مجدداً چینش انجام شود
        self.view.viewport().installEventFilter(self)

    def eventFilter(self, source, event):
        if source is self.view.viewport() and event.type() == QEvent.Resize:
            QTimer.singleShot(50, self._do_layout)
        return super().eventFilter(source, event)

    def on_generate(self):
        self._do_layout()

    def _do_layout(self):
        count = self.spin.value()
        layout = Layout.auto_grid(count)
        w = self.view.viewport().width()
        h = self.view.viewport().height()

        if self.scene is None:
            self.scene = BoardScene(TILE_IMAGE_PATH)
            self.view.setScene(self.scene)
        self.scene.load_layout(layout, w, h)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
