# view/board_item.py

from PyQt5.QtWidgets import QGraphicsPixmapItem, QGraphicsItem
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QPointF


class BoardItem(QGraphicsPixmapItem):
    def __init__(self, controller, pixmap_path, tile_size, spacing):
        super().__init__()
        self.controller = controller
        self.tile_size = int(tile_size)  # اطمینان به int بودن
        self.spacing = float(spacing)

        # بارگذاری تصویر و تغییر سایز
        pm = QPixmap(pixmap_path)
        pm = pm.scaled(
            self.tile_size, self.tile_size, Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        self.setPixmap(pm)

        # مجاز بودن جابه‌جایی و ارسال تغییرات
        self.setFlags(
            QGraphicsItem.ItemIsMovable
            | QGraphicsItem.ItemIsSelectable
            | QGraphicsItem.ItemSendsGeometryChanges
        )
        # مرکز چرخش وسط تصویر
        self.setTransformOriginPoint(pm.width() / 2, pm.height() / 2)

        # ذخیرهٔ موقعیت و زاویهٔ قبل برای rollback
        from PyQt5.QtCore import QPointF

        self._last_pos = QPointF()
        self._last_angle = 0

    def mousePressEvent(self, event):
        # ذخیرهٔ حالت قبل از حرکت/چرخش
        self._last_pos = self.pos()
        self._last_angle = self.rotation()
        super().mousePressEvent(event)

    def contextMenuEvent(self, event):
        # راست‌کلیک چرخش 45 درجه
        angle = (self.rotation() + 45) % 360
        self.setRotation(angle)

    def mouseReleaseEvent(self, event):
        # پس از آزادسازی ماوس، بررسی برخورد و خروج از صحنه
        scene = self.scene()
        from PyQt5.QtCore import QRectF

        newRect = self.sceneBoundingRect()

        # اگر از صحنه خارج شد
        if not scene.sceneRect().contains(newRect):
            self.setPos(self._last_pos)
            self.setRotation(self._last_angle)
        else:
            # بررسی برخورد با دیگر آیتم‌ها
            for other in scene.items():
                if other is self:
                    continue
                if newRect.intersects(other.sceneBoundingRect()):
                    self.setPos(self._last_pos)
                    self.setRotation(self._last_angle)
                    break

        super().mouseReleaseEvent(event)
