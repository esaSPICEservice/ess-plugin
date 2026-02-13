from PyQt5.QtWidgets import (
    QDialog, QPushButton, QGridLayout, QDoubleSpinBox,
    QHBoxLayout, QVBoxLayout, QLabel
)
from PyQt5.QtCore import Qt
from utils.frame_generator import SwiFrameGenerator
from actions.sensors import toggle_sensor
from actions.time_navigation import sensor_view

class SwiPointerDialog(QDialog):
    sc = SwiFrameGenerator()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.pitch = 0
        self.yaw = 0
        self.delta = 1

        self.setWindowTitle("SWI Pointer")

         # Buttons
        self.pitch_up_btn = QPushButton("⬆️")  # Pitch up
        self.pitch_down_btn = QPushButton("⬇️")  # Pitch down
        self.yaw_left_btn = QPushButton("⬅️")  # Yaw left
        self.yaw_right_btn = QPushButton("➡️")  # Yaw right
        self.reset_btn = QPushButton("✖️")  # Reset

        for btn in (
            self.pitch_up_btn,
            self.pitch_down_btn,
            self.yaw_left_btn,
            self.yaw_right_btn,
            self.reset_btn,
        ):
            btn.setFixedSize(150, 40)

        # Cross layout
        buttons_layout = QGridLayout()
        buttons_layout.addWidget(self.pitch_up_btn, 0, 1)
        buttons_layout.addWidget(self.pitch_down_btn, 2, 1)
        buttons_layout.addWidget(self.yaw_left_btn, 1, 0)
        buttons_layout.addWidget(self.yaw_right_btn, 1, 2)
        buttons_layout.addWidget(self.reset_btn, 1, 1)


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


    def on_pitch_up(self):
        self.update(self.delta, 0)

    def on_pitch_down(self):
        self.update(-self.delta, 0)

    def on_yaw_left(self):
        self.update(0, -self.delta)

    def on_yaw_right(self):
        self.update(0, self.delta)

    def on_reset(self):
        self.pitch = 0
        self.yaw = 0
        self.update(0, 0)

    def on_delta_changed(self, value: float):
        self.delta = value

    def update(self, delta_pitch, delta_yaw):
        self.pitch += delta_pitch
        self.yaw += delta_yaw
        label = "Pitch (ΔY): {:.2f} (deg) | Yaw (ΔX): {:.2f} (deg)".format(self.pitch, self.yaw)
        self.status_label.setText(label)

        self.sc.update([self.yaw, self.pitch, 0])

    def show_and_focus(self):
        self.hide()

        toggle_sensor(True,'JUICE_SWI_FULL')
        toggle_sensor(True,'JUICE_SWI_CH1P')
        toggle_sensor(True, 'JUICE_SWI_CH2P')

        sensor_view('JUICE_SWI_CH1P', 10)

        self.show()


# TODO
# - Add two input text boxes for pitch and yaw
# - The yaw is scaled by the cosine of the pitch
