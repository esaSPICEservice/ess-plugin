from PyQt5.QtWidgets import  ( QDialog, QTableWidget, QTableWidgetItem, 
                              QVBoxLayout, QPushButton, QHBoxLayout,
                                QAbstractItemView, QFormLayout, 
                                QLineEdit, QLabel, QMessageBox, QFileDialog)
import csv

class StarDBDialog(QDialog):

    id = 'stardb_dialog_window_id'
    def __init__(self, main_window):
        super().__init__(main_window)
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 600, 400)
        self.setWindowTitle('Star Database Customizer')

        layout = QVBoxLayout()

        buttonLayout = QHBoxLayout()
        addButton = QPushButton('Add Star')
        addButton.clicked.connect(self.addRow)
        buttonLayout.addWidget(addButton)

        removeButton = QPushButton('Remove Star')
        removeButton.clicked.connect(self.removeRow)
        buttonLayout.addWidget(removeButton)

        importFromCsvButton = QPushButton('Import from CSV')
        importFromCsvButton.clicked.connect(self.importFromCsv)
        buttonLayout.addWidget(importFromCsvButton)
        layout.addLayout(buttonLayout)

        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(['RA J2000 (deg)', 'DEC J2000 (deg)', 'Star Name'])
        self.tableWidget.setEditTriggers(QAbstractItemView.AllEditTriggers)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.cellChanged.connect(self.validateCell)
        layout.addWidget(self.tableWidget)

        buttonLayout = QHBoxLayout()
        cancelButton = QPushButton('Cancel')
        cancelButton.clicked.connect(self.cancel)
        buttonLayout.addWidget(cancelButton)
        saveStarsButton = QPushButton('Save stars')
        saveStarsButton.clicked.connect(self.saveStars)
        buttonLayout.addWidget(saveStarsButton)

        # layout.addLayout(formLayout)
        layout.addLayout(buttonLayout)

        self.setLayout(layout)


    def validateCell(self, row, column):
        # Only check RA (0) and DEC (1) columns
        if column in (0, 1):
            item = self.tableWidget.item(row, column)
            text = item.text()
            try:
                value = float(text)
                if column == 0 and not (0 <= value < 360):
                    raise ValueError("RA must be 0-360°")
                elif column == 1 and not (-90 <= value <= 90):
                    raise ValueError("DEC must be -90° to 90°")
            except ValueError:
                QMessageBox.warning(
                    self, "Invalid Input",
                    f"Invalid value for {'RA' if column == 0 else 'DEC'}: {text}"
                )
                self.tableWidget.blockSignals(True) 
                item.setText('')  # Clear invalid input
                self.tableWidget.blockSignals(False) 

    def addRow(self):
        """Add an empty row to the table."""
        rowPosition = self.tableWidget.rowCount()
        self.tableWidget.insertRow(rowPosition)
        self.tableWidget.blockSignals(True) 
        # Insert empty cells
        self.tableWidget.setItem(rowPosition, 0, QTableWidgetItem(''))
        self.tableWidget.setItem(rowPosition, 1, QTableWidgetItem(''))
        self.tableWidget.setItem(rowPosition, 2, QTableWidgetItem(''))
        self.tableWidget.blockSignals(False) 

    def removeRow(self):
        rowPosition = self.tableWidget.currentRow()
        if rowPosition >= 0:
            self.tableWidget.removeRow(rowPosition)


    def getContents(self):
        contents = []
        FAKE_ID_START = 9999
        for row in range(self.tableWidget.rowCount()):
            ra = float(self.tableWidget.item(row, 0).text())
            dec = float(self.tableWidget.item(row, 1).text())
            name = self.tableWidget.item(row, 2).text()
            contents.append( {'ra': ra, 'dec': dec, 'name': name, 'id': row + FAKE_ID_START} )
        return contents

    def addFromList(self, contents):
        for row, content in enumerate(contents):
            self.tableWidget.insertRow(row)
            self.tableWidget.setItem(row, 0, QTableWidgetItem(str(content.get('ra'))))
            self.tableWidget.setItem(row, 1, QTableWidgetItem(str(content.get('dec'))))
            self.tableWidget.setItem(row, 2, QTableWidgetItem(content.get('name')))

    def importFromCsv(self):
        filename, _ = QFileDialog.getOpenFileName(self, 'Open CSV File', '.', 'CSV Files (*.csv)')
        if filename:
            with open(filename, 'r') as file:
                reader = csv.reader(file)
                row = 0
                for content in reader:
                    if len(content) == 3:
                        self.tableWidget.insertRow(row)
                        self.tableWidget.setItem(row, 0, QTableWidgetItem(content[0]))
                        self.tableWidget.setItem(row, 1, QTableWidgetItem(content[1]))
                        self.tableWidget.setItem(row, 2, QTableWidgetItem(content[2]))
                        row += 1
                    else:
                        QMessageBox.warning(self, "Invalid CSV File", "Each row must have exactly 3 columns")


    def isValidRaDec(self, ra, dec):
        try:
            float(ra)
            float(dec)
            return True
        except ValueError:
            return False

    def saveStars(self):
        self.callback(self.getContents())
        self.close()

    def cancel(self):
        self.cancel_callback()
        self.close()

    def show_and_focus(self, callback, cancel_callback):
        self.callback = callback
        self.cancel_callback = cancel_callback
        self.hide()
        self.show()