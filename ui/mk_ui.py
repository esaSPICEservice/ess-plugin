
from PyQt5.QtWidgets import qApp, QMenuBar, QAction, QFileDialog, QDialog, QMessageBox, QVBoxLayout
from ui.design.mk_loader import Ui_mkLoaderWidget
from actions.mkloader import execute
import os


class MkLoaderDialog(QDialog):

    id = 'mk_loader_dialog_window_id'

    def __init__(self, main_window):
        QDialog.__init__(self, main_window)
        self.init_ui()

    def init_ui(self):
        self.setObjectName(MkLoaderDialog.id)
        self.mk_loader = Ui_mkLoaderWidget()
        self.mk_loader.setupUi(self)
        self.mk_loader.visualizeButton.clicked.connect(self.visualize)
        self.mk_loader.mkButton.clicked.connect(self.browse_mk)
        self.mk_loader.extraAddButton.clicked.connect(self.add_kernel)
        self.mk_loader.extraBrowseButton.clicked.connect(self.browse_extra)
        self.mk_loader.mkInput.setText('/Users/randres/juice_repo/juice_crema_5_1_150lb_23_1_v435_20230918_001.tm')
        

    def add_kernel(self):
        extra = self.mk_loader.extraInput.text()
        self.mk_loader.extraInput.setText('')
        if extra:
            if os.path.exists(extra):
                self.mk_loader.extraList.addItem(extra)
            else:
                QMessageBox.warning(self, 'Add extra kernel',
                                    f'Kernel file not valid {extra}' )
    def visualize(self):
        date = '2031-09-07T12:00:00 UTC'
        mk = self.mk_loader.mkInput.text()
        lw = self.mk_loader.extraList
        extra_kernels = [lw.item(x).text() for x in range(lw.count())]
        try:
            execute(mk, extra_kernels, date)
            self.hide()
        except ValueError as error:
            QMessageBox.warning(self, 'PTR editor',
                                f'PTR not valid {error}' )

    def browse_mk(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Select Metarkernel", None, "Metakernel files (*.tm *.mk)")
        if file_name:
            self.mk_loader.mkInput.setText(file_name)
        self.show_and_focus()

    def browse_extra(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Select Extra Kernel", None, "Kernel files (*.*)")
        if file_name:
            self.mk_loader.extraInput.setText(file_name)
        self.show_and_focus()


    def show_and_focus(self):
        self.hide()
        self.show()


