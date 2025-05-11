# view/board_canvas.py

from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QColor, QBrush
from PyQt5.QtCore import QRect
from model.board import Board


class BoardCanvas(QWidget):
    """
    A QWidget that renders the Board model graphically.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        # Default colors for an initial 2×2 board (RGB tuples)
        default_colors = [
            (255, 0, 0),  # Red
            (0, 255, 0),  # Green
            (0, 0, 255),  # Blue
            (255, 255, 0),  # Yellow
        ]

        # Initialize a 2×2 Board model
        self.board = Board(rows=2, cols=2, default_colors=default_colors)

        # Optional: set a minimum size
        self.setMinimumSize(200, 200)

    def paintEvent(self, event):
        """
        Paints each Tile from the Board model onto the widget using QPainter.
        """
        painter = QPainter(self)

        # Determine tile size based on widget dimensions
        tile_size = min(
            self.width() // self.board.cols, self.height() // self.board.rows
        )

        # Draw each tile
        for tile in self.board.tiles:
            row, col = tile.row, tile.col
            r, g, b = tile.color
            color = QColor(r, g, b)

            # Compute position and size
            x = col * tile_size
            y = row * tile_size
            rect = QRect(x, y, tile_size, tile_size)

            # Fill the rectangle
            painter.fillRect(rect, QBrush(color))

            # Optional: draw border
            painter.setPen(QColor(0, 0, 0))
            painter.drawRect(rect)

        painter.end()
