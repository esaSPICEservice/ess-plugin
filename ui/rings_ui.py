
from ui.design.style import common_style
from PyQt5.QtWidgets import QDialog, QVBoxLayout
from ui.tabbed_selector import TabbedSelector
from actions.rings import get_rings, toggle_ring

class RingsDialog(QDialog):

    id = 'rings_dialog_window_id'

    def __init__(self, main_window):
        QDialog.__init__(self, main_window)
        self.init_ui()

    def init_ui(self):
        self.setObjectName(RingsDialog.id)
        self.setStyleSheet(common_style)
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.tabSelector = TabbedSelector(self, get_rings(), toggle_ring, num_colums=1)
        self.setWindowTitle('Jupiter Rings and Moon Torus')
        layout.addWidget(self.tabSelector)


    def show_and_focus(self):
        self.hide()
        self.show()