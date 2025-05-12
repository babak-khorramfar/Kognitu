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
from view.board_scene import BoardScene
from utils.config import TILE_IMAGE_PATH


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kognitu")

        # نمایش در حالت تمام‌صفحه و قفل resize
        self.showMaximized()
        self.setFixedSize(self.size())

        # ایجاد QGraphicsView برای صحنه
        self.view = QGraphicsView()
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scene = BoardScene(tile_image_path=TILE_IMAGE_PATH)
        self.view.setScene(self.scene)

        self._init_ui()

    def _init_ui(self):
        lbl = QLabel("Number of Boards:")
        self.spin = QSpinBox()
        self.spin.setRange(1, 100)
        self.spin.setValue(4)

        btn = QPushButton("Auto Layout")
        btn.clicked.connect(self._do_layout)

        ctl = QHBoxLayout()
        ctl.addWidget(lbl)
        ctl.addWidget(self.spin)
        ctl.addStretch()
        ctl.addWidget(btn)

        lay = QVBoxLayout()
        lay.addLayout(ctl)
        lay.addWidget(self.view)

        container = QWidget()
        container.setLayout(lay)
        self.setCentralWidget(container)

        # وقتی سایز view تغییر کند، چیدمان دوباره ساخته می‌شود
        self.view.viewport().installEventFilter(self)

    def eventFilter(self, source, event):
        if source is self.view.viewport() and event.type() == QEvent.Resize:
            QTimer.singleShot(50, self._do_layout)
        return super().eventFilter(source, event)

    def _do_layout(self):
        count = self.spin.value()
        w = self.view.viewport().width()
        h = self.view.viewport().height()
        self.scene.auto_layout(count, w, h)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
