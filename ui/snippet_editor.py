from PyQt5.QtWidgets import QPlainTextEdit, QCompleter
from PyQt5.QtCore import QStringListModel, Qt, QTimer



SNIPPETS = {
    "base": """<prm>
<body>
    <segment>
    <data>
        <timeline frame="SC">
        </timeline>
    </data>    
    </segment>    
</body>
</prm>""",

    "track": """
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
               </block>
""",
    "slew": """
               <block ref="SLEW" />
"""
}

class SnippetTextEdit(QPlainTextEdit):
    def __init__(self, parent=None, snippets=SNIPPETS):
        super().__init__(parent)
        self.snippets = snippets

        model = QStringListModel(list(snippets.keys()))
        self.completer = QCompleter(model, self)
        self.completer.snippet_model = model
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.completer.setCompletionMode(QCompleter.PopupCompletion)
        self.completer.activated.connect(self.insert_completion)
        self.completer.setWidget(self)

    def keyPressEvent(self, event):
        # Accept completion on Enter or Tab
        if self.completer.popup().isVisible() and event.key() in (Qt.Key_Return, Qt.Key_Enter, Qt.Key_Tab):
            index = self.completer.popup().currentIndex()
            if index.isValid():
                self.completer.activated.emit(index.data())
            self.completer.popup().hide()
            return  # Do not pass to base

        # Trigger completion on '@'
        super().keyPressEvent(event)
        if event.text() == "@":
            QTimer.singleShot(0,self.show_completer)

    def show_completer(self):
        cursor = self.textCursor()
        self.setFocus()
        popup = self.completer.popup()
        if popup.model().rowCount() > 0:
            popup.setCurrentIndex(popup.model().index(0, 0))

        rect = self.cursorRect(cursor)
        rect.setWidth(100)
        self.completer.complete(rect)

    def insert_completion(self, key):
        cursor = self.textCursor()
        cursor.movePosition(cursor.Left, cursor.KeepAnchor, 1)
        cursor.removeSelectedText()
        snippet = self.snippets.get(key, key)
        cursor.insertText(snippet)
