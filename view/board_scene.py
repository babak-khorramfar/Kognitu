# view/board_scene.py

import math
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsTextItem
from PyQt5.QtCore import QRectF, Qt
from PyQt5.QtGui import QFont
from view.board_item import BoardItem
from utils.config import TILE_IMAGE_PATH, SPACING_FACTOR


class BoardScene(QGraphicsScene):
    def __init__(self, tile_image_path=TILE_IMAGE_PATH):
        super().__init__()
        self.tile_image_path = tile_image_path
        self.items_list = []
        self.tile_size = 0  # برای استفاده در محدودسازی

    def auto_layout(self, count, view_width, view_height, board_type="4-color"):
        self.clear_scene()
        self.setSceneRect(QRectF(0, 0, view_width, view_height))

        # رنگ‌ها
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

        # محاسبه سطر/ستون برای کل تخته‌ها
        cols = math.ceil(math.sqrt(count))
        rows = math.ceil(count / cols)

        # اندازه و فاصله
        tile_size_w = (view_width - 100) / (cols + (cols + 1) * (SPACING_FACTOR - 1))
        tile_size_h = view_height / (rows + (rows + 1) * (SPACING_FACTOR - 1))
        tile_size = int(min(tile_size_w, tile_size_h))
        spacing = tile_size * (SPACING_FACTOR - 1)
        self.tile_size = tile_size  # ذخیره برای later use

        # ناحیه رزرو شده سمت چپ برای START
        reserved_start_width = tile_size

        # محاسبه offset برای center کردن باقی گرید
        total_w = cols * tile_size + (cols - 1) * spacing
        total_h = rows * tile_size + (rows - 1) * spacing
        offset_x = (
            reserved_start_width + (view_width - reserved_start_width - total_w) / 2
        )
        offset_y = (view_height - total_h) / 2

        # اضافه کردن متن START
        self._add_start_label(tile_size, view_height)

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

    def _add_start_label(self, tile_size, scene_height):
        text_item = QGraphicsTextItem("START")
        font = QFont("Arial", int(tile_size / 2))
        text_item.setFont(font)
        text_item.setDefaultTextColor(Qt.black)
        text_item.setRotation(-90)

        # محاسبه محل قرارگیری وسط نوار سمت چپ
        x = tile_size / 2
        y = scene_height / 2 + text_item.boundingRect().width() / 2
        text_item.setPos(x, y)

        self.addItem(text_item)

    def clear_scene(self):
        for item in self.items_list:
            self.removeItem(item)
        self.items_list.clear()
        for item in self.items():
            if isinstance(item, QGraphicsTextItem):
                self.removeItem(item)
