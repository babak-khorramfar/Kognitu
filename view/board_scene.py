# view/board_scene.py

import math
from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtGui import QPixmap
from view.board_item import BoardItem
from utils.config import DIAGONAL_SPACING_FACTOR


class BoardScene(QGraphicsScene):
    """
    Scene that arranges BoardItems centered with dynamic tile size
    and minimal spacing to prevent any overlap when rotated at 45 degrees.
    """

    def __init__(self, tile_image_path: str, parent=None):
        super().__init__(parent)
        self.pixmap = QPixmap(tile_image_path)

    def load_layout(self, placements, view_width, view_height):
        self.clear()
        if not placements:
            return

        cols = max(p.x for p in placements) + 1
        rows = max(p.y for p in placements) + 1

        factor = DIAGONAL_SPACING_FACTOR  # ≈ sqrt(2)-1
        # Compute grid factors
        grid_factor_x = cols + (cols + 1) * factor
        grid_factor_y = rows + (rows + 1) * factor

        # Determine tile size to fit in view
        tile_size = int(min(view_width / grid_factor_x, view_height / grid_factor_y))
        spacing = tile_size * factor

        total_w = cols * tile_size + (cols + 1) * spacing
        total_h = rows * tile_size + (rows + 1) * spacing

        # Use full view rect
        self.setSceneRect(0, 0, view_width, view_height)

        # Center offsets
        offset_x = (view_width - total_w) / 2
        offset_y = (view_height - total_h) / 2

        for p in placements:
            item = BoardItem(p, self.pixmap, tile_size, spacing)
            x = offset_x + spacing + p.x * (tile_size + spacing)
            y = offset_y + spacing + p.y * (tile_size + spacing)
            item.setPos(x, y)
            item.setRotation(p.angle)
            self.addItem(item)
