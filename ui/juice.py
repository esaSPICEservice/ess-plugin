import sys
from PyQt5.QtWidgets import (
    QDialog, QPushButton, QGridLayout, QDoubleSpinBox,
    QHBoxLayout, QVBoxLayout, QLabel
)
from PyQt5.QtCore import Qt
from utils.frame_generator import SpacecraftFrameGenerator
from ui.common import get_runtime
from actions.sensors import toggle_sensor, reconfigure_catalogue
from actions.time_navigation import sensor_view

class SpacecraftPointerDialog(QDialog):
    sc = SpacecraftFrameGenerator()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.roll = 0
        self.pitch = 0
        self.yaw = 0
        self.delta = 1

        self.setWindowTitle("Spacecraft Pointer")

         # Buttons
        self.roll_clock_btn = QPushButton("⃕")  #  Roll clock
        self.roll_counterclock_btn = QPushButton("⃔")  # Roll counterclock
        self.pitch_up_btn = QPushButton("⬆️")  # Pitch up
        self.pitch_down_btn = QPushButton("⬇️")  # Pitch down
        self.yaw_left_btn = QPushButton("⬅️")  # Yaw left
        self.yaw_right_btn = QPushButton("➡️")  # Yaw right
        self.reset_btn = QPushButton("✖️")  # Reset

        for btn in (
            self.roll_clock_btn,
            self.roll_counterclock_btn,
            self.pitch_up_btn,
            self.pitch_down_btn,
            self.yaw_left_btn,
            self.yaw_right_btn,
            self.reset_btn,
        ):
            btn.setFixedSize(150, 40)

        # Cross layout
        buttons_layout = QGridLayout()
        buttons_layout.addWidget(self.roll_clock_btn, 0, 0)
        buttons_layout.addWidget(self.roll_counterclock_btn, 0, 1)
        buttons_layout.addWidget(self.pitch_up_btn, 1, 0)
        buttons_layout.addWidget(self.pitch_down_btn, 1, 1)
        buttons_layout.addWidget(self.yaw_left_btn, 2, 0)
        buttons_layout.addWidget(self.yaw_right_btn, 2, 1)
        buttons_layout.addWidget(self.reset_btn, 3, 0)

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

        self.roll_clock_btn.clicked.connect(self.on_roll_clock)
        self.roll_counterclock_btn.clicked.connect(self.on_roll_counterclock)
        self.pitch_up_btn.clicked.connect(self.on_pitch_up)
        self.pitch_down_btn.clicked.connect(self.on_pitch_down)
        self.yaw_left_btn.clicked.connect(self.on_yaw_left)
        self.yaw_right_btn.clicked.connect(self.on_yaw_right)
        self.reset_btn.clicked.connect(self.on_reset)

        # ---- Status label at the end ----
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignLeft)
        main_layout.addWidget(self.status_label)

        self.setLayout(main_layout)


    def on_roll_clock(self):
        self.update(0, 0, self.delta)

    def on_roll_counterclock(self):
        self.update(0, 0, -self.delta)

    def on_pitch_up(self):
        self.update(0, self.delta, 0)

    def on_pitch_down(self):
        self.update(0, -self.delta, 0)

    def on_yaw_left(self):
        self.update(-self.delta, 0, 0)

    def on_yaw_right(self):
        self.update(self.delta, 0, 0)

    def on_reset(self):
        self.roll = 0
        self.pitch = 0
        self.yaw = 0
        self.update(0, 0, 0)

    def on_delta_changed(self, value: float):
        self.delta = value

    def update(self, delta_roll, delta_pitch, delta_yaw):
        self.roll += delta_roll
        self.pitch += delta_pitch
        self.yaw += delta_yaw
        label = "Roll (Z): {:.2f} (deg) | Pitch (ΔY): {:.2f} (deg) | Yaw (ΔX): {:.2f} (deg)".format(self.roll, self.pitch, self.yaw)
        self.status_label.setText(label)

        self.sc.update([self.yaw, self.pitch, self.roll])

    def show_and_focus(self):
        self.hide()

        toggle_sensor(True,'JUICE_JANUS')
        toggle_sensor(True,'JUICE_MAJIS_EXTENDED')
        toggle_sensor(True, 'JUICE_MAJIS_VISNIR')
        toggle_sensor(True, 'JUICE_UVS_AP_HP')

        sensor_view('JUICE_MAJIS_EXTENDED', 8.5)
        self.show()
