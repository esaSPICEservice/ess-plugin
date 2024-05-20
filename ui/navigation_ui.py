
from PyQt5.QtWidgets import QDialog
from actions.sensors import get_sensors, toggle_sensor, get_boresights
from ui.design.navigation_panel import Ui_Form
from actions.time_navigation import spacecraft_view, sensor_view
from ui.tabbed_selector import TabbedSelector


class NavigationDialog(QDialog):

    id = 'navigation_dialog_window_id'

    def __init__(self, main_window):
        QDialog.__init__(self, main_window)
        self.boresights = get_boresights()
        self.init_ui()
        

    def init_ui(self):
        self.setObjectName(NavigationDialog.id)
        self.navigation_panel = Ui_Form()
        self.navigation_panel.setupUi(self)
        self.navigation_panel.scViewButton.clicked.connect(spacecraft_view)
        self.navigation_panel.sensorViewButton.clicked.connect(self.sensor_view)

        self.tabSelector = TabbedSelector(self, get_sensors(), toggle_sensor)
        self.navigation_panel.verticalLayout.addWidget(self.tabSelector)

        sensor_list = list(map(lambda item: item.get('name'), self.boresights))
        self.navigation_panel.sensorBox.addItems(sensor_list)

    def sensor_view(self):
        sensor_name = self.navigation_panel.sensorBox.currentText()
        sensor = next(filter(lambda item: item.get('name') == sensor_name, self.boresights))
        sensor_view(sensor.get('fov_frame'), sensor.get('size'))

    def show_and_focus(self):
        self.hide()
        self.show()


