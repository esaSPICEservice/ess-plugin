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
        self.tableWidget.setHorizontalHeaderLabels(['RA', 'DEC', 'Name'])
        self.tableWidget.setEditTriggers(QAbstractItemView.AllEditTriggers)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.tableWidget)

        formLayout = QFormLayout()
        self.raInput = QLineEdit()
        self.decInput = QLineEdit()
        self.nameInput = QLineEdit()
        formLayout.addRow(QLabel('Right Ascension (J2000)'), self.raInput)
        formLayout.addRow(QLabel('Declination (J2000)'), self.decInput)
        formLayout.addRow(QLabel('Name'), self.nameInput)

        buttonLayout = QHBoxLayout()
       
        saveStarsButton = QPushButton('Save stars')
        saveStarsButton.clicked.connect(self.saveStars)
        buttonLayout.addWidget(saveStarsButton)

        layout.addLayout(formLayout)
        layout.addLayout(buttonLayout)

        self.setLayout(layout)

    def addRow(self):
        ra = self.raInput.text()
        dec = self.decInput.text()
        name = self.nameInput.text()
        if self.isValidRaDec(ra, dec):
            rowPosition = self.tableWidget.rowCount()
            self.tableWidget.insertRow(rowPosition)
            self.tableWidget.setItem(rowPosition, 0, QTableWidgetItem(ra))
            self.tableWidget.setItem(rowPosition, 1, QTableWidgetItem(dec))
            self.tableWidget.setItem(rowPosition, 2, QTableWidgetItem(name))
            self.raInput.clear()
            self.decInput.clear()
            self.nameInput.clear()
        else:
            QMessageBox.warning(self, "Invalid Input", "RA and DEC must be valid float numbers")

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

    def show_and_focus(self, callback):
        self.callback = callback
        self.hide()
        self.show()