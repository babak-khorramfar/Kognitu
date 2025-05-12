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
    The main application window.
    Contains control for total number of boards and a QGraphicsView for interactive layout.
    """

    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("Kognitu")
        self.resize(900, 700)

        # Graphics view placeholder
        self.view = QGraphicsView()
        self.scene = None

        # Build UI
        self._init_ui()

    def _init_ui(self):
        # Total boards control
        lbl_count = QLabel("Number of Boards:")
        self.spin_count = QSpinBox()
        self.spin_count.setRange(1, 100)
        self.spin_count.setValue(4)

        # Auto Layout button
        btn_generate = QPushButton("Auto Layout")
        btn_generate.clicked.connect(self.on_generate)

        # Controls layout
        controls = QHBoxLayout()
        controls.addWidget(lbl_count)
        controls.addWidget(self.spin_count)
        controls.addWidget(btn_generate)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.addLayout(controls)
        main_layout.addWidget(self.view)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def on_generate(self):
        """
        Auto-generate a grid layout based on total number of boards.
        """
        count = self.spin_count.value()

        # Create Layout automatically
        layout = Layout.auto_grid(count)

        # Create new scene with calculated rows and cols
        self.scene = BoardScene(layout.rows, layout.cols, TILE_IMAGE_PATH)
        self.view.setScene(self.scene)

        # Load placements into the scene
        self.scene.load_layout(layout)

        QMessageBox.information(
            self,
            "Layout Generated",
            f"Auto-generated layout for {count} boards ({layout.rows}×{layout.cols}).",
        )
