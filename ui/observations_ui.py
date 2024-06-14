
from PyQt5.QtWidgets import QFileDialog, QDialog, QTableWidgetItem, QMessageBox
from PyQt5.QtCore import Qt, QDateTime
from actions.sensors import get_sensor_ids, get_targets, reconfigure_catalogue
from ui.common import get_settings, get_runtime
from ui.design.observations_panel import Ui_observationsPanel
import os


class ObservationsDialog(QDialog):

    id = 'observations_dialog_window_id'

    def __init__(self, main_window):
        QDialog.__init__(self, main_window)
        self.run_time = get_runtime()
        self.init_ui()

    def init_ui(self):
        self.setObjectName(ObservationsDialog.id)
        self.panel = Ui_observationsPanel()
        self.panel.setupUi(self)
        self.panel.newButton.clicked.connect(self._add_row)
        self.panel.removeButton.clicked.connect(self._remove_row)
        self.panel.browseButton.clicked.connect(self._browse)
        self.panel.importButton.clicked.connect(self._import)
        self.panel.addButton.clicked.connect(self.__add_observations)
        self.panel.sensorComboBox.addItems(get_sensor_ids())
        self.panel.targetComboBox.addItems(get_targets())
        self.table = self.panel.tableWidget

    def _add_row(self):
      
        sensor = self.panel.sensorComboBox.currentText()
        target = self.panel.targetComboBox.currentText()
        start = self.panel.startDateTimeEdit.dateTime().toUTC().toString(Qt.ISODate)
        end = self.panel.endDateTimeEdit.dateTime().toUTC().toString(Qt.ISODate)
        self.__add_row_content(sensor, target, start, end)

    def __add_row_content(self, sensor, target, start, end):
        row_count = self.table.rowCount()
        self.table.insertRow(row_count)
        self.table.setItem(row_count , 0, QTableWidgetItem(sensor))
        self.table.setItem(row_count , 1, QTableWidgetItem(target))
        self.table.setItem(row_count , 2, QTableWidgetItem(start))
        self.table.setItem(row_count , 3, QTableWidgetItem(end))

    def _remove_row(self):
        if self.table.rowCount() > 0:
            self.table.removeRow(self.table.rowCount()-1)

    def _browse(self):
        # default_folder = self.settings.get(self.mission, last_repo_key, '')
        default_folder = ''
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Select CSV", default_folder, "CSV files (*.csv)")
        if file_name:
            self.panel.importLineEdit.setText(file_name)
        self.focus()
    
    def _import(self):
        csv_path = self.panel.importLineEdit.text()

        if not csv_path or not os.path.exists(csv_path):
            QMessageBox.warning(self, 'Observations', 'CSV file is mandatory')
            return
        
        with open(csv_path, 'r') as csv_file:
            lines = csv_file.readlines()
            for line in lines:
                fields = line.split(',')
                if len(fields) == 4:
                    self.__add_row_content(fields[0], fields[1], fields[2], fields[3])


    def _get_observations(self):
        row_count = self.table.rowCount()
        column_count = self.table.columnCount()
        observations = []
        for row in range(row_count):
            observation = []
            for column in range(column_count):
                observation.append(self.table.item(row, column).text())
            observations.append(observation)
        return observations
    
    def __add_observations(self):
        observations = self._get_observations()
        if len(observations) > 0:
            self.run_time.set('observations', observations)
            reconfigure_catalogue()
            self.hide()

    def show_and_focus(self):
        self.focus()

    def focus(self):
        self.hide()
        self.show()
