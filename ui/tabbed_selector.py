from PyQt5.QtWidgets import QTabWidget, QGridLayout, QCheckBox, QPushButton, QWidget, QVBoxLayout, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt
import math



class TabbedSelector(QWidget):

    def __init__(self, parent, items, callback, num_colums=4):
        super(QWidget, self).__init__(parent)
        self.callback = callback
        self.checkboxes = []
        self.setup(items, num_colums)

    def setup(self, items, num_colums):

        n_items = max([len(value) for value in items.values()]) 
        items_per_row = math.ceil(n_items / num_colums)
        main_layout = QVBoxLayout()
        tabmm_map = dict()
        tabmm_index = dict()
        tabmm_widget = QTabWidget()
        all_checkboxes = []
        group_checkboxes = dict()
        for group_name in sorted(items.keys()):
            group_moons = items[group_name]
            group_checkboxes[group_name] = list()
            for moon in sorted(group_moons,key=lambda item: item[1] if type(item) is tuple else item):

                if type(moon) is tuple:
                    moon_value = moon[0]
                    moon_label = moon[1]
                else:
                    moon_value = moon
                    moon_label = moon

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
                cb = QCheckBox(moon_label, self)
                cb.setChecked(False)
                cb.stateChanged.connect(
                    lambda state, name=moon_value: self.adapt_callback(state, name))
                col = new_index % items_per_row
                row = new_index // items_per_row
                layout.addWidget(cb, col, row)
                self.adapt_callback(Qt.Unchecked, moon_value)
                group_checkboxes[group_name].append(cb)
                self.checkboxes.append(cb)
                all_checkboxes.append(cb)

            layout = tabmm_map[group_name]
            checkboxes = group_checkboxes[group_name]
            # Add a vertical spacer with a size of 10 pixels
            spacer = QSpacerItem(0, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)
            layout.addItem(spacer)

            select_all = QPushButton('Select group')
            select_all.clicked.connect(lambda state, group=checkboxes: self.toggle_group(group, True))
            layout.addWidget(select_all, layout.rowCount() + 1, 0, 1, layout.columnCount())
            unselect_all = QPushButton('Deselect group')
            unselect_all.clicked.connect(lambda state, group=checkboxes: self.toggle_group(group, False))
            layout.addWidget(unselect_all, layout.rowCount() + 1, 0, 1, layout.columnCount())

        main_layout.addWidget(tabmm_widget)
        select_all = QPushButton('Select all')
        select_all.clicked.connect(lambda state, group=all_checkboxes: self.toggle_group(group, True))
        main_layout.addWidget(select_all)
        unselect_all = QPushButton('Deselect all')
        unselect_all.clicked.connect(lambda state, group=all_checkboxes: self.toggle_group(group, False))
        main_layout.addWidget(unselect_all)
        self.setLayout(main_layout)

    def toggle_group(self, checkboxes, value):
        for cb in checkboxes:
            cb.setChecked(value)

    def adapt_callback(self, state, name):
        self.callback(True if state == Qt.Checked else False, name)

    def get_state(self):
        state = {}
        for cb in self.checkboxes:
            state[cb.text()] = cb.isChecked()
        return state
