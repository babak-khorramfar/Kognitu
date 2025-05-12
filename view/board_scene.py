# view/board_scene.py

import math
from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtGui import QPixmap
from view.board_item import BoardItem
from model.layout import Layout
from utils.config import TILE_IMAGE_PATH, SPACING_FACTOR


class BoardScene(QGraphicsScene):
    def __init__(self, tile_image_path: str, parent=None):
        super().__init__(parent)
        self.pixmap = QPixmap(tile_image_path)
        self.current_layout = None

    def load_layout(self, layout: Layout, view_w: int, view_h: int):
        self.clear()
        self.current_layout = layout

        placements = layout.placements
        if not placements:
            return

        cols = max(p.x for p in placements) + 1
        rows = max(p.y for p in placements) + 1

        factor = SPACING_FACTOR
        tile_size = int(
            min(
                view_w / (cols + (cols + 1) * factor),
                view_h / (rows + (rows + 1) * factor),
            )
        )
        spacing = tile_size * factor

        total_w = cols * tile_size + (cols + 1) * spacing
        total_h = rows * tile_size + (rows + 1) * spacing

        self.setSceneRect(0, 0, view_w, view_h)
        offset_x = (view_w - total_w) / 2 + spacing / 2
        offset_y = (view_h - total_h) / 2 + spacing / 2

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
