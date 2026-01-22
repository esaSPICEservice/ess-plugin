import sys
from PyQt5.QtWidgets import (
    QDialog, QPushButton, QGridLayout, QDoubleSpinBox,
    QHBoxLayout, QVBoxLayout, QLabel
)
from PyQt5.QtCore import Qt
from utils.frame_generator import MajisFrameGenerator
from ui.common import get_runtime
from actions.sensors import toggle_sensor, reconfigure_catalogue
from actions.time_navigation import sensor_view

class MajisPointerDialog(QDialog):
    mj = MajisFrameGenerator()
    SLIT_STEPS = 0.008_594  # degrees

    def __init__(self, parent=None):
        super().__init__(parent)

        self.slit_offset = 0
        self.delta = 128

        self.setWindowTitle("MAJIS Scanner")

         # Buttons
        self.up_btn = QPushButton("⬆️ Slit up")
        self.down_btn = QPushButton("⬇️ Slit down")
        self.reset_btn = QPushButton("✖️ Reset")

        for btn in (
            self.up_btn,
            self.down_btn,
            self.reset_btn,
        ):
            btn.setFixedSize(300, 40)

        # Cross layout
        arrows_layout = QVBoxLayout()
        arrows_layout.addWidget(self.up_btn)
        arrows_layout.addWidget(self.reset_btn)
        arrows_layout.addWidget(self.down_btn)

        # Delta input
        delta_label = QLabel("Slits offset:")
        self.delta_spin = QDoubleSpinBox()
        self.delta_spin.setRange(0, 1e3)
        self.delta_spin.setDecimals(0)
        self.delta_spin.setSingleStep(1)
        self.delta_spin.setValue(self.delta)

        self.delta_spin.valueChanged.connect(self.on_delta_changed)

        delta_layout = QHBoxLayout()
        delta_layout.addWidget(delta_label)
        delta_layout.addWidget(self.delta_spin)
        delta_layout.addStretch()

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.addLayout(arrows_layout)
        main_layout.addLayout(delta_layout)

        self.up_btn.clicked.connect(self.on_up)
        self.down_btn.clicked.connect(self.on_down)
        self.reset_btn.clicked.connect(self.on_reset)

        # ---- Status label at the end ----
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignLeft)
        main_layout.addWidget(self.status_label)

        self.setLayout(main_layout)

    def on_up(self):
        self.update(self.delta)

    def on_down(self):
        self.update(-self.delta)

    def on_reset(self):
        self.slit_offset = 0
        self.update(0)

    def on_delta_changed(self, value: float):
        self.delta = value

    def update(self, delta_y):
        self.slit_offset += delta_y
        label = "ΔSlits: {:.0f} | Scan angle: {:.2f}° | Mirror position: {:.2f}°".format(
            self.slit_offset,
            self.slit_offset * self.SLIT_STEPS,
            self.slit_offset * self.SLIT_STEPS / 2,
        )
        self.status_label.setText(label)
        self.mj.update([self.slit_offset * self.SLIT_STEPS, 0, 0])

    def show_and_focus(self):
        self.hide()

        toggle_sensor(True,'JUICE_JANUS')
        toggle_sensor(True,'JUICE_MAJIS_EXTENDED')
        toggle_sensor(True, 'JUICE_MAJIS_VISNIR')

        sensor_view('JUICE_MAJIS_EXTENDED', 8.5)
        self.show()
