# view/board_scene.py

import math
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsTextItem
from PyQt5.QtCore import QRectF, Qt
from PyQt5.QtGui import QFont
from view.board_item import BoardItem
from utils.config import TILE_IMAGE_PATH, SPACING_FACTOR
from PyQt5.QtGui import QPen, QColor
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QGraphicsPixmapItem


class BoardScene(QGraphicsScene):
    def __init__(self, tile_image_path=TILE_IMAGE_PATH):
        super().__init__()
        self.tile_image_path = tile_image_path
        self.items_list = []
        self.static_items = []
        self.tile_size = 0  # برای استفاده در محدودسازی
        self.restricted_x = None  # محل خط‌چین که باید محدودیت از اون اعمال بشه

    def auto_layout(self, count, view_width, view_height, board_type="4 Core"):
        self.clear_scene()
        self.setSceneRect(QRectF(0, 0, view_width, view_height))

        # رنگ‌ها
        if board_type == "4 Core":
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
        reserved_start_width = int(tile_size * 0.6)

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
        # کلمه START
        text_item = QGraphicsTextItem("START")
        font = QFont("Pixel Game", 42, QFont.Bold)
        text_item.setFont(font)
        text_item.setDefaultTextColor(Qt.darkRed)
        text_item.setRotation(90)

        # تصویر قطب‌نما
        compass = QPixmap("resources/images/compass.png").scaled(
            100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        compass_item = QGraphicsPixmapItem(compass)

        # جای‌گذاری: بالا و وسط عرض محوطه START (که tile_size پهنا داره)
        x = (tile_size - 100) / 2  # 100 = عرض تصویر
        y = tile_size * 0.1  # کمی فاصله از بالا

        compass_item.setPos(x, y)
        self.addItem(compass_item)
        self.static_items.append(compass_item)

        # محاسبه موقعیت وسط صفحه
        x = tile_size / 2
        y = (scene_height - text_item.boundingRect().height()) / 2

        text_item.setPos(x, y)
        self.addItem(text_item)
        self.static_items.append(text_item)

        # فلش سمت راست
        arrow = QGraphicsTextItem("→")
        arrow.setFont(QFont("Pixel Game", 38, QFont.Bold))
        arrow.setDefaultTextColor(Qt.darkRed)

        arrow_x = x + 40  # به‌صورت تجربی، این مقدار نزدیک‌ترین فاصله‌ست

        arrow_y = (
            y + (text_item.boundingRect().width() - arrow.boundingRect().height()) / 2
        )

        arrow.setPos(arrow_x, arrow_y)
        self.addItem(arrow)
        self.static_items.append(arrow)

        # خط‌چین جداکننده
        from PyQt5.QtGui import QPen, QColor

        pen = QPen(QColor("#bbbbbb"))
        pen.setStyle(Qt.DashLine)
        pen.setWidth(2)

        line_x = arrow_x + arrow.boundingRect().width() + 10
        line = self.addLine(line_x, 0, line_x, scene_height, pen)
        self.static_items.append(line)
        self.restricted_x = line_x  # ذخیره محل خط‌چین برای مقایسه بعدی

    def clear_scene(self):
        for item in self.items_list:
            self.removeItem(item)
        self.items_list.clear()
        for item in self.items():
            if isinstance(item, QGraphicsTextItem):
                self.removeItem(item)

        for item in self.static_items:
            self.removeItem(item)
        self.static_items.clear()
