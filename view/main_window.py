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
from model.layout import Layout
from view.board_scene import BoardScene
from utils.config import TILE_IMAGE_PATH


class MainWindow(QMainWindow):
    """
    Main window with control for number of boards and interactive QGraphicsView.
    """

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

    def on_generate(self):
        count = self.spin.value()
        layout = Layout.auto_grid(count)

        w = self.view.viewport().width()
        h = self.view.viewport().height()

        self.scene = BoardScene(TILE_IMAGE_PATH)
        self.view.setScene(self.scene)
        # بدون پیام!
        self.scene.load_layout(layout, w, h)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showMaximized()
    sys.exit(app.exec_())
