# view/board_scene.py

import math
from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtGui import QPixmap
from view.board_item import BoardItem
from utils.config import DIAGONAL_SPACING_FACTOR


class BoardScene(QGraphicsScene):
    """
    Scene that arranges BoardItems centered with dynamic tile size
    and spacing to prevent any overlap when rotated.
    """

    def __init__(self, tile_image_path: str, parent=None):
        super().__init__(parent)
        self.pixmap = QPixmap(tile_image_path)

    def load_layout(self, placements, view_width, view_height):
        self.clear()
        cols = max(p.x for p in placements) + 1
        rows = max(p.y for p in placements) + 1

        # compute base tile size
        base_tile_w = view_width / (cols + DIAGONAL_SPACING_FACTOR)
        base_tile_h = view_height / (rows + DIAGONAL_SPACING_FACTOR)
        tile_size = int(min(base_tile_w, base_tile_h))
        # spacing ensures no overlap at 45 degrees
        spacing = int(tile_size * DIAGONAL_SPACING_FACTOR)

        total_w = cols * tile_size + (cols + 1) * spacing
        total_h = rows * tile_size + (rows + 1) * spacing
        # full scene covers entire view
        self.setSceneRect(0, 0, view_width, view_height)

        # center offsets
        offset_x = (view_width - total_w) / 2
        offset_y = (view_height - total_h) / 2

        for p in placements:
            item = BoardItem(p, self.pixmap, tile_size, spacing)
            x = offset_x + spacing + p.x * (tile_size + spacing)
            y = offset_y + spacing + p.y * (tile_size + spacing)
            item.setPos(x, y)
            item.setRotation(p.angle)
            self.addItem(item)
