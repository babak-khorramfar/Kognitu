# view/board_item.py

from PyQt5.QtWidgets import QGraphicsPixmapItem
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QPointF


class BoardItem(QGraphicsPixmapItem):
    def __init__(self, face_up_path, face_down_path, tile_size, spacing):
        super().__init__()

        self.tile_size = int(tile_size)
        self.spacing = spacing

        self.face_up_image = QPixmap(face_up_path).scaled(
            self.tile_size, self.tile_size, Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        self.face_down_image = QPixmap(face_down_path).scaled(
            self.tile_size, self.tile_size, Qt.KeepAspectRatio, Qt.SmoothTransformation
        )

        self.flipped = False
        self.setPixmap(self.face_up_image)

        self.setFlags(
            QGraphicsPixmapItem.ItemIsMovable
            | QGraphicsPixmapItem.ItemIsSelectable
            | QGraphicsPixmapItem.ItemSendsGeometryChanges
        )

        self.setTransformOriginPoint(self.boundingRect().center())
        self._last_pos = QPointF()
        self._last_rotation = 0

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            self.toggle_flip()
        else:
            self._last_pos = self.pos()
            self._last_rotation = self.rotation()
            super().mousePressEvent(event)

    def mouseDoubleClickEvent(self, event):
        self.setRotation((self.rotation() + 45) % 360)
        super().mouseDoubleClickEvent(event)

    def mouseReleaseEvent(self, event):
        scene = self.scene()
        if not scene:
            return super().mouseReleaseEvent(event)

        my_rect = self.sceneBoundingRect()
        if not scene.sceneRect().contains(my_rect) or self.pos().x() < scene.tile_size:
            self.setPos(self._last_pos)
            self.setRotation(self._last_rotation)
            return super().mouseReleaseEvent(event)

        for item in scene.items():
            if item is not self and isinstance(item, QGraphicsPixmapItem):
                if self.collidesWithItem(item):
                    self.setPos(self._last_pos)
                    self.setRotation(self._last_rotation)
                    break

        super().mouseReleaseEvent(event)

    def toggle_flip(self):
        self.flipped = not self.flipped
        self.setPixmap(self.face_down_image if self.flipped else self.face_up_image)
