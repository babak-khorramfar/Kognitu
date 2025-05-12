# view/board_item.py

from PyQt5.QtWidgets import QGraphicsPixmapItem, QGraphicsItem
from PyQt5.QtCore import Qt, QPointF


class BoardItem(QGraphicsPixmapItem):
    def __init__(
        self, placement, pixmap, tile_size, spacing, offset_x, offset_y, scene_rect
    ):
        super().__init__(pixmap)
        self.placement = placement
        self.tile_size = tile_size
        self.spacing = spacing
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.scene_rect = scene_rect

        self.setFlags(
            QGraphicsItem.ItemIsMovable
            | QGraphicsItem.ItemIsSelectable
            | QGraphicsItem.ItemSendsGeometryChanges
        )
        self.setTransformationMode(Qt.SmoothTransformation)
        self.setTransformOriginPoint(pixmap.width() / 2, pixmap.height() / 2)
        self.setScale(tile_size / pixmap.width())

    def contextMenuEvent(self, event):
        self.placement.angle = (self.placement.angle + 45) % 360
        self.setRotation(self.placement.angle)

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionChange and isinstance(value, QPointF):
            # اسنپ به نزدیکترین مرکز فاصله‌ای
            newPos = value
            grid = self.tile_size + self.spacing
            # محاسبهٔ نزدیک‌ترین موقعیت با همان spacing
            colf = (newPos.x() - self.offset_x) / grid
            rowf = (newPos.y() - self.offset_y) / grid
            # گرد کردن اعشار برای اسنپ
            col = round(colf)
            row = round(rowf)
            x = self.offset_x + col * grid
            y = self.offset_y + row * grid
            # محدود کردن درون صحنه
            x = min(
                max(x, self.scene_rect.left()), self.scene_rect.right() - self.tile_size
            )
            y = min(
                max(y, self.scene_rect.top()), self.scene_rect.bottom() - self.tile_size
            )
            self.placement.x, self.placement.y = col, row
            return QPointF(x, y)
        return super().itemChange(change, value)
