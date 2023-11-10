from PyQt5.QtWidgets import QTabWidget, QGridLayout, QCheckBox, QPushButton, QWidget, QVBoxLayout
from PyQt5.QtCore import Qt



class TabbedSelector(QWidget):

    def __init__(self, parent, items, callback, num_colums=4):
        super(QWidget, self).__init__(parent)
        self.callback = callback
        self.setup(items, num_colums)

    def setup(self, items, num_columns):

        main_layout = QVBoxLayout()
        tabmm_map = dict()
        tabmm_index = dict()
        tabmm_widget = QTabWidget()

        group_checkboxes = dict()
        for group_name in sorted(items.keys()):
            group_moons = items[group_name]
            group_checkboxes[group_name] = list()
            for moon in sorted(group_moons):
                tab_id = group_name
                if tab_id not in tabmm_map:
                    new_layout = QGridLayout()
                    new_widget = QWidget()
                    new_widget.setLayout(new_layout)
                    tabmm_map[tab_id] = new_layout
                    tabmm_index[tab_id] = 0
                    tabmm_widget.addTab(new_widget, tab_id.lower())

                layout = tabmm_map[tab_id]
                new_index = tabmm_index[tab_id]
                tabmm_index[tab_id] = new_index + 1
                cb = QCheckBox(moon, self)
                cb.setChecked(False)
                cb.stateChanged.connect(
                    lambda state, name=moon: self.adapt_callback(state, name))
                col = new_index % num_columns
                row = new_index // num_columns
                layout.addWidget(cb, col, row)
                self.adapt_callback(Qt.Unchecked, moon)
                group_checkboxes[group_name].append(cb)

            layout = tabmm_map[group_name]
            checkboxes = group_checkboxes[group_name]
            select_all = QPushButton('Select all')
            select_all.clicked.connect(lambda state, group=checkboxes: self.toggle_group(group, True))
            layout.addWidget(select_all, layout.rowCount() + 1, 0, 1, layout.columnCount())
            unselect_all = QPushButton('Deselect all')
            unselect_all.clicked.connect(lambda state, group=checkboxes: self.toggle_group(group, False))
            layout.addWidget(unselect_all, layout.rowCount() + 1, 0, 1, layout.columnCount())
        main_layout.addWidget(tabmm_widget)
        self.setLayout(main_layout)

    def toggle_group(self, checkboxes, value):
        for cb in checkboxes:
            cb.setChecked(value)

    def adapt_callback(self, state, name):
        self.callback(True if state == Qt.Checked else False, name)
