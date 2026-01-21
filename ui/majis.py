import sys
from PyQt5.QtWidgets import (
    QDialog, QPushButton, QGridLayout, QDoubleSpinBox,
    QHBoxLayout, QVBoxLayout, QLabel
)
from PyQt5.QtCore import Qt
from utils.frame_generator import MajisFrameGenerator
from actions.sensors import toggle_sensor

class MajisPointerDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.x_angle = 0
        self.y_angle = 0
        self.delta = 1
 
        self.setWindowTitle("MAJIS Pointer")

         # Buttons
        self.up_btn = QPushButton("Up")
        self.down_btn = QPushButton("Down")
        self.left_btn = QPushButton("Left")
        self.right_btn = QPushButton("Right")
        self.center_btn = QPushButton("Center")

        for btn in (
            self.up_btn,
            self.down_btn,
            self.left_btn,
            self.right_btn,
            self.center_btn,
        ):
            btn.setFixedSize(80, 40)

        # Cross layout
        cross_layout = QGridLayout()
        cross_layout.addWidget(self.up_btn, 0, 1)
        cross_layout.addWidget(self.left_btn, 1, 0)
        cross_layout.addWidget(self.center_btn, 1, 1)
        cross_layout.addWidget(self.right_btn, 1, 2)
        cross_layout.addWidget(self.down_btn, 2, 1)

        # Delta input
        delta_label = QLabel("Delta (deg):")
        self.delta_spin = QDoubleSpinBox()
        self.delta_spin.setRange(-1e6, 1e6)
        self.delta_spin.setDecimals(4)
        self.delta_spin.setSingleStep(0.1)
        self.delta_spin.setValue(self.delta)

        self.delta_spin.valueChanged.connect(self.on_delta_changed)

        delta_layout = QHBoxLayout()
        delta_layout.addWidget(delta_label)
        delta_layout.addWidget(self.delta_spin)
        delta_layout.addStretch()

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.addLayout(cross_layout)
        main_layout.addLayout(delta_layout)


        self.up_btn.clicked.connect(self.on_up)
        self.down_btn.clicked.connect(self.on_down)
        self.left_btn.clicked.connect(self.on_left)
        self.right_btn.clicked.connect(self.on_right)
        self.center_btn.clicked.connect(self.on_center)

        # ---- Status label at the end ----
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignLeft)
        main_layout.addWidget(self.status_label)

        self.setLayout(main_layout)

    def on_up(self):
        self.update(0, self.delta)

    def on_down(self):
        self.update(0, -self.delta)

    def on_left(self):
        self.update(-self.delta, 0)

    def on_right(self):
        self.update(self.delta, 0)

    def on_center(self):
        self.x_angle = 0
        self.y_angle = 0
        self.update(0, 0)

    def on_delta_changed(self, value: float):
        self.delta = value

    def update(self, delta_x, delta_y):
        toggle_sensor(True,'JUICE_MAJIS_POINTER')
        self.x_angle += delta_x
        self.y_angle += delta_y
        label = "X: {:.2f} (deg) Y: {:.2f} (deg)".format(self.x_angle, self.y_angle)
        self.status_label.setText(label)
        mj = MajisFrameGenerator()
        mj.update([self.x_angle, self.y_angle, 0])

    def show_and_focus(self):
        self.hide()
        self.show()