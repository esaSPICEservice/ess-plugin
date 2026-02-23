from PyQt5.QtWidgets import (
    QDialog, QPushButton, QGridLayout, QDoubleSpinBox,
    QHBoxLayout, QVBoxLayout, QLabel
)
from PyQt5.QtCore import Qt
from utils.frame_generator import PhebusFrameGenerator
from actions.sensors import toggle_sensor
from actions.time_navigation import sensor_view

class PhebusPointerDialog(QDialog):
    sc = PhebusFrameGenerator()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.s = None
        self.delta = 1

        self.setWindowTitle("Phebus Pointer")

         # Buttons

        self.s_left_btn = QPushButton("⬅️")  # Yaw left
        self.s_right_btn = QPushButton("➡️")  # Yaw right
        self.reset_btn = QPushButton("✖️")  # Reset
        self.look_btn = QPushButton("🔎")

        for btn in (
            self.s_left_btn,
            self.s_right_btn,
            self.reset_btn,
        ):
            btn.setFixedSize(150, 40)

        # Cross layout
        buttons_layout = QGridLayout()
        buttons_layout.addWidget(self.s_left_btn, 1, 0)
        buttons_layout.addWidget(self.s_right_btn, 1, 2)
        buttons_layout.addWidget(self.reset_btn, 1, 1)
        buttons_layout.addWidget(self.look_btn, 2, 1)


        # Delta input
        delta_label = QLabel("Delta steps (deg):")
        self.delta_angle = QDoubleSpinBox()
        self.delta_angle.setRange(-1e2, 1e2)
        self.delta_angle.setDecimals(2)
        self.delta_angle.setSingleStep(0.1)
        self.delta_angle.setValue(self.delta)

        self.delta_angle.valueChanged.connect(self.on_delta_changed)

        delta_layout = QHBoxLayout()
        delta_layout.addWidget(delta_label)
        delta_layout.addWidget(self.delta_angle)
        delta_layout.addStretch()

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.addLayout(buttons_layout)
        main_layout.addLayout(delta_layout)

        self.s_left_btn.clicked.connect(self.on_s_left)
        self.s_right_btn.clicked.connect(self.on_s_right)
        self.reset_btn.clicked.connect(self.on_reset)
        self.look_btn.clicked.connect(self.look_through)

        # ---- Status label at the end ----
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignLeft)
        main_layout.addWidget(self.status_label)

        self.setLayout(main_layout)


    def on_s_left(self):
        self.update(-self.delta)

    def on_s_right(self):
        self.update(self.delta)

    def on_reset(self):
        self.s = 0
        self.update(0)

    def on_delta_changed(self, value: float):
        self.delta = value

    def update(self, delta_s):
        self.s += delta_s
        label = "Phebus S angle: {:.2f} (deg)".format(self.s)
        self.status_label.setText(label)
        self.sc.update(self.sc.phebus_to_euler(self.s))

    def look_through(self):
        sensor_view('MPO_PHEBUS_SLIT_75_P', 3)

    def show_and_focus(self):
        self.hide()
        toggle_sensor(True,'MPO_PHEBUS_SLIT_75_P')
        self.show()
        if self.s is None:
            self.s = 0
            self.update(0)


# TODO
# - Add two input text boxes for pitch and yaw
# - The yaw is scaled by the cosine of the pitch
