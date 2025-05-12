# view/board_item.py

from PyQt5.QtWidgets import QGraphicsPixmapItem, QGraphicsItem
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QTransform


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
        # راست‌کلیک چرخش 45 درجه
        self.placement.angle = (self.placement.angle + 45) % 360
        self.setRotation(self.placement.angle)

    def itemChange(self, change, value):
        from PyQt5.QtCore import QRectF

        if change == QGraphicsItem.ItemPositionChange and isinstance(value, QPointF):
            scene = self.scene()
            if scene is None:
                return super().itemChange(change, value)

            newPos = value
            grid = self.tile_size + self.spacing

            # اسنپ به نزدیکترین نقطه‌ی گرید
            col = round((newPos.x() - self.offset_x) / grid)
            row = round((newPos.y() - self.offset_y) / grid)
            x = self.offset_x + col * grid
            y = self.offset_y + row * grid

            # محدود کردن درون صحنه (با احتساب اندازه‌ی واقعی آیتم)
            br = self.boundingRect().size() * self.scale()
            w, h = br.width(), br.height()
            x = min(max(x, self.scene_rect.left()), self.scene_rect.right() - w)
            y = min(max(y, self.scene_rect.top()), self.scene_rect.bottom() - h)

            # جلوگیری از هم‌پوشانی با دیگر آیتم‌ها
            newRect = QRectF(x, y, w, h)
            for other in scene.items():
                if other is not self and isinstance(other, BoardItem):
                    # رکت دیگر آیتم
                    obr = other.boundingRect().size() * other.scale()
                    orx = other.pos().x()
                    ory = other.pos().y()
                    otherRect = QRectF(orx, ory, obr.width(), obr.height())
                    if newRect.intersects(otherRect):
                        # اگر تداخل داشت، حرکت را لغو کن
                        return super().itemChange(change, self.pos())

            # تأیید موقعیت جدید
            self.placement.x, self.placement.y = col, row
            return QPointF(x, y)

        return super().itemChange(change, value)
