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
from PyQt5.QtCore import QPointF


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
        if board_type == "4 Core" and count == 8:
            top_y = view_height / 2 - tile_size - spacing / 2
            bottom_y = view_height / 2 + spacing / 2

            # استفاده از restricted_x به‌عنوان مرجع چپ چیدمان
            start_x = self.restricted_x + spacing

            for i in range(4):
                color = colors[i]
                face_down_path = f"{color_path}/{color}.png"
                for y in [top_y, bottom_y]:
                    x = start_x + i * (tile_size + spacing)
                    item = BoardItem(
                        face_up_path=self.tile_image_path,
                        face_down_path=face_down_path,
                        tile_size=tile_size,
                        spacing=spacing,
                    )
                    item.setPos(x, y)
                    self.addItem(item)
                    self.items_list.append(item)
            return

        if board_type == "4 Core" and count == 4:
            # چیدمان خاص به ترتیب ساعتگرد: 3 1 / 4 2
            start_x = (view_width - (2 * tile_size + spacing)) / 2
            start_y = (view_height - (2 * tile_size + spacing)) / 2

            # مکان‌ها: (row, col)
            positions = [
                (0, 1),  # شماره 1 - بالا راست (آبی)
                (1, 1),  # شماره 2 - پایین راست (قرمز)
                (0, 0),  # شماره 3 - بالا چپ (زرد)
                (1, 0),  # شماره 4 - پایین چپ (سبز)
            ]

            for i, (row, col) in enumerate(positions):
                color = colors[i]
                face_down_path = f"{color_path}/{color}.png"
                x = start_x + col * (tile_size + spacing)
                y = start_y + row * (tile_size + spacing)

                item = BoardItem(
                    face_up_path=self.tile_image_path,
                    face_down_path=face_down_path,
                    tile_size=tile_size,
                    spacing=spacing,
                )
                item.setPos(x, y)
                self.addItem(item)
                self.items_list.append(item)
            return

        if board_type == "4 Core" and count == 12:
            tile_size *= 0.8
            spacing = tile_size * 0.3
            self.tile_size = tile_size

            color_order = ["yellow", "red", "blue", "green"]

            block_cols = 3
            block_rows = 1
            block_w = 2 * tile_size + spacing
            block_h = 2 * tile_size + spacing

            total_w = block_cols * block_w + (block_cols - 1) * spacing
            total_h = block_rows * block_h + (block_rows - 1) * spacing

            start_x = max(
                self.restricted_x + spacing,
                (view_width - total_w) / 2,
            )
            start_y = (view_height - total_h) / 2

            def add_block(origin_x, origin_y):
                positions = [
                    (0, 0),  # بالا چپ = زرد
                    (0, 1),  # بالا راست = قرمز
                    (1, 0),  # پایین چپ = آبی
                    (1, 1),  # پایین راست = سبز
                ]
                for idx, (r, c) in enumerate(positions):
                    color = color_order[idx]
                    face_down_path = f"{color_path}/{color}.png"
                    item = BoardItem(
                        face_up_path=self.tile_image_path,
                        face_down_path=face_down_path,
                        tile_size=tile_size,
                        spacing=spacing,
                    )
                    item.setPos(origin_x + c * tile_size, origin_y + r * tile_size)
                    self.addItem(item)
                    self.items_list.append(item)

            for row in range(block_rows):  # 0 و 1 (بالا و پایین)
                for col in range(block_cols):  # 0 تا 2 (سه ستون)
                    x = start_x + col * (block_w + spacing)
                    y = start_y + row * (block_h + spacing)
                    add_block(x, y)

            return

        if board_type == "9 Full" and count == 9:
            # ترتیب رنگ‌ها بر اساس موقعیت موردنظر
            layout_3x3 = [
                [3, 6, 2],  # ردیف بالا ← زرد، طوسی، قرمز
                [5, 9, 7],  # وسط ← صورتی، قهوه‌ای، بنفش
                [1, 8, 4],  # پایین ← آبی، نارنجی، سبز
            ]

            color_map = {
                1: "blue",
                2: "red",
                3: "yellow",
                4: "green",
                5: "pink",
                6: "gray",
                7: "purple",
                8: "orange",
                9: "brown",
            }

            start_x = (view_width - (3 * tile_size + 2 * spacing)) / 2
            start_y = (view_height - (3 * tile_size + 2 * spacing)) / 2

            def snap(x, y):
                grid = 20
                return round(x / grid) * grid, round(y / grid) * grid

            for row in range(3):
                for col in range(3):
                    color_number = layout_3x3[row][col]
                    color = color_map[color_number]
                    face_down_path = f"{color_path}/{color}.png"

                    x = start_x + col * (tile_size + spacing)
                    y = start_y + row * (tile_size + spacing)
                    x, y = snap(x, y)

                    item = BoardItem(
                        face_up_path=self.tile_image_path,
                        face_down_path=face_down_path,
                        tile_size=tile_size,
                        spacing=spacing,
                    )
                    item.toggle_flip()  # پیش‌فرض پشت (face-down)
                    item.setPos(x, y)
                    self.addItem(item)
                    self.items_list.append(item)
            return

    def _add_start_label(self, tile_size, scene_height):
        # حذف آیتم‌های قبلی ثابت
        for item in getattr(self, "static_items", []):
            self.removeItem(item)
        self.static_items = []

        # --- قطب‌نما ---
        compass = QPixmap("resources/images/compass.png").scaled(
            100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        compass_item = QGraphicsPixmapItem(compass)
        compass_x = (tile_size - 100) / 2
        compass_y = tile_size * 0.1
        compass_item.setPos(compass_x, compass_y)
        self.addItem(compass_item)
        self.static_items.append(compass_item)

        # --- کلمه START ---
        text_item = QGraphicsTextItem("START")
        font = QFont("Game Changer", 42, QFont.Bold)
        text_item.setFont(font)
        text_item.setDefaultTextColor(Qt.darkRed)
        text_item.setRotation(90)
        self.addItem(text_item)
        self.static_items.append(text_item)

        # --- فلش ---
        arrow = QGraphicsTextItem("→")
        arrow.setFont(QFont("Game Changer", 38, QFont.Bold))
        arrow.setDefaultTextColor(Qt.darkRed)
        self.addItem(arrow)
        self.static_items.append(arrow)

        # --- محاسبه موقعیت عمودی (وسط صفحه) ---
        text_rect = text_item.boundingRect()
        arrow_rect = arrow.boundingRect()

        total_height = max(text_rect.width(), arrow_rect.height())
        center_y = (scene_height - total_height) / 2

        x = tile_size / 2
        text_item.setPos(x, center_y)

        arrow_x = x + 40  # فاصله افقی ثابت
        arrow_y = center_y + (text_rect.width() - arrow_rect.height()) / 2
        arrow.setPos(arrow_x, arrow_y)

        # --- خط‌چین جداکننده ---
        pen = QPen(QColor("#bbbbbb"))
        pen.setStyle(Qt.DashLine)
        pen.setWidth(2)
        line_x = arrow_x + arrow.boundingRect().width() + 10
        line = self.addLine(line_x, 0, line_x, scene_height, pen)
        self.static_items.append(line)

        # --- ذخیره موقعیت محدودیت قرارگیری تخته‌ها ---
        self.restricted_x = line_x

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

    def drawBackground(self, painter, rect):

        grid_size = 20
        # نمایش ندادن گرید، ولی حفظ کد برای آینده
        # painter.setPen(Qt.NoPen)
        return

        left = int(rect.left()) - (int(rect.left()) % grid_size)
        right = int(rect.right()) + grid_size
        top = int(rect.top()) - (int(rect.top()) % grid_size)
        bottom = int(rect.bottom()) + grid_size

        for x in range(left, right, grid_size):
            painter.drawLine(
                QPointF(x + 0.5, rect.top()), QPointF(x + 0.5, rect.bottom())
            )

        for y in range(top, bottom, grid_size):
            painter.drawLine(
                QPointF(rect.left(), y + 0.5), QPointF(rect.right(), y + 0.5)
            )
