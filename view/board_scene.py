# view/board_scene.py

from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtGui import QPixmap
from view.board_item import BoardItem
from model.layout import Layout
from utils.config import TILE_IMAGE_PATH, SPACING_RATIO


class BoardScene(QGraphicsScene):
    def __init__(self, tile_image_path: str, parent=None):
        super().__init__(parent)
        self.pixmap = QPixmap(tile_image_path)

    def load_layout(self, layout: Layout, view_w: int, view_h: int):
        self.clear()
        placements = layout.placements
        if not placements:
            return

        # تعداد ردیف و ستون
        cols = max(p.x for p in placements) + 1
        rows = max(p.y for p in placements) + 1

        # ابتدا حداکثر سایز tile بر اساس view محاسبه می‌کنیم
        # با فرض spacing نسبت به tile ثابت
        # total_w = cols*tile + (cols-1)*spacing
        # spacing = tile * SPACING_RATIO
        # بنابراین total_w = tile*(cols + (cols-1)*SPACING_RATIO)
        factor = 1 + (cols - 1) * SPACING_RATIO / cols
        tile_w = view_w / (cols + (cols - 1) * SPACING_RATIO)
        tile_h = view_h / (rows + (rows - 1) * SPACING_RATIO)
        tile_size = int(min(tile_w, tile_h))
        spacing = tile_size * SPACING_RATIO

        # عرض و ارتفاع گرید
        total_w = cols * tile_size + (cols - 1) * spacing
        total_h = rows * tile_size + (rows - 1) * spacing

        # مرکزچین‌سازی
        offset_x = (view_w - total_w) / 2
        offset_y = (view_h - total_h) / 2

        # تنظیم صحنه
        self.setSceneRect(0, 0, view_w, view_h)

        # اضافه کردن آیتم‌ها
        for p in placements:
            item = BoardItem(
                placement=p,
                pixmap=self.pixmap,
                tile_size=tile_size,
                spacing=spacing,
                offset_x=offset_x,
                offset_y=offset_y,
                scene_rect=self.sceneRect(),
            )
            x = offset_x + p.x * (tile_size + spacing)
            y = offset_y + p.y * (tile_size + spacing)
            item.setPos(x, y)
            item.setRotation(p.angle)
            self.addItem(item)
