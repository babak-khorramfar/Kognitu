# view/board_scene.py

from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtGui import QPixmap
from view.board_item import BoardItem


class BoardScene(QGraphicsScene):
    """
    Scene that arranges BoardItems based on placements and available view size.
    """

    def __init__(self, tile_image_path: str, parent=None):
        super().__init__(parent)
        # تصویر تک‌تخته (60×60px) که برای همه‌ی آیتم‌ها استفاده می‌شود
        self.pixmap = QPixmap(tile_image_path)

    def load_layout(self, placements, view_width, view_height, spacing):
        """
        placements: list of Placement
        view_width, view_height: available display area in pixels
        spacing: pixel gap between tiles
        """
        self.clear()
        # تعیین تعداد ستون و ردیف براساس مختصات حداکثر
        cols = max(p.x for p in placements) + 1
        rows = max(p.y for p in placements) + 1

        # محاسبه اندازه‌ی هر tile به‌نحوی که در پنجره جا شود
        tile_w = (view_width - spacing * (cols + 1)) / cols
        tile_h = (view_height - spacing * (rows + 1)) / rows
        tile_size = int(min(tile_w, tile_h))

        # به‌روزرسانی محدوده‌ی صحنه
        total_w = spacing + cols * (tile_size + spacing)
        total_h = spacing + rows * (tile_size + spacing)
        self.setSceneRect(0, 0, total_w, total_h)

        # افزودن هر BoardItem در موقعیت و زاویه‌ی درست
        for p in placements:
            item = BoardItem(p, self.pixmap, tile_size)
            x = spacing + p.x * (tile_size + spacing)
            y = spacing + p.y * (tile_size + spacing)
            item.setPos(x, y)
            item.setRotation(p.angle)
            self.addItem(item)
