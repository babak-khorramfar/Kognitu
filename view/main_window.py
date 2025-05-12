# view/main_window.py

from PyQt5.QtWidgets import (
    QMainWindow,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
    QSpinBox,
    QLabel,
    QGraphicsView,
    QMessageBox,
)
from model.layout import Layout
from view.board_scene import BoardScene
from utils.config import TILE_IMAGE_PATH


class MainWindow(QMainWindow):
    """
    Main window with control for number of boards and interactive QGraphicsView.
    """

    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("Kognitu")
        self.resize(900, 700)

        # ویجت گرافیکی
        self.view = QGraphicsView()
        self.scene = None

        self._init_ui()

    def _init_ui(self):
        lbl_count = QLabel("Number of Boards:")
        self.spin_count = QSpinBox()
        self.spin_count.setRange(1, 100)
        self.spin_count.setValue(4)

        btn_generate = QPushButton("Auto Layout")
        btn_generate.clicked.connect(self.on_generate)

        controls = QHBoxLayout()
        controls.addWidget(lbl_count)
        controls.addWidget(self.spin_count)
        controls.addWidget(btn_generate)

        main_layout = QVBoxLayout()
        main_layout.addLayout(controls)
        main_layout.addWidget(self.view)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def on_generate(self):
        count = self.spin_count.value()
        layout = Layout.auto_grid(count)

        # اندازه‌ی فضای قابل نمایش
        view_width = self.view.viewport().width()
        view_height = self.view.viewport().height()
        spacing = 10  # فاصله‌ی بین تخته‌ها

        # ساخت و بارگذاری صحنه
        self.scene = BoardScene(TILE_IMAGE_PATH)
        self.view.setScene(self.scene)
        self.scene.load_layout(layout.placements, view_width, view_height, spacing)

        QMessageBox.information(
            self,
            "Layout Generated",
            f"Generated {count} tiles with spacing {spacing}px.",
        )
