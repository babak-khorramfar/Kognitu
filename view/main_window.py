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
from PyQt5.QtCore import QTimer
from model.layout import Layout
from view.board_scene import BoardScene
from utils.config import TILE_IMAGE_PATH


class MainWindow(QMainWindow):
    def __init__(self, controller=None):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("Kognitu")
        self.resize(900, 700)

        self.view = QGraphicsView()
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

        # بعد از resize یا maximize چیدمان مجدد کنیم
        self.view.viewport().installEventFilter(self)

    def on_generate(self):
        self._do_layout()

    def eventFilter(self, source, event):
        from PyQt5.QtCore import QEvent

        if source is self.view.viewport() and event.type() == QEvent.Resize:
            # زمان کوتاهی بعد از ریست شدن اندازه، layout را دوباره اعمال کن
            QTimer.singleShot(50, self._do_layout)
        return super().eventFilter(source, event)

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
    window.showMaximized()
    sys.exit(app.exec_())
