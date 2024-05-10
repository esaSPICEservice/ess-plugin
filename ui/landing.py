from PyQt5.QtWidgets import QDialog
from actions.sensors import get_sensors, toggle_sensor, get_sensor_list
from ui.design.landing import Ui_landingWidget
from actions.time_navigation import spacecraft_view, sensor_view


class LandingDialog(QDialog):

    id = 'landing_dialog_window_id'

    def __init__(self, main_window):
        QDialog.__init__(self, main_window)
        self.init_ui()

    def init_ui(self):
        self.setObjectName(LandingDialog.id)
        self.navigation_panel = Ui_landingWidget()
        self.navigation_panel.setupUi(self)
        self.navigation_panel.selectButton.clicked.connect(self.create_ui)
        
    def create_ui(self):
        mission = self.navigation_panel.comboBox.currentText()
        self.callback(mission.lower() + '.json')
        self.hide()

    def show_and_focus(self, callback):
        self.callback = callback
        self.hide()
        self.show()