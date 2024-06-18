
from PyQt5.QtWidgets import QFileDialog, QDialog, QMessageBox
from PyQt5.QtCore import Qt, QDateTime
from ui.common import get_settings, get_runtime
from ui.design.mk_loader import Ui_mkLoaderWidget
from actions.mkloader import execute
import os

from settings.handler import last_repo_key, last_kernel_key, last_start_date

class MkLoaderDialog(QDialog):

    id = 'mk_loader_dialog_window_id'

    def __init__(self, main_window):
        QDialog.__init__(self, main_window)
        self.settings = get_settings()
        self.run_time = get_runtime()
        self.mission = self.run_time.get('mission')
        self.init_ui()

    def init_ui(self):
        self.setObjectName(MkLoaderDialog.id)
        self.mk_loader = Ui_mkLoaderWidget()
        self.mk_loader.setupUi(self)
        self.mk_loader.visualizeButton.clicked.connect(self.visualize)
        self.mk_loader.mkButton.clicked.connect(self.browse_mk)
        self.mk_loader.extraAddButton.clicked.connect(self.add_kernel)
        self.mk_loader.extraBrowseButton.clicked.connect(self.browse_extra)
        self.mk_loader.extraResetButton.clicked.connect(self.reset_extra)

    def reset_extra(self):
        self.mk_loader.extraList.clear()
        self.mk_loader.extraInput.setText('')

    def add_kernel(self):
        extra = self.mk_loader.extraInput.text()
        self.mk_loader.extraInput.setText('')
        if extra:
            if os.path.exists(extra):
                self.mk_loader.extraList.addItem(extra)
            else:
                QMessageBox.warning(self, 'Add extra kernel',
                                    'Kernel file not valid ' + extra)
    def visualize(self):
        date = self.mk_loader.dateTimeEdit.dateTime().toUTC().toString(Qt.ISODate)
        mk = self.mk_loader.mkInput.text()

        if not date or not mk or not os.path.exists(mk):
            QMessageBox.warning(self, 'PTR editor', 'Date and metakernel are mandatory')
            return

        self.settings.set(self.mission, last_repo_key, os.path.dirname(mk))
        self.settings.set(self.mission, last_kernel_key, mk)
        self.settings.set(self.mission, last_start_date, date)
        self.settings.save()

        lw = self.mk_loader.extraList
        extra_kernels = [lw.item(x).text() for x in range(lw.count())]
        try:
            execute(mk, extra_kernels, date)
            self.hide()
        except ValueError as error:
            QMessageBox.warning(self, 'PTR editor',
                                'PTR not valid' + error)

    def browse_mk(self):
        default_folder = self.settings.get(self.mission, last_repo_key, '')
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Select Metarkernel", default_folder, "Metakernel files (*.tm *.mk)")
        if file_name:
            self.mk_loader.mkInput.setText(file_name)
        self.focus()

    def browse_extra(self):
        default_folder = self.settings.get(self.mission, last_repo_key, '')
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Select Extra Kernel", default_folder, "Kernel files (*.*)")
        if file_name:
            self.mk_loader.extraInput.setText(file_name)
        self.focus()


    def show_and_focus(self):
        mk = self.settings.get(self.mission, last_kernel_key, '')
        self.mk_loader.mkInput.setText(mk)
        start_date = self.settings.get(self.mission, last_start_date, '2010-01-01T00:00:00Z')
        dt = QDateTime.fromString(start_date, 'yyyy-M-dThh:mm:ssZ')
        self.mk_loader.dateTimeEdit.setDateTime(dt)
        self.focus()

    def focus(self):
        self.hide()
        self.show()
