# view/board_scene.py

import math
from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtCore import QRectF
from view.board_item import BoardItem
from utils.config import SPACING_FACTOR


class BoardScene(QGraphicsScene):
    def __init__(self, tile_image_path):
        super().__init__()
        self.tile_image_path = tile_image_path
        self.items_list = []

    def auto_layout(self, count, view_width, view_height):
        # پاک‌سازی صحنه و آیتم‌ها
        for item in self.items():
            self.removeItem(item)
        self.items_list.clear()
        self.setSceneRect(QRectF(0, 0, view_width, view_height))

        # تعداد ردیف و ستون
        cols = math.ceil(math.sqrt(count))
        rows = math.ceil(count / cols)

        # محاسبه tile_size و spacing
        spacing_factor = SPACING_FACTOR  # مثلاً √2
        tile_size_w = view_width / (cols + (cols + 1) * (spacing_factor - 1))
        tile_size_h = view_height / (rows + (rows + 1) * (spacing_factor - 1))
        tile_size = int(min(tile_size_w, tile_size_h))
        spacing = tile_size * (spacing_factor - 1)

        # مرکزچین کردن گرید
        total_w = cols * tile_size + (cols - 1) * spacing
        total_h = rows * tile_size + (rows - 1) * spacing
        offset_x = (view_width - total_w) / 2
        offset_y = (view_height - total_h) / 2

        # ساخت و اضافه کردن تخته‌ها
        for i in range(count):
            row = i // cols
            col = i % cols
            x = offset_x + col * (tile_size + spacing)
            y = offset_y + row * (tile_size + spacing)

            item = BoardItem(
                image_path=self.tile_image_path, tile_size=tile_size, spacing=spacing
            )
            item.setPos(x, y)
            self.addItem(item)
            self.items_list.append(item)
