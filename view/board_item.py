# view/board_item.py

from PyQt5.QtWidgets import QGraphicsPixmapItem
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QPixmap


class BoardItem(QGraphicsPixmapItem):
    def __init__(self, image_path, tile_size, spacing):
        super().__init__()

        self.tile_size = int(tile_size)
        self.spacing = spacing

        # بارگذاری تصویر و مقیاس‌دهی
        pixmap = QPixmap(image_path)
        pixmap = pixmap.scaled(
            self.tile_size, self.tile_size, Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        self.setPixmap(pixmap)

        # فعال‌سازی قابلیت جابجایی و انتخاب
        self.setFlags(
            QGraphicsPixmapItem.ItemIsMovable
            | QGraphicsPixmapItem.ItemIsSelectable
            | QGraphicsPixmapItem.ItemSendsGeometryChanges
        )

        # نقطهٔ چرخش: مرکز تصویر
        self.setTransformOriginPoint(self.boundingRect().center())

        # ذخیره موقعیت قبلی برای بازگشت در صورت برخورد
        self._last_pos = QPointF()
        self._last_rotation = 0

    def mousePressEvent(self, event):
        self._last_pos = self.pos()
        self._last_rotation = self.rotation()
        super().mousePressEvent(event)

    def mouseDoubleClickEvent(self, event):
        # چرخش ۴۵ درجه در هر دابل‌کلیک
        self.setRotation((self.rotation() + 45) % 360)
        super().mouseDoubleClickEvent(event)

    def mouseReleaseEvent(self, event):
        scene = self.scene()
        if not scene:
            return super().mouseReleaseEvent(event)

        my_rect = self.sceneBoundingRect()

        # اگر از کادر صحنه خارج شد → بازگشت
        if not scene.sceneRect().contains(my_rect):
            self.setPos(self._last_pos)
            self.setRotation(self._last_rotation)
            return super().mouseReleaseEvent(event)

        # اگر با آیتمی دیگر برخورد داشت → بازگشت
        for item in scene.items():
            if item is not self and isinstance(item, QGraphicsPixmapItem):
                if self.collidesWithItem(item):
                    self.setPos(self._last_pos)
                    self.setRotation(self._last_rotation)
                    break

        super().mouseReleaseEvent(event)
