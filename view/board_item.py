# view/board_item.py

from PyQt5.QtWidgets import QGraphicsPixmapItem, QGraphicsItem
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap


class BoardItem(QGraphicsPixmapItem):
    """
    A QGraphicsPixmapItem representing one board tile.
    Supports drag & drop and 45° rotation via right-click.
    """

    def __init__(self, placement, pixmap: QPixmap, tile_size: int, spacing: int):
        super().__init__(pixmap)
        self.placement = placement
        self.tile_size = tile_size
        self.spacing = spacing

        # Scale the pixmap to tile_size
        self.setTransformationMode(Qt.SmoothTransformation)
        self.setScale(self.tile_size / self.pixmap().width())

        # Enable moving and selection
        self.setFlags(
            QGraphicsItem.ItemIsMovable
            | QGraphicsItem.ItemIsSelectable
            | QGraphicsItem.ItemSendsGeometryChanges
        )

        # Initial position & rotation
        self.update_position()

    def update_position(self):
        """
        Position the item according to its placement,
        using grid coordinates, tile_size and spacing.
        """
        x = self.placement.x * (self.tile_size + self.spacing) + self.spacing
        y = self.placement.y * (self.tile_size + self.spacing) + self.spacing
        self.setPos(x, y)
        self.setRotation(self.placement.angle)

    def contextMenuEvent(self, event):
        """
        Right-click rotates the tile by 45° clockwise.
        """
        self.placement.angle = (self.placement.angle + 45) % 360
        self.setRotation(self.placement.angle)
