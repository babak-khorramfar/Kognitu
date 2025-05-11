# view/main_window.py

import ast
from PyQt5.QtWidgets import QMainWindow, QPushButton, QHBoxLayout, QWidget, QMessageBox
from view.board_canvas import BoardCanvas
from controller.ai_client import AIClient


class MainWindow(QMainWindow):
    """
    The main application window, containing buttons and the board canvas.
    Handles user actions for generating and customizing layouts via AI.
    """

    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("Kognitu")
        self.resize(800, 600)

        # Initialize the board canvas
        self.canvas = BoardCanvas()

        # Initialize AI client (you can switch model_name)
        self.ai_client = AIClient(model_name="gpt2")

        # Build UI
        self._init_ui()

    def _init_ui(self):
        # Buttons
        btn_generate = QPushButton("Generate Challenge")
        btn_custom = QPushButton("Create Custom Layout")
        btn_generate.clicked.connect(self.on_generate)
        btn_custom.clicked.connect(self.on_custom)

        # Layouts
        top_layout = QHBoxLayout()
        top_layout.addWidget(btn_generate)
        top_layout.addWidget(btn_custom)

        main_layout = QHBoxLayout()
        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.canvas)

        # Container widget
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def on_generate(self):
        """
        Generate a new layout via AI, parse the RGB list,
        and update the board colors.
        """
        rows = self.canvas.board.rows
        cols = self.canvas.board.cols

        # Craft prompt: request a pure Python list of RGB tuples
        prompt = (
            f"Generate a Python list of RGB tuples for a {rows}x{cols} board "
            f"in row-major order. Example output: [(255,0,0),(0,255,0),...]."
        )

        try:
            result_text = self.ai_client.generate(prompt, max_length=100)
            # Parse the returned text into a Python list
            color_list = ast.literal_eval(result_text.strip().split("\\n")[-1])

            # Validate length
            if len(color_list) != rows * cols:
                raise ValueError(f"Expected {rows*cols} colors, got {len(color_list)}")

            # Apply to tiles
            for tile, color in zip(self.canvas.board.tiles, color_list):
                # Ensure each color is a tuple of three ints
                if isinstance(color, (list, tuple)) and len(color) == 3:
                    tile.color = tuple(color)
                else:
                    raise ValueError(f"Invalid color format: {color}")

            # Redraw canvas
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
