# view/board_canvas.py

from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QColor, QBrush
from PyQt5.QtCore import QRect
from model.board import Board
from utils.config import DEFAULT_ROWS, DEFAULT_COLS, DEFAULT_COLORS


class BoardCanvas(QWidget):
    """
    A QWidget that renders the Board model graphically.
    """

    def __init__(self, parent=None, rows=None, cols=None):
        super().__init__(parent)

        # Use provided rows/cols or fall back to defaults
        self.rows = rows or DEFAULT_ROWS
        self.cols = cols or DEFAULT_COLS

        # Initialize Board model
        self.board = Board(
            rows=self.rows, cols=self.cols, default_colors=DEFAULT_COLORS
        )

        self.setMinimumSize(200, 200)

    def reset_board(self, rows, cols):
        """
        Re-create the Board model with new dimensions.
        """
        self.rows = rows
        self.cols = cols
        self.board = Board(rows=rows, cols=cols, default_colors=DEFAULT_COLORS)
        self.update()

    def paintEvent(self, event):
        """
        Paint each Tile on the widget using QPainter.
        """
        painter = QPainter(self)
        tile_size = min(
            self.width() // self.board.cols, self.height() // self.board.rows
        )

        for tile in self.board.tiles:
            x = tile.col * tile_size
            y = tile.row * tile_size
            r, g, b = tile.color
            color = QColor(r, g, b)

            rect = QRect(x, y, tile_size, tile_size)
            painter.fillRect(rect, QBrush(color))
            painter.setPen(QColor(0, 0, 0))
            painter.drawRect(rect)

        painter.end()
