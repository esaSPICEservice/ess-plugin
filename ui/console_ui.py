from ui.common import get_settings, get_runtime

from PyQt5.QtWidgets import  QDialog, QMessageBox
from ui.design.console import Ui_consoleWidget
from settings.handler import last_expressions
from actions.time_navigation import evaluate, EvaluateException

class ConsoleDialog(QDialog):

    id = 'console_dialog_window_id'

    def __init__(self, main_window):
        QDialog.__init__(self, main_window)
        self.settings = get_settings()
        self.runtime = get_runtime()
        self.mission = self.runtime.get('mission')
        self.init_ui()

    def init_ui(self):
        self.setObjectName(ConsoleDialog.id)
        self.console_widget = Ui_consoleWidget()
        self.console_widget.setupUi(self)
        self.console_widget.runButton.clicked.connect(self.run)


    def run(self):
        expressions =  self.console_widget.expressionEditor.toPlainText()
       
        self.settings.set(self.mission, last_expressions, expressions)
        self.settings.save()
        
        try:
            evaluate(expressions)
            # self.hide()
        except EvaluateException as error:
            QMessageBox.warning(self, 'Expression editor',
                                str(error))


    def show_and_focus(self):
        expressions = self.settings.get(self.mission, last_expressions, '')
        self.console_widget.expressionEditor.setPlainText(expressions)

        self.hide()
        self.show()
