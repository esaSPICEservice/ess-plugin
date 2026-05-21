from PyQt5.QtWidgets import (
    QDialog, QPushButton, QGridLayout, QDoubleSpinBox,
    QHBoxLayout, QVBoxLayout, QLabel
)
from PyQt5.QtCore import Qt
from utils.frame_generator import SwiFrameGenerator
from actions.sensors import toggle_sensor
from actions.time_navigation import sensor_view, spacecraft_view

class SwiPointerDialog(QDialog):
    sc = SwiFrameGenerator()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.at = 0
        self.ct = 0
        self.delta = 1

        self.setWindowTitle("SWI Pointer")

         # Buttons
        self.at_up_btn = QPushButton("⬅️")  # Pitch up
        self.at_down_btn = QPushButton("➡️")  # Pitch down
        self.ct_up_btn = QPushButton("⬆️")  # Yaw left
        self.ct_down_btn = QPushButton("⬇️")  # Yaw right
        self.reset_btn = QPushButton("✖️")  # Reset
        self.sc_view = QPushButton("🚀")
        self.zoom_view = QPushButton("🔎")

        for btn in (
            self.ct_up_btn,
            self.ct_down_btn,
            self.at_up_btn,
            self.at_down_btn,
            self.reset_btn,
            self.sc_view,
            self.zoom_view
        ):
            btn.setFixedSize(70, 40)


        # Delta input
        self.delta_angle = QDoubleSpinBox()
        self.delta_angle.setRange(-180, 180)
        self.delta_angle.setDecimals(3)
        self.delta_angle.setSingleStep(0.1)
        self.delta_angle.setValue(self.delta)

        self.delta_angle.valueChanged.connect(self.on_delta_changed)

        # ---- Status label ----
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignLeft)

        # ---- AT/CT inputs ----
        self.at_input = QDoubleSpinBox()
        self.at_input.setRange(-180, 180)
        self.at_input.setDecimals(3)
        self.at_input.setValue(self.at)

        self.ct_input = QDoubleSpinBox()
        self.ct_input.setRange(-180, 180)
        self.ct_input.setDecimals(3)
        self.ct_input.setValue(self.ct)

        self.apply_btn = QPushButton("Apply")
        self.apply_btn.setFixedSize(100, 40)

        self.set_triggers()
        self.set_layout()
        self.set_status_label()


        
    def set_triggers(self):
        
        self.at_up_btn.clicked.connect(self.on_at_down)
        self.at_down_btn.clicked.connect(self.on_at_up)
        self.ct_up_btn.clicked.connect(self.on_ct_down)
        self.ct_down_btn.clicked.connect(self.on_ct_up)
        self.reset_btn.clicked.connect(self.on_reset)
        self.sc_view.clicked.connect(self.on_sc_view)
        self.zoom_view.clicked.connect(self.on_zoom_view)
        self.apply_btn.clicked.connect(self.on_apply_manual)


    def set_layout(self):
        # --- Direction buttons ---
        for btn in (
            self.ct_up_btn,
            self.ct_down_btn,
            self.at_up_btn,
            self.at_down_btn,
            self.reset_btn,
        ):
            btn.setFixedSize(70, 40)

        self.sc_view.setFixedSize(70, 36)
        self.zoom_view.setFixedSize(70, 36)

        buttons_layout = QGridLayout()
        buttons_layout.setSpacing(6)

        buttons_layout.addWidget(self.ct_up_btn, 0, 1)
        buttons_layout.addWidget(self.at_up_btn, 1, 0)
        buttons_layout.addWidget(self.reset_btn, 1, 1)
        buttons_layout.addWidget(self.at_down_btn, 1, 2)
        buttons_layout.addWidget(self.ct_down_btn, 2, 1)

        controls_wrapper = QHBoxLayout()
        controls_wrapper.addStretch()
        controls_wrapper.addLayout(buttons_layout)
        controls_wrapper.addStretch()

        

        # --- Delta ---
        delta_layout = QHBoxLayout()
        delta_layout.addWidget(QLabel("Delta step:"))
        delta_layout.addWidget(self.delta_angle)
        delta_layout.addStretch()

        # --- View buttons ---
        view_layout = QHBoxLayout()
        view_layout.addWidget(self.sc_view)
        view_layout.addStretch()
        view_layout.addWidget(self.zoom_view)

        # --- Manual controls ---
        manual_layout = QHBoxLayout()
        manual_layout.addWidget(QLabel("AT"))
        manual_layout.addWidget(self.at_input)
        manual_layout.addSpacing(12)
        manual_layout.addWidget(QLabel("CT"))
        manual_layout.addWidget(self.ct_input)
        manual_layout.addSpacing(20)
        manual_layout.addWidget(self.apply_btn)
        manual_layout.addStretch()

        # --- Status ---
        self.status_label.setStyleSheet("""
            QLabel {
                font-weight: bold;
                padding-top: 6px;
            }
        """)

        # --- Main layout ---
        main_layout = QVBoxLayout()
        main_layout.setSpacing(12)
        main_layout.setContentsMargins(12, 12, 12, 12)

        main_layout.addLayout(view_layout)
        main_layout.addLayout(controls_wrapper)
        main_layout.addLayout(delta_layout)
        main_layout.addLayout(manual_layout)
        main_layout.addWidget(self.status_label)
        self.setLayout(main_layout)


    def on_at_up(self):
        self.update(self.delta, 0)

    def on_at_down(self):
        self.update(-self.delta, 0)

    def on_ct_down(self):
        self.update(0, self.delta)

    def on_ct_up(self):
        self.update(0, -self.delta)

    def on_reset(self):
        self.at = 0
        self.ct = 0
        self.update(0, 0)

    def on_sc_view(self):
        spacecraft_view()

    def on_zoom_view(self):
        sensor_view('JUICE_SWI_CH1P', 10)

    def on_delta_changed(self, value: float):
        self.delta = value

    def update(self, delta_pitch, delta_yaw):
        self.at += delta_pitch
        self.ct += delta_yaw
        self.set_status_label()
        self.sc.update([self.ct, self.at, 0])
        self.at_input.setValue(- self.at)
        self.ct_input.setValue(- self.ct)


    def on_apply_manual(self):
        self.at = - self.at_input.value()
        self.ct = - self.ct_input.value()
        self.set_status_label()
        self.sc.update([self.ct, self.at, 0])

    def set_status_label(self):
        label = "AT: {:.2f} (deg) | CT: {:.2f} (deg)".format(
            -self.at, -self.ct
        )
        self.status_label.setText(label)


    def show_and_focus(self):
        self.hide()

        toggle_sensor(True,'JUICE_SWI_FULL')
        toggle_sensor(True,'JUICE_SWI_CH1P')
        toggle_sensor(True, 'JUICE_SWI_CH2P')
        toggle_sensor(True,'JUICE_SWI_CH1')
        toggle_sensor(True, 'JUICE_SWI_CH2')

        self.show()


# TODO
# - Add two input text boxes for pitch and yaw
# - The yaw is scaled by the cosine of the pitch
