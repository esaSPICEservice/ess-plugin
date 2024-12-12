
import datetime
from ui.design.block_panel import Ui_Form
from PyQt5.QtWidgets import QDialog, QTableWidgetItem, QTableWidget, QTableWidgetSelectionRange, QVBoxLayout
import cosmoscripting
from PyQt5.QtCore import QTimer
from ui.timeline.timeline import Timeline, TimelineBlock

from simulator.osve.utils import get_platform
my_platform = get_platform()
if (my_platform.startswith("linux")):
    from utils.re_block_parser import BlockParser
    print('Regular Expression Parser')
else:
    from utils.block_parser import BlockParser

from actions.time_navigation import goto_date
from utils.time import duration

class DateTableWidgetItem(QTableWidgetItem):
    
    def __init__(self, date_str, callback):
        QTableWidgetItem.__init__(self, date_str)
        self.date_str = date_str
        self.callback = callback

    def doEdit(self):
        self.callback(self.date_str)

class BlockTableWidgetItem(QTableWidgetItem):
    
    def __init__(self, block_str):
        QTableWidgetItem.__init__(self, block_str)

    def doEdit(self):
        pass


EPOCH_2000 = datetime.datetime(2000, 1, 1, 12, 0, tzinfo=datetime.timezone.utc).timestamp()

class BlocksDialog(QDialog):

    id = 'blocks_dialog_window_id'

    def __init__(self, main_window, ptr_path):
        QDialog.__init__(self, main_window)
        self.ptr_path = ptr_path
        self.init_ui()
        self.cosmo = cosmoscripting.Cosmo()
        self.timer0 = QTimer()
        self.timer0.setInterval(200)
        self.timer0.timeout.connect(self.set_cosmographia_time)
        self.timer0.start()

    def init_ui(self):
        self.setObjectName(BlocksDialog.id)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        timelineLayout = QVBoxLayout()
        self.ui.timelineWidget.setLayout(timelineLayout)
        self.timeline = Timeline(self, self.goto_date_timeline)
        timelineLayout.addWidget(self.timeline)
        self.block_timeline_index = []
        try:
            with open(self.ptr_path, 'r') as ptr_file:
                ptr_content = ptr_file.read()
            parser = BlockParser(ptr_content)
            parser.process()

            self.ui.tableWidget.setEditTriggers( QTableWidget.NoEditTriggers )

            self.ui.tableWidget.verticalHeader().sectionClicked.connect(self.show_block_index)

            # create a connection to the double click event
            self.ui.tableWidget.itemDoubleClicked.connect(self.edit_item)
            self.ui.tableWidget.clicked.connect(self.show_block)
            self.block_contents = {}
            row_number = 0
            print('*********************')
            print(parser.start_times)
            print('*********************')
            for index, start_time in enumerate(parser.start_times):
                if start_time:
                    end_time = parser.end_times[index]
                    self.timeline.add_block(TimelineBlock(start_time, end_time, 'OBS'))
                else:
                    start_time = parser.end_times[index-1]
                    end_time = parser.start_times[index+1]

                self.ui.tableWidget.insertRow(row_number)
                self.ui.tableWidget.setItem(
                    row_number, 0, 
                    DateTableWidgetItem(start_time, self.goto_date_cosmographia))
                self.ui.tableWidget.setItem(
                    row_number, 1, 
                    DateTableWidgetItem(end_time, self.goto_date_cosmographia))
                self.ui.tableWidget.setItem(
                    row_number, 2, 
                    BlockTableWidgetItem(str(duration(start_time, end_time))))
                self.block_contents[row_number] = parser.block_contents[index]
                self.block_timeline_index.append((row_number,start_time, end_time))
                row_number +=1

        except Exception as error:
            print(error)

    def set_cosmographia_time(self):
        time = self.cosmo.getTime()
        delta = (32.5 + 37) # TDB to UTC delta
        date_utc = datetime.datetime.fromtimestamp(EPOCH_2000 + time - delta, tz=datetime.timezone.utc)
        if self.timeline:
            date_str = date_utc.isoformat()
            self.timeline.set_time(date_str)
            self.select_in_table(self.get_block_index(date_str))

    def get_block_index(self, timestamp):
        for index, start, end in self.block_timeline_index:
            if start <= timestamp <= end:
                return index
        return None

    def select_in_table(self, index):
        if index is None:
            return
        table = self.ui.tableWidget
        table.clearSelection()
        table.setRangeSelected(QTableWidgetSelectionRange(index, 0, index, 2), True)
        table.scrollToItem(table.item(index, 0))
        self.show_block_index(index)

    def edit_item(self, item):
        item.doEdit()

    def goto_date_timeline(self, value):
        self.goto_date_cosmographia(value)
        self.select_in_table(self.get_block_index(value))

    def goto_date_cosmographia(self, utc_str):
        self.cosmo.setTime(utc_str + " UTC")

    def show_block(self, item):
        self.show_block_index(item.row())

    def show_block_index(self, index):
        if index in self.block_contents:
            block_content = self.block_contents[index]
            self.ui.blockTextEdit.setPlainText(block_content)
        else:
            self.ui.blockTextEdit.setPlainText('Slewing to block...')

    def show_and_focus(self):
        self.hide()
        self.show()