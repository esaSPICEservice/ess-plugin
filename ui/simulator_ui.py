from ui.common import get_settings, get_runtime

from PyQt5.QtWidgets import  QFileDialog, QDialog, QMessageBox, QCompleter
from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor
from PyQt5.QtCore import QRegExp, QStringListModel, Qt

from ui.design.ptr_editor import Ui_ptrEditorWidget
from actions.ptr import execute_ptr, validate_ptr
from settings.handler import last_repo_key, last_kernel_key

import os


class XmlHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super(XmlHighlighter, self).__init__(parent)
        self.highlightingRules = []

        # Define formats for different XML elements
        tagFormat = QTextCharFormat()
        tagFormat.setForeground(QColor("blue"))
        self.highlightingRules.append((r"</?[^>]+>", tagFormat))

        attributeFormat = QTextCharFormat()
        attributeFormat.setForeground(QColor("red"))
        self.highlightingRules.append((r"\b\w+=(\"[^\"]*\"|'[^']*')", attributeFormat))

        valueFormat = QTextCharFormat()
        valueFormat.setForeground(QColor("green"))
        self.highlightingRules.append((r"\"[^\"]*\"|'[^']*'", valueFormat))

    def highlightBlock(self, text):
        for pattern, format in self.highlightingRules:
            expression = QRegExp(pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)

class PTREditorDialog(QDialog):

    id = 'ptr_editor_dialog_window_id'

    def __init__(self, main_window):
        QDialog.__init__(self, main_window, Qt.WindowStaysOnTopHint)
        self.settings = get_settings()
        self.runtime = get_runtime()
        self.mission = self.runtime.get('mission')
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

        mk = self.settings.get(self.mission, last_kernel_key, '')
        self.ptr_editor.mkInput.setText(mk)

        self.highlighter = XmlHighlighter(self.ptr_editor.ptrEditor.document())

    def visualize(self):
        ptr_content =  self.ptr_editor.ptrEditor.toPlainText()
        mk = self.ptr_editor.mkInput.text()
        if not ptr_content or not mk or not os.path.exists(mk):
            QMessageBox.warning(self, 'PTR editor', 'PTR and metakernel are mandatory')
            return

        self.settings.set(self.mission, last_repo_key, os.path.dirname(mk))
        self.settings.set(self.mission, last_kernel_key, mk)
        self.settings.save()

        # calculate_power = self.ptr_editor.powerCheck.isChecked()
        # calculate_sa = self.ptr_editor.saCheck.isChecked()
        # calculate_mga = self.ptr_editor.mgaCheck.isChecked()

        calculate_power = False
        calculate_sa = False
        calculate_mga = False
        
        try:
            execute_ptr(mk, ptr_content, calculate_power, calculate_sa, calculate_mga)
            self.hide()
        except ValueError as error:
            QMessageBox.warning(self, 'PTR editor',
                                'PTR not valid ' + str(error))

    def browse_mk(self):
        default_folder = self.settings.get(self.mission, last_repo_key, '')
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
                                'PTR not valid ' + error)
            return None
        return ptr_content

    def clean_ptr(self):
        content = """
<prm>
<body>
    <segment>
    <data>
        <timeline frame="SC">
              <!-- Block (303) -->
               <block ref="OBS">
                  <startTime> 2032-12-26T10:15:31 </startTime>
                  <endTime> 2032-12-26T11:29:10 </endTime>
                  <attitude ref="track">
                     <boresight ref="SC_Zaxis" />
                     <phaseAngle ref="powerOptimised">
                        <yDir> false </yDir>
                        <angle units="deg"> 90 </angle>
                     </phaseAngle>
                     <target ref="Jupiter" />
                  </attitude>
                  <metadata>
                     <planning>
                        <observations designer="SWI">
                           <observation>
                              <type>DESIGNER</type>
                              <definition>SWI_2D_MAP_OTF_V1_38</definition>
                              <unit>SWI</unit>
                              <target>planet.jupiter</target>
                              <startDelta>+00:00:00</startDelta>
                              <endDelta>+00:00:00</endDelta>
                              <startTime>2032-12-26T10:15:31</startTime>
                              <endTime>2032-12-26T11:29:10</endTime>
                           </observation>
                        </observations>
                     </planning>
                  </metadata>
               </block>

               <!-- Block (304) -->
               <block ref="SLEW" />

               <!-- Block (305) -->
               <block ref="OBS">
                  <startTime> 2032-12-26T11:36:23 </startTime>
                  <endTime> 2032-12-26T12:09:18 </endTime>
                  <attitude ref="inertial">
                     <boresight ref="JUICE_UVS_Xaxis" />
                     <phaseAngle ref="align">
                        <SCAxis frame="SC">
                           <x> 1 </x>
                           <y> 0 </y>
                           <z> 0 </z>
                        </SCAxis>
                        <inertialAxis ref="rotate">
                           <axis ref="JP2Sun" />
                           <rotationAxis ref="SC2JP" />
                           <rotationAngle units="deg"> 180 </rotationAngle>
                        </inertialAxis>
                     </phaseAngle>
                     <target frame="EME2000">
                        <lon units="deg"> 235.671 </lon>
                        <lat units="deg"> -34.7104 </lat>
                     </target>
                  </attitude>
                  <metadata>
                       <comment> Occultation of Jupiter by HD140008 </comment>
                     <planning>
                        <observations designer="UVS">
                           <observation>
                              <type>DESIGNER</type>
                              <definition>UVS_JUP_AP_STELL_OCC</definition>
                              <unit>UVS</unit>
                              <target>planet.jupiter</target>
                              <startDelta>+00:00:00</startDelta>
                              <endDelta>+00:00:00</endDelta>
                              <startTime>2032-12-26T11:31:23</startTime>
                              <endTime>2032-12-26T12:13:18</endTime>
                           </observation>
                        </observations>
                     </planning>
                  </metadata>
               </block>

               <!-- Block (306) -->
               <block ref="SLEW" />

               <!-- Block (307) -->
               <block ref="OBS">
                  <startTime> 2032-12-26T12:15:31 </startTime>
                  <endTime> 2032-12-26T12:41:31 </endTime>
                  <attitude ref="track">
                     <boresight ref="SC_Zaxis" />
                     <phaseAngle ref="powerOptimised">
                        <yDir> false </yDir>
                        <angle units="deg"> 90 </angle>
                     </phaseAngle>
                     <target ref="Jupiter" />
                  </attitude>
                  <metadata>
                     <planning>
                        <observations designer="SWI">
                           <observation>
                              <type>DESIGNER</type>
                              <definition>SWI_NADIR_STARE_FS_V1_14</definition>
                              <unit>SWI</unit>
                              <target>planet.jupiter</target>
                              <startDelta>+00:00:00</startDelta>
                              <endDelta>+00:00:00</endDelta>
                              <startTime>2032-12-26T12:15:31</startTime>
                              <endTime>2032-12-26T12:41:31</endTime>
                           </observation>
                        </observations>
                     </planning>
                  </metadata>
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
