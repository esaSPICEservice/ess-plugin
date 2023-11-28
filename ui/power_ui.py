import csv
from ui.design.power_panel import Ui_Form
from PyQt5.QtWidgets import QDialog, QDialog


from ui.charts.qcharts import (LineChart,  DataTable, Viewer)


class LineChartPanel(Viewer):

    def __init__(self, power_file_path):
        super().__init__()
        self.power_file_path = power_file_path
        self.init_ui()

    def init_ui(self):
        table = DataTable()
        table.add_column('Time')
        table.add_column('Act')
        table.add_column('Ref')
        try:
            vmax = None
            vmin = None
            with open(self.power_file_path, 'r') as power_file:
                reader = csv.reader(filter(lambda row: row[0]!='#', power_file))
                for index, row in enumerate(reader):
                    actual = float(row[1])
                    ck = float(row[2])
                    table.add_row([index, actual, ck])
                    vmax = max(actual, ck) if vmax is None else max(actual, ck, vmax)
                    vmin = min(actual, ck) if vmin is None else min(actual, ck, vmin)

            chart = LineChart(table)
            chart.set_horizontal_axis_column(0)
            chart.haxis_title = 'Time'
            chart.haxis_step = int(index / 5)
            chart.vaxis_step = int ((vmax - vmin) / 5)
            chart.vaxis_vmin = vmin - chart.vaxis_step 
            chart.vaxis_vmax = vmax + chart.vaxis_step 
            self.set_graph(chart)
        except Exception as error:
            print(error)

       

class PowerDialog(QDialog):

    id = 'power_dialog_window_id'

    def __init__(self, main_window, power_file_path):
        QDialog.__init__(self, main_window)
        self.power_file_path = power_file_path
        self.init_ui()

    def init_ui(self):
        self.setObjectName(PowerDialog.id)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        viewer = LineChartPanel(self.power_file_path)
        self.ui.verticalLayout.addWidget(viewer)

    def show_and_focus(self):
        self.hide()
        self.show()