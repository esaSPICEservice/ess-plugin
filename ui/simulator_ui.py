from ui.common import get_main_window, add_menu, MenuSpec, ActionSpec

from PyQt5.QtWidgets import qApp, QMenuBar, QAction, QFileDialog, QDialog, QMessageBox, QVBoxLayout
from ui.design.ptr_editor import Ui_ptrEditorWidget
from actions.ptr import execute_ptr, validate_ptr
class PTREditorDialog(QDialog):

    id = 'ptr_editor_dialog_window_id'

    def __init__(self, main_window):
        QDialog.__init__(self, main_window)
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

        self.ptr_editor.mkInput.setText('/Users/randres/juice_repo/juice_crema_5_1_150lb_23_1_v435_20230918_001.tm')


    def visualize(self):
        ptr_content =  self.ptr_editor.ptrEditor.toPlainText()
        mk = self.ptr_editor.mkInput.text()
        try:
            execute_ptr(mk, ptr_content)
            self.hide()
        except ValueError as error:
            QMessageBox.warning(self, 'PTR editor',
                                f'PTR not valid {error}' )

    def browse_mk(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Open Metarkernel", None, "Metakernel files (*.tm *.mk)")
        if file_name:
            self.ptr_editor.mkInput.setText(file_name)

    def open_ptr(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Open PTR", None, "PTR (*.*)")
        if file_name:
            with open(file_name, 'r') as ptr_file:
                content = ptr_file.read()
                self.ptr_editor.ptrEditor.setPlainText(content)

    def save_ptr(self):
        ptr_content = self.validate_ptr()
        if ptr_content:
            file_name, _ = QFileDialog.getSaveFileName(
                self, 'Save PTR', None, 'PTR file (*.ptx)')
            if file_name:
                with open(file_name, 'w') as ptr_file:
                    ptr_file.write(ptr_content)

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


def create_ui():
    main_window = get_main_window()
    main_window.setWindowOpacity(0.9)

    bd = PTREditorDialog(main_window)
    add_menu(main_window, MenuSpec('Simulator', [ActionSpec('PTR request', 'Execute OSVE', 'Alt+P', bd.show_and_focus)]))
