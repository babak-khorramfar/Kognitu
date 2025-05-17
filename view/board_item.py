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

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)

        if self.rotation() % 90 != 0:
            return

        scene = self.scene()
        if not scene:
            return

        my_rect = self.sceneBoundingRect()
        snap_threshold = 20

        for item in scene.items():
            if item is self or not isinstance(item, QGraphicsPixmapItem):
                continue

            other_rect = item.sceneBoundingRect()
            dx = dy = 0

            # Snap logic during drag
            if abs(my_rect.right() - other_rect.left()) < snap_threshold:
                if abs(my_rect.top() - other_rect.top()) < snap_threshold:
                    dx = other_rect.left() - my_rect.right()
                    dy = other_rect.top() - my_rect.top()
            elif abs(my_rect.left() - other_rect.right()) < snap_threshold:
                if abs(my_rect.top() - other_rect.top()) < snap_threshold:
                    dx = other_rect.right() - my_rect.left()
                    dy = other_rect.top() - my_rect.top()
            elif abs(my_rect.bottom() - other_rect.top()) < snap_threshold:
                if abs(my_rect.left() - other_rect.left()) < snap_threshold:
                    dy = other_rect.top() - my_rect.bottom()
                    dx = other_rect.left() - my_rect.left()
            elif abs(my_rect.top() - other_rect.bottom()) < snap_threshold:
                if abs(my_rect.left() - other_rect.left()) < snap_threshold:
                    dy = other_rect.bottom() - my_rect.top()
                    dx = other_rect.left() - my_rect.left()

            if dx != 0 or dy != 0:
                self.moveBy(dx, dy)
                break

    def mouseReleaseEvent(self, event):
        scene = self.scene()
        if not scene:
            return super().mouseReleaseEvent(event)

        grid_size = 20

        def is_illegal(pos: QPointF):
            original = self.pos()
            self.setPos(pos)
            illegal = not scene.sceneRect().contains(self.sceneBoundingRect()) or (
                hasattr(scene, "restricted_x")
                and self.scenePos().x() < scene.restricted_x
            )
            if not illegal:
                for item in scene.items():
                    if item is self or not isinstance(item, QGraphicsPixmapItem):
                        continue
                    if self.collidesWithItem(item):
                        illegal = True
                        break
            self.setPos(original)
            return illegal

        # اگه موقعیت فعلی قانونی بود → هیچی نکن
        if not is_illegal(self.pos()):
            return super().mouseReleaseEvent(event)

        # مرکز فعلی
        center = self.sceneBoundingRect().center()

        # اسنپ به گرید پایه
        base_x = (
            round(center.x() / grid_size) * grid_size - self.boundingRect().width() / 2
        )
        base_y = (
            round(center.y() / grid_size) * grid_size - self.boundingRect().height() / 2
        )

        # جستجوی شعاعی اطراف نقطه فعلی تا حداکثر 7x7
        max_radius = 3
        for r in range(1, max_radius + 1):
            for dx in range(-r, r + 1):
                for dy in range(-r, r + 1):
                    candidate = QPointF(
                        base_x + dx * grid_size, base_y + dy * grid_size
                    )
                    if not is_illegal(candidate):
                        self.setPos(candidate)
                        return super().mouseReleaseEvent(event)

        # اگه جایی پیدا نشد → بازگشت به موقعیت قبل
        self.setPos(self._last_pos)
        self.setRotation(self._last_rotation)
        return super().mouseReleaseEvent(event)

    def toggle_flip(self):
        self.flipped = not self.flipped
        current_pos = self.pos()
        self.setPixmap(self.face_down_image if self.flipped else self.face_up_image)
        self.setPos(current_pos)
