from ui.common import get_main_window, add_menu, MenuSpec, ActionSpec
from ui.design.moons_panel import Ui_Form
from PyQt5.QtWidgets import QSpacerItem, QDialog, QSizePolicy
from ui.tabbed_selector import TabbedSelector
from actions.moons import get_moons, toggle_moon

class MoonsDialog(QDialog):

    id = 'moons_dialog_window_id'

    def __init__(self, main_window):
        QDialog.__init__(self, main_window)
        self.init_ui()

    def init_ui(self):
        self.setObjectName(MoonsDialog.id)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.tabSelector = TabbedSelector(self, get_moons(), toggle_moon)
        self.ui.label.setText('Jupiter Rings and Moon Torus')
        self.ui.verticalLayout.addWidget(self.tabSelector)
        self.ui.verticalLayout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

    def show_and_focus(self):
        self.hide()
        self.show()


