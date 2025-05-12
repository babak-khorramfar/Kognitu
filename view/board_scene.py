# view/board_scene.py

from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtGui import QPixmap
from view.board_item import BoardItem


class BoardScene(QGraphicsScene):
    """
    Scene that arranges BoardItems in a centered grid with dynamic tile size
    ensuring full view usage and spacing equal to tile_size.
    """

    def __init__(self, tile_image_path: str, parent=None):
        super().__init__(parent)
        self.pixmap = QPixmap(tile_image_path)

    def load_layout(self, placements, view_width, view_height):
        """
        placements: list of Placement
        view_width, view_height: available display area in pixels
        """
        self.clear()
        cols = max(p.x for p in placements) + 1
        rows = max(p.y for p in placements) + 1

        # spacing equals tile_size: total width = (2*cols+1)*tile_size <= view_width
        tile_size_w = view_width / (2 * cols + 1)
        tile_size_h = view_height / (2 * rows + 1)
        tile_size = int(min(tile_size_w, tile_size_h))
        spacing = tile_size

        total_w = cols * tile_size + (cols + 1) * spacing
        total_h = rows * tile_size + (rows + 1) * spacing

        # full scene covers entire view area
        self.setSceneRect(0, 0, view_width, view_height)

        # center offsets
        offset_x = (view_width - total_w) / 2
        offset_y = (view_height - total_h) / 2

        for p in placements:
            item = BoardItem(p, self.pixmap, tile_size)
            x = offset_x + spacing + p.x * (tile_size + spacing)
            y = offset_y + spacing + p.y * (tile_size + spacing)
            item.setPos(x, y)
            item.setRotation(p.angle)
            self.addItem(item)
