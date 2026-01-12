import sys
import json
from PyQt5.QtWidgets import (
    QApplication,
    QDialog,
    QTreeView,
    QFileDialog,
    QMessageBox,
    QLineEdit,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QCheckBox,
    QTextEdit,
    QLabel
)
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QColor, QFontMetrics
from PyQt5.QtCore import Qt, QSortFilterProxyModel, QModelIndex


SEVERITY_COLORS = {
    "DEBUG": QColor(235, 235, 235),
    "INFO": QColor(220, 235, 255),
    "WARNING": QColor(255, 235, 200),
    "ERROR": QColor(255, 210, 210),
}


class JsonFilterProxy(QSortFilterProxyModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.allowed_severities = {"INFO", "WARNING", "ERROR"}
        self.allowed_modules = {"AGM", "OSVE"}

    def filterAcceptsRow(self, source_row, source_parent):
        model = self.sourceModel()
        headers = getattr(model, "headers", [])

        # Severity filter
        if "severity" in headers:
            sev_col = headers.index("severity")
            sev_index = model.index(source_row, sev_col, source_parent)
            severity = str(model.data(sev_index)).upper()
            if severity and severity not in self.allowed_severities:
                return False

        # Module filter
        if "module" in headers:
            mod_col = headers.index("module")
            mod_index = model.index(source_row, mod_col, source_parent)
            module = str(model.data(mod_index)).upper()
            if module and module not in self.allowed_modules:
                return False

        # Text filter (all columns)
        pattern = self.filterRegExp().pattern()
        if not pattern:
            return True

        for col in range(model.columnCount()):
            index = model.index(source_row, col, source_parent)
            if self.filterRegExp().indexIn(str(model.data(index))) != -1:
                return True

        return False


class TextPopup(QDialog):
    def __init__(self, text, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Details")
        self.resize(600, 300)

        edit = QTextEdit(self)
        edit.setReadOnly(True)
        edit.setText(text)

        layout = QVBoxLayout(self)
        layout.addWidget(edit)


class JsonTreeDialog(QDialog):
    def __init__(self, parent, json_path):
        super().__init__(parent)
        self.json_path = json_path
        self.setWindowTitle("OSVE Log Viewer")
        self.resize(1100, 600)

        self.model = QStandardItemModel(self)
        self.proxy = JsonFilterProxy(self)
        self.proxy.setSourceModel(self.model)
        self.proxy.setFilterCaseSensitivity(Qt.CaseInsensitive)

        self.tree = QTreeView(self)
        self.tree.setModel(self.proxy)
        self.tree.setRootIsDecorated(False)
        self.tree.setAlternatingRowColors(True)
        self.tree.setSortingEnabled(True)
        self.tree.doubleClicked.connect(self.show_cell_popup)

        self.filter_edit = QLineEdit(self)
        self.filter_edit.setPlaceholderText("Text filter…")
        self.filter_edit.textChanged.connect(self.proxy.setFilterFixedString)

        # Severity checkboxes
        self.severity_cbs = {}
        sev_layout = QHBoxLayout()
        sev_layout.addWidget(QLabel("Severity:"))

        for sev in ["DEBUG", "INFO", "WARNING", "ERROR"]:
            cb = QCheckBox(sev)
            cb.setChecked(sev != "DEBUG")
            cb.stateChanged.connect(self.update_filters)
            self.severity_cbs[sev] = cb
            sev_layout.addWidget(cb)

        sev_layout.addStretch()

        # Module checkboxes
        self.module_cbs = {}
        mod_layout = QHBoxLayout()
        mod_layout.addWidget(QLabel("Module:"))

        for mod in ["AGM", "OSVE"]:
            cb = QCheckBox(mod)
            cb.setChecked(True)
            cb.stateChanged.connect(self.update_filters)
            self.module_cbs[mod] = cb
            mod_layout.addWidget(cb)

        mod_layout.addStretch()


        self.close_button = QPushButton("Close")
        self.close_button.clicked.connect(self.close)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.close_button)

        layout = QVBoxLayout(self)
        layout.addWidget(self.filter_edit)
        layout.addLayout(sev_layout)
        layout.addLayout(mod_layout)
        layout.addWidget(self.tree)
        layout.addLayout(button_layout)

    def update_filters(self):
        self.proxy.allowed_severities = {
            sev for sev, cb in self.severity_cbs.items() if cb.isChecked()
        }
        self.proxy.allowed_modules = {
            mod for mod, cb in self.module_cbs.items() if cb.isChecked()
        }
        self.proxy.invalidateFilter()


    def populate_model(self, data):
        self.model.clear()
        if not data:
            return

        headers = list(data[0].keys())
        self.model.headers = headers 
        self.model.setHorizontalHeaderLabels(headers)

        for entry in data:
            severity = entry.get("severity", "").upper()
            color = SEVERITY_COLORS.get(severity)
            row_items = []

            for key in headers:
                item = QStandardItem(str(entry.get(key, "")))
                item.setEditable(False)
                if color:
                    item.setBackground(color)
                row_items.append(item)

            self.model.appendRow(row_items)

        self.tree.resizeColumnToContents(0)
        self._set_field_column_width(headers)
        self.update_filters()


    def _set_field_column_width(self, headers, field="text", length=64):
        if field not in headers:
            return

        field_col = headers.index(field)
        metrics = QFontMetrics(self.tree.font())
        width = metrics.width("X" * length)
        self.tree.setColumnWidth(field_col, width)


    def show_cell_popup(self, index: QModelIndex):
        source_index = self.proxy.mapToSource(index)
        text = str(self.model.data(source_index))
        TextPopup(text, self).exec_()

    def show_and_focus(self):
        self.hide()
        with open(self.json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.populate_model(data)
        self.show()


