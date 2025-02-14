from ui.design.style import common_style
from PyQt5.QtWidgets import QDialog, QVBoxLayout
from ui.tabbed_selector import TabbedSelector
from actions.moons import get_moons, toggle_moon

class MoonsDialog(QDialog):

    id = 'moons_dialog_window_id'

    def __init__(self, main_window):
        QDialog.__init__(self, main_window)
        self.init_ui()

    def init_ui(self):
        self.setObjectName(MoonsDialog.id)
        self.setStyleSheet(common_style)
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.tabSelector = TabbedSelector(self, get_moons(), toggle_moon, num_colums=5)
        self.setWindowTitle ('Jupiter Moons')
        layout.addWidget(self.tabSelector)

    def show_and_focus(self):
        self.hide()
        self.show()


