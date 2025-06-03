from PyQt5.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QComboBox,
    QPushButton,
    QGraphicsView,
    QFrame,
    QFileDialog,
    QMessageBox,
)
from PyQt5.QtGui import QPixmap, QCursor
from PyQt5.QtCore import Qt, QTimer, QEvent, QPointF
import json
from view.board_scene import BoardScene
from utils.config import TILE_IMAGE_PATH
from view.board_item import BoardItem


class GameWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.showFullScreen()

        self.view = QGraphicsView()
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scene = BoardScene(tile_image_path=TILE_IMAGE_PATH)
        self.view.setScene(self.scene)

        self._init_ui()

    def _init_ui(self):
        sidebar_frame = QFrame()
        sidebar_layout = QVBoxLayout(sidebar_frame)
        sidebar_layout.setAlignment(Qt.AlignTop)
        sidebar_frame.setFixedWidth(250)

        label_type = QLabel("Board Type:")
        self.combo_type = QComboBox()
        self.combo_type.addItems(["4 Core", "9 Full"])
        self.combo_type.currentIndexChanged.connect(self.update_count_options)

        self.label_count = QLabel("Board Count:")
        self.combo_count = QComboBox()

        btn_generate = QPushButton("Generate Layout")
        btn_generate.clicked.connect(self._do_layout)

        btn_save = QPushButton("💾 Save Layout")
        btn_save.clicked.connect(self.save_layout)

        btn_load = QPushButton("📥 Load Layout")
        btn_load.clicked.connect(self.load_layout)

        btn_back = QPushButton("← Back to Launcher")
        btn_back.clicked.connect(self.back_to_launcher)
        btn_back.setStyleSheet(
            "background-color: #95a5a6; color: white; font-weight: bold;"
        )

        for widget in [
            label_type,
            self.combo_type,
            self.label_count,
            self.combo_count,
            btn_generate,
        ]:
            sidebar_layout.addWidget(widget)
            sidebar_layout.addSpacing(10)

        sidebar_layout.addStretch(1)
        sidebar_layout.addSpacing(20)
        sidebar_layout.addWidget(btn_save)
        sidebar_layout.addWidget(btn_load)
        sidebar_layout.addSpacing(10)
        sidebar_layout.addWidget(btn_back)

        sidebar_frame.setStyleSheet(
            """
            QFrame {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                                  stop:0 #34495e, stop:1 #2c3e50);
            }
            QLabel {
                font-family: "Game Changer";
                font-size: 24px;
                color: #f0f0f0;
                font-weight: bold;
            }
            QComboBox {
                font-family: "Game Changer";
                font-size: 22px;
                padding: 6px 12px;
                border-radius: 10px;
                background-color: #ecf0f1;
                border: 2px solid #f39c12;
                color: #2c3e50;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 30px;
                border-left: 1px solid #aaa;
                border-top-right-radius: 10px;
                border-bottom-right-radius: 10px;
            }
            QComboBox QAbstractItemView {
                background-color: #ffffff;
                selection-background-color: #f39c12;
                selection-color: white;
                border: 1px solid #bdc3c7;
                font-size: 22px;
            }
            QPushButton {
                font-family: "Game Changer";
                font-size: 28px;
                padding: 10px 20px;
                border-radius: 16px;
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                  stop:0 #fcd34d, stop:1 #f97316);
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #f59e0b;
            }
        """
        )

        layout = QHBoxLayout()
        layout.addWidget(sidebar_frame)
        layout.addWidget(self.view, stretch=1)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.update_count_options()
        self.view.viewport().installEventFilter(self)

        self.help_icon = QLabel(self)
        self.help_icon.setPixmap(
            QPixmap("resources/images/help.png").scaled(
                58, 58, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
        )
        self.help_icon.setToolTip(
            "<div style='font-family:\"Arial\"; font-size:18px;'>"
            "🖱️ <b>Right click</b>: Flip board<br>"
            "🖱️ <b>Double click</b>: Rotate 45°<br>"
            "🖱️ <b>Drag & Drop</b>: Move Board</div>"
        )
        self.help_icon.setStyleSheet(
            "QToolTip { background-color: #2c3e50; color: white; padding: 6px; border-radius: 5px; }"
        )
        self.help_icon.resize(58, 58)
        self.help_icon.show()

        def reposition_help_icon():
            x = self.width() - 90
            y = 25
            self.help_icon.move(x, y)

        reposition_help_icon()
        self.resizeEvent = lambda event: (
            reposition_help_icon(),
            super().resizeEvent(event),
        )

    def update_count_options(self):
        self.combo_count.clear()
        if self.combo_type.currentText() == "4 Core":
            self.combo_count.addItems(["4", "8", "12"])
            self.label_count.show()
            self.combo_count.show()
        else:
            self.label_count.hide()
            self.combo_count.hide()

    def _do_layout(self):
        board_type = self.combo_type.currentText()
        count = int(self.combo_count.currentText()) if board_type == "4 Core" else 9
        w = self.view.viewport().width()
        h = self.view.viewport().height()
        self.scene.auto_layout(count, w, h, board_type=board_type)

    def save_layout(self):
        path, _ = QFileDialog.getSaveFileName(
            self, "Save Layout", "", "HipHop Layout (*.hht)"
        )
        if not path:
            return
        data = {
            "board_type": self.combo_type.currentText(),
            "board_count": (
                int(self.combo_count.currentText())
                if self.combo_count.isVisible()
                else 9
            ),
            "boards": [],
        }
        for item in self.scene.items_list:
            center = item.mapToScene(item.boundingRect().center())
            data["boards"].append(
                {
                    "x": center.x(),
                    "y": center.y(),
                    "rotation": item.rotation(),
                    "flipped": item.flipped,
                    "face_down_path": item.face_down_image_path,
                    "tile_size": item.tile_size,
                }
            )
        with open(path, "w") as f:
            json.dump(data, f)

    def load_layout(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Load Layout", "", "HipHop Layout (*.hht)"
        )
        if not path:
            return
        try:
            with open(path, "r") as f:
                data = json.load(f)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Load failed:\n{e}")
            return

        self.combo_type.setCurrentText(data["board_type"])
        self.update_count_options()
        if self.combo_count.isVisible():
            self.combo_count.setCurrentText(str(data["board_count"]))

        w = self.view.viewport().width()
        h = self.view.viewport().height()
        self.scene.clear_scene()
        self.scene.setSceneRect(0, 0, w, h)
        self.scene._add_start_label(self.scene.tile_size or 100, h)

        self.scene.items_list = []
        for b in data["boards"]:
            item = BoardItem(
                face_up_path=TILE_IMAGE_PATH,
                face_down_path=b["face_down_path"],
                tile_size=b["tile_size"],
                spacing=0,
            )
            item.setRotation(b["rotation"])
            item.flipped = b["flipped"]
            item.setPixmap(item.face_down_image if item.flipped else item.face_up_image)
            # تعیین مرکز تخته در صحنه
            center = QPointF(b["x"], b["y"])
            offset = item.boundingRect().center()
            item.setPos(center - offset)
            self.scene.addItem(item)
            self.scene.items_list.append(item)

    def eventFilter(self, source, event):
        if source is self.view.viewport() and event.type() == QEvent.Resize:
            QTimer.singleShot(50, self._do_layout)
        return super().eventFilter(source, event)

    def back_to_launcher(self):
        from view.main_window import MainLauncherWindow

        self.launcher = MainLauncherWindow()
        self.launcher.show()
        self.close()

    def closeEvent(self, event):
        self.back_to_launcher()
