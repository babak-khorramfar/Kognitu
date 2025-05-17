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
)
from PyQt5.QtCore import Qt, QTimer, QEvent
from view.board_scene import BoardScene
from model.layout import Layout
from utils.config import TILE_IMAGE_PATH


class GameWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kognitu - Manual Game")
        self.showMaximized()
        self.setFixedSize(self.size())

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

        for widget in [
            label_type,
            self.combo_type,
            self.label_count,
            self.combo_count,
            btn_generate,
        ]:
            sidebar_layout.addWidget(widget)
            sidebar_layout.addSpacing(10)

        sidebar_frame.setStyleSheet(
            """
            QFrame {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                                  stop:0 #34495e, stop:1 #2c3e50);
            }
            QLabel {
                font-family: "Pixel Game";
                font-size: 24px;
                color: #f0f0f0;
                font-weight: bold;
            }
            QComboBox {
                font-family: "Pixel Game";
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
                font-family: "Pixel Game";
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

    def update_count_options(self):
        self.combo_count.clear()
        board_type = self.combo_type.currentText()
        if board_type == "4 Core":
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

    def eventFilter(self, source, event):
        if source is self.view.viewport() and event.type() == QEvent.Resize:
            QTimer.singleShot(50, self._do_layout)
        return super().eventFilter(source, event)

    def closeEvent(self, event):
        from view.main_window import MainLauncherWindow

        self.launcher = MainLauncherWindow()
        self.launcher.show()
        event.accept()
