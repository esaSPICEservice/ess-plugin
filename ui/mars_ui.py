from ui.design.style import common_style
from PyQt5.QtWidgets import QSpacerItem, QDialog, QSizePolicy, QVBoxLayout
from ui.tabbed_selector import TabbedSelector
from actions.mars import get_structures, toggle_structure

class MarsDialog(QDialog):

    id = 'mars_dialog_window_id'

    def __init__(self, main_window):
        QDialog.__init__(self, main_window)
        self.init_ui()

    def init_ui(self):
        self.setObjectName(MarsDialog.id)
        self.setStyleSheet(common_style)
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.tabSelector = TabbedSelector(self, get_structures(), toggle_structure)
        self.setWindowTitle("Mars Structures")
        layout.addWidget(self.tabSelector)

    def show_and_focus(self):
        self.hide()
        self.show()


