# view/board_scene.py

import math
from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtCore import QRectF
from view.board_item import BoardItem
from utils.config import TILE_IMAGE_PATH, SPACING_FACTOR


class BoardScene(QGraphicsScene):
    def __init__(self, tile_image_path=TILE_IMAGE_PATH):
        super().__init__()
        self.tile_image_path = tile_image_path
        self.items_list = []

    def auto_layout(self, count, view_width, view_height, board_type="4-color"):
        self.clear_scene()
        self.setSceneRect(QRectF(0, 0, view_width, view_height))

        # تعریف رنگ‌ها بر اساس نوع تخته
        if board_type == "4-color":
            colors = ["blue", "red", "yellow", "green"]
            color_path = "resources/images/backs/4colors"
        else:
            colors = [
                "blue",
                "red",
                "yellow",
                "green",
                "orange",
                "gray",
                "purple",
                "brown",
                "pink",
            ]
            color_path = "resources/images/backs/9colors"

        count_per_color = count // len(colors)

        # محاسبه سطر/ستون برای چیدمان
        cols = math.ceil(math.sqrt(count))
        rows = math.ceil(count / cols)

        tile_size_w = view_width / (cols + (cols + 1) * (SPACING_FACTOR - 1))
        tile_size_h = view_height / (rows + (rows + 1) * (SPACING_FACTOR - 1))
        tile_size = int(min(tile_size_w, tile_size_h))
        spacing = tile_size * (SPACING_FACTOR - 1)

        total_w = cols * tile_size + (cols - 1) * spacing
        total_h = rows * tile_size + (rows - 1) * spacing
        offset_x = (view_width - total_w) / 2
        offset_y = (view_height - total_h) / 2

        # ساخت تخته‌ها
        index = 0
        for color in colors:
            for _ in range(count_per_color):
                row = index // cols
                col = index % cols
                x = offset_x + col * (tile_size + spacing)
                y = offset_y + row * (tile_size + spacing)

                face_down_path = f"{color_path}/{color}.png"
                item = BoardItem(
                    face_up_path=self.tile_image_path,
                    face_down_path=face_down_path,
                    tile_size=tile_size,
                    spacing=spacing,
                )
                item.setPos(x, y)
                self.addItem(item)
                self.items_list.append(item)
                index += 1

    def clear_scene(self):
        for item in self.items_list:
            self.removeItem(item)
        self.items_list.clear()
