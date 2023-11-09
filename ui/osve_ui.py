from ui.load import get_main_window, add_menu, MenuSpec, ActionSpec, BasicDialog

from PyQt5.QtWidgets import qApp, QMenuBar, QAction, QMenu, QDialog, QPushButton, QVBoxLayout
from PyQt5.QtGui import QIcon
from ui.design.ptr_editor import Ui_Form as PTRForm

class PTREditorDialog(QDialog):

    id = 'basic_dialog_window_id'

    def __init__(self, main_window):
        QDialog.__init__(self, main_window)
        self.init_ui()

    def init_ui(self):
        self.setObjectName(BasicDialog.id)
        self.ptr_editor = PTRForm()
        self.ptr_editor.setupUi(self)

        # self.setGeometry(100, 100, 521, 360)



    def show_and_focus(self):
        self.hide()
        self.show()


def create_ui():
    main_window = get_main_window()
    main_window.setWindowOpacity(0.9)

    bd = PTREditorDialog(main_window)
    add_menu(main_window, MenuSpec('OSVE', [ActionSpec('PTR request', 'Execute OSVE', 'Alt+P', bd.show_and_focus)]))
