
from ui.design.block_panel import Ui_Form
from PyQt5.QtWidgets import QDialog, QTableWidgetItem, QTableWidget

from utils.block_parser import BlockParser
from actions.time_navigation import goto_date
from utils.time import duration

class DateTableWidgetItem(QTableWidgetItem):
    
    def __init__(self, date_str):
        QTableWidgetItem.__init__(self, date_str)
        self.date_str = date_str

    def doEdit(self):
        goto_date(self.date_str)

class BlockTableWidgetItem(QTableWidgetItem):
    
    def __init__(self, block_str):
        QTableWidgetItem.__init__(self, block_str)

    def doEdit(self):
        pass

class BlocksDialog(QDialog):

    id = 'blocks_dialog_window_id'

    def __init__(self, main_window, ptr_path):
        QDialog.__init__(self, main_window)
        self.ptr_path = ptr_path
        self.init_ui()

    def init_ui(self):
        self.setObjectName(BlocksDialog.id)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        
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
            for index, start_time in enumerate(parser.start_times):
                if start_time:
                    duration_secs = duration(start_time, parser.end_times[index])
                    self.ui.tableWidget.insertRow(row_number)
                    self.ui.tableWidget.setItem(
                        row_number, 0, 
                        DateTableWidgetItem(start_time))
                    self.ui.tableWidget.setItem(
                        row_number, 1, 
                        DateTableWidgetItem(parser.end_times[index]))
                    self.ui.tableWidget.setItem(
                        row_number, 2, 
                        BlockTableWidgetItem(str(duration_secs)))
                    self.block_contents[row_number] = parser.block_contents[index]
                    row_number +=1
                    

        except Exception as error:
            print(error)

    def edit_item(self, item):
        item.doEdit()

    def show_block(self, item):
        self.show_block_index(item.row())

    def show_block_index(self, index):
        block_content = self.block_contents[index]
        self.ui.blockTextEdit.setPlainText(block_content)

    def show_and_focus(self):
        self.hide()
        self.show()