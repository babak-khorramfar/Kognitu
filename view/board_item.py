# view/board_item.py

from PyQt5.QtWidgets import QGraphicsPixmapItem, QGraphicsItem
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QPixmap


class BoardItem(QGraphicsPixmapItem):
    # Graphics item for a board tile.
    # Supports drag & drop snapping to grid and 45-degree rotation on right-click.
    # placement: model.Placement instance
    # tile_size: pixel size for display
    def __init__(self, placement, pixmap: QPixmap, tile_size: int, spacing: int):
        super().__init__(pixmap)
        self.placement = placement
        self.tile_size = tile_size
        self.spacing = spacing

        self.setFlags(
            QGraphicsItem.ItemIsMovable
            | QGraphicsItem.ItemIsSelectable
            | QGraphicsItem.ItemSendsGeometryChanges
        )
        self.setTransformationMode(Qt.SmoothTransformation)
        # rotate around center
        self.setTransformOriginPoint(pixmap.width() / 2, pixmap.height() / 2)
        scale_factor = tile_size / pixmap.width()
        self.setScale(scale_factor)

    def contextMenuEvent(self, event):
        # Right-click rotates by 45 degrees clockwise around center.
        self.placement.angle = (self.placement.angle + 45) % 360
        self.setRotation(self.placement.angle)

    def itemChange(self, change, value):
        # Snap to grid on position change.
        if change == QGraphicsItem.ItemPositionChange and isinstance(value, QPointF):
            newPos = value
            grid_size = self.tile_size + self.spacing
            col = round((newPos.x() - self.spacing) / grid_size)
            row = round((newPos.y() - self.spacing) / grid_size)
            col = max(0, col)
            row = max(0, row)
            self.placement.x = col
            self.placement.y = row
            x = self.spacing + col * grid_size
            y = self.spacing + row * grid_size
            return QPointF(x, y)
        return super().itemChange(change, value)
