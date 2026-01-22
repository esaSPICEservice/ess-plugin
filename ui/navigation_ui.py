
from PyQt5.QtWidgets import QDialog, QPushButton, QWidget
from PyQt5 import QtCore
from actions.sensors import get_sensor_names, toggle_sensor, get_boresights, reconfigure_catalogue
from ui.common import get_runtime
from ui.design.navigation_panel import Ui_Form
from ui.design.time_panel import Ui_Form as TimePanel
from actions.time_navigation import faster2x, slower2x, reverseTime, unpause, pause, sensor_view, goto_spacecraft, get_cosmo_time
from ui.tabbed_selector import TabbedSelector
from PyQt5.QtCore import QTimer

class NavigationDialog(QDialog):

    id = 'navigation_dialog_window_id'

    def __init__(self, main_window):
        QDialog.__init__(self, main_window, QtCore.Qt.WindowStaysOnTopHint)
        self.boresights = get_boresights()
        self.run_time = get_runtime()
        self.init_ui()
        self.timer0 = QTimer()
        self.timer0.setInterval(200)
        self.timer0.timeout.connect(self.set_cosmographia_time)
        self.timer0.start()

    def init_ui(self):
        self.setObjectName(NavigationDialog.id)
        self.navigation_panel = Ui_Form()
        self.navigation_panel.setupUi(self)
        self.navigation_panel.sensorViewButton.clicked.connect(self.sensor_view)
        self.frustrumCheckbox = self.navigation_panel.frustrumCheckbox
        self.frustrumCheckbox.setChecked(False)
        self.frustrumCheckbox.stateChanged.connect(self.frustrumChange)
        self.spacecrafts_tab()
        self.tabSelector = TabbedSelector(self, get_sensor_names(), self.toggle_sensor)
        self.navigation_panel.verticalLayout.addWidget(self.tabSelector)

        sensor_list = list(map(lambda item: item.get('name'), self.boresights))
        self.navigation_panel.sensorBox.addItems(sensor_list)

        timeControlWidget = QWidget(self)
        self.timeControl = TimePanel()
        self.timeControl.setupUi(timeControlWidget)
        self.setup_time_control()
        self.navigation_panel.verticalLayout.addWidget(timeControlWidget)

    def spacecrafts_tab(self):
        spacecrafts = self.run_time.get("spacecrafts", [])
        for spacecraft in spacecrafts:
            button = QPushButton(self)
            name = spacecraft.get("spacecraft")
            frame = spacecraft.get("spacecraft_frame")
            initial_offset = spacecraft.get("initial_offset", [0, 2e-3, -22e-3])
            button.setText(name)
            button.clicked.connect(lambda _, name=name, frame=frame, initial_offset=initial_offset: goto_spacecraft(name, frame, initial_offset))
            self.navigation_panel.spacecraftsBar.addWidget(button)

    def sensor_view(self):
        sensor_name = self.navigation_panel.sensorBox.currentText()
        sensor = next(filter(lambda item: item.get('name') == sensor_name, self.boresights))
        sensor_view(sensor.get('name'), sensor.get('size'))

    def toggle_sensor(self, visible, name):
        toggle_sensor(visible, name)
        # We invoke during init state, this guard prevents from storing the state
        # too early
        if hasattr(self, 'tabSelector'):
            self.run_time.set('sensors_state', self.tabSelector.get_state())

    def frustrumChange(self):
        self.run_time.set('sensors_frustrum', self.frustrumCheckbox.isChecked())
        reconfigure_catalogue()

    def show_and_focus(self):
        self.run_time.set('sensors_state', self.tabSelector.get_state())
        self.hide()
        self.show()

    def setup_time_control(self):
        self.timeControl.rewind.clicked.connect(slower2x)
        self.timeControl.forward.clicked.connect(faster2x)
        self.timeControl.direction.clicked.connect(reverseTime)
        self.timeControl.play.clicked.connect(unpause)
        self.timeControl.pause.clicked.connect(pause)

    def set_cosmographia_time(self):
        date_str = get_cosmo_time()
        if self.timeControl:
            self.timeControl.timeDisplay.setText(date_str[:19] + ' UTC')
