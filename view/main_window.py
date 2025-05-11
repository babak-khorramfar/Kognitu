# view/main_window.py

import ast
from PyQt5.QtWidgets import (
    QMainWindow,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
    QMessageBox,
    QLabel,
    QSpinBox,
)
from view.board_canvas import BoardCanvas
from controller.ai_client import AIClient
from utils.config import PROMPT_TEMPLATE


class MainWindow(QMainWindow):
    """
    The main application window, containing buttons, controls and the board canvas.
    """

    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("Kognitu")
        self.resize(900, 700)

        # Initialize the board canvas with default size
        self.canvas = BoardCanvas()

        # Initialize AI client from config
        self.ai_client = AIClient()

        # Build UI
        self._init_ui()

    def _init_ui(self):
        # Controls: Rows & Cols
        lbl_rows = QLabel("Rows:")
        self.spin_rows = QSpinBox()
        self.spin_rows.setRange(1, 10)
        self.spin_rows.setValue(self.canvas.rows)

        lbl_cols = QLabel("Cols:")
        self.spin_cols = QSpinBox()
        self.spin_cols.setRange(1, 10)
        self.spin_cols.setValue(self.canvas.cols)

        # Buttons
        btn_generate = QPushButton("Generate Challenge")
        btn_custom = QPushButton("Create Custom Layout")
        btn_generate.clicked.connect(self.on_generate)
        btn_custom.clicked.connect(self.on_custom)

        # Layouts
        control_layout = QHBoxLayout()
        control_layout.addWidget(lbl_rows)
        control_layout.addWidget(self.spin_rows)
        control_layout.addWidget(lbl_cols)
        control_layout.addWidget(self.spin_cols)
        control_layout.addWidget(btn_generate)
        control_layout.addWidget(btn_custom)

        main_layout = QVBoxLayout()
        main_layout.addLayout(control_layout)
        main_layout.addWidget(self.canvas)

        # Container widget
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def on_generate(self):
        """
        Generate a new layout via AI, parse the RGB list,
        recreate the board model and update the displayed tiles.
        """
        rows = self.spin_rows.value()
        cols = self.spin_cols.value()

        # Reset canvas with new dimensions
        self.canvas.reset_board(rows, cols)

        # Prepare prompt
        prompt = PROMPT_TEMPLATE.format(rows=rows, cols=cols)

        try:
            result_text = self.ai_client.generate(prompt, max_length=150)
            last_line = result_text.strip().splitlines()[-1]
            color_list = ast.literal_eval(last_line)

            # Validate length
            if len(color_list) != rows * cols:
                raise ValueError(f"Expected {rows*cols} colors, got {len(color_list)}")

            # Apply colors
            for tile, color in zip(self.canvas.board.tiles, color_list):
                if isinstance(color, (list, tuple)) and len(color) == 3:
                    tile.color = tuple(color)
                else:
                    raise ValueError(f"Invalid color format: {color}")

            self.canvas.update()

        except Exception as e:
            QMessageBox.critical(self, "AI Error", f"Failed to generate layout:\n{e}")

    def on_custom(self):
        """
        Placeholder for custom layout creation mode.
        """
        QMessageBox.information(
            self, "Custom Layout", "Custom layout mode not implemented yet."
        )
