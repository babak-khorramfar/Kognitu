# view/board_scene.py

from PyQt5.QtWidgets import QGraphicsScene
from view.board_item import BoardItem
from PyQt5.QtGui import QPixmap


class BoardScene(QGraphicsScene):
    """
    A QGraphicsScene that displays a grid of BoardItem instances
    with proper spacing and tile sizing.
    """

    def __init__(
        self,
        rows: int,
        cols: int,
        tile_image_path: str,
        tile_size: int,
        spacing: int,
        parent=None,
    ):
        super().__init__(parent)
        self.rows = rows
        self.cols = cols
        self.tile_size = tile_size
        self.spacing = spacing

        # Load the tile image
        self.tile_image = QPixmap(tile_image_path)

        # Compute total scene size:
        total_w = cols * tile_size + (cols + 1) * spacing
        total_h = rows * tile_size + (rows + 1) * spacing
        self.setSceneRect(0, 0, total_w, total_h)

    def load_layout(self, layout):
        """
        Clear the scene and add one BoardItem per placement in layout.
        """
        self.clear()
        for placement in layout.placements:
            item = BoardItem(placement, self.tile_image, self.tile_size, self.spacing)
            self.addItem(item)
