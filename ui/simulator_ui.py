from ui.common import get_settings_handler

from PyQt5.QtWidgets import  QFileDialog, QDialog, QMessageBox
from ui.design.ptr_editor import Ui_ptrEditorWidget
from actions.ptr import execute_ptr, validate_ptr
from settings.handler import last_repo_key, last_kernel_key

import os
class PTREditorDialog(QDialog):

    id = 'ptr_editor_dialog_window_id'

    def __init__(self, main_window):
        QDialog.__init__(self, main_window)
        self.settings_hdl = get_settings_handler()
        self.init_ui()

    def init_ui(self):
        self.setObjectName(PTREditorDialog.id)
        self.ptr_editor = Ui_ptrEditorWidget()
        self.ptr_editor.setupUi(self)
        self.ptr_editor.visualizeButton.clicked.connect(self.visualize)
        self.ptr_editor.mkButton.clicked.connect(self.browse_mk)
        self.ptr_editor.openButton.clicked.connect(self.open_ptr)
        self.ptr_editor.saveButton.clicked.connect(self.save_ptr)
        self.ptr_editor.cleanButton.clicked.connect(self.clean_ptr)

        mk = self.settings_hdl.settings.get(last_kernel_key, '')
        self.ptr_editor.mkInput.setText(mk)

    def visualize(self):
        ptr_content =  self.ptr_editor.ptrEditor.toPlainText()
        mk = self.ptr_editor.mkInput.text()
        if not ptr_content or not mk or not os.path.exists(mk):
            QMessageBox.warning(self, 'PTR editor', f'PTR and metakernel are mandatory')
            return

        self.settings_hdl.settings[last_repo_key] = os.path.dirname(mk)
        self.settings_hdl.settings[last_kernel_key] = mk
        self.settings_hdl.save()

        calculate_power = self.ptr_editor.powerCheck.isChecked()
        calculate_sa = self.ptr_editor.saCheck.isChecked()
        calculate_mga = self.ptr_editor.mgaCheck.isChecked()
        
        try:
            execute_ptr(mk, ptr_content, calculate_power, calculate_sa, calculate_mga)
            self.hide()
        except ValueError as error:
            QMessageBox.warning(self, 'PTR editor',
                                f'PTR not valid {error}' )

    def browse_mk(self):
        default_folder = self.settings_hdl.settings.get(last_repo_key, '')
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Open Metarkernel", default_folder, "Metakernel files (*.tm *.mk)")
        if file_name:
            self.ptr_editor.mkInput.setText(file_name)
            self.show_and_focus()

    def open_ptr(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Open PTR", None, "PTR (*.*)")
        if file_name:
            with open(file_name, 'r') as ptr_file:
                content = ptr_file.read()
                self.ptr_editor.ptrEditor.setPlainText(content)
            self.show_and_focus()

    def save_ptr(self):
        ptr_content = self.validate_ptr()
        if ptr_content:
            file_name, _ = QFileDialog.getSaveFileName(
                self, 'Save PTR', None, 'PTR file (*.ptx)')
            if file_name:
                with open(file_name, 'w') as ptr_file:
                    ptr_file.write(ptr_content)
            self.show_and_focus()

    def validate_ptr(self):
        ptr_content =  self.ptr_editor.ptrEditor.toPlainText()
        
        try:
            validate_ptr(ptr_content)
        except ValueError as error:
            QMessageBox.warning(self, 'PTR editor',
                                f'PTR not valid {error}' )
            return None
        return ptr_content

    def clean_ptr(self):
        content = """
<prm>
<body>
    <segment>
    <data>
        <timeline frame="SC">
                <block ref="OBS">
                    <startTime>2032-05-15T20:00:00</startTime>
                    <endTime>2032-05-15T20:15:00</endTime>
                    <attitude ref="terminator">
                        <boresight ref="SC_Zaxis" />
                        <surface ref="Jupiter" />
                        <phaseAngle ref="powerOptimised">
                            <yDir> false </yDir>
                        </phaseAngle>
                    </attitude>
                </block>
        </timeline>
    </data>
    </segment>
</body>
</prm>
"""
        self.ptr_editor.ptrEditor.setPlainText(content)

    def show_and_focus(self):
        self.hide()
        self.show()
