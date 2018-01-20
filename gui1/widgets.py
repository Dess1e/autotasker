from PyQt5.QtGui import QDropEvent
from PyQt5.QtWidgets import (QWidget, QListWidget, QComboBox, QToolButton, QGridLayout, QBoxLayout, QPushButton,
                             QTextEdit, QLineEdit, QCheckBox)


class DialogWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.doneButton = QPushButton(self)
        self.cancelButton = QPushButton(self)
        self.setGeometry(300, 300, 300, 300)
        self.init()

    def init(self):
        self.doneButton.setText('Done')
        self.cancelButton.setText('Cancel')


class DialogTimer(DialogWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setLayout(QGridLayout())
        self.timeLine = QLineEdit(self)
        self.setWindowTitle('Select timer properties')
        self.layout().addWidget(self.timeLine, 0, 0)
        self.layout().addWidget(self.doneButton, 1, 0)
        f = lambda: self.parent.pushDialogKwargs(self.makeKwargs())
        f_c = lambda: self.parent.pushDialogKwargs({'ABORT': None})
        self.doneButton.clicked.connect(f)
        self.cancelButton.clicked.connect(f_c)
        self.show()

    def makeKwargs(self):
        kwargs = {'time': self.timeLine.text()}
        return kwargs


class DialogAlerter(DialogWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setLayout(QGridLayout())
        self.textLine = QLineEdit(self)
        self.setWindowTitle('Select alert message properties')
        self.layout().addWidget(self.textLine, 0, 0)
        self.layout().addWidget(self.doneButton, 1, 0)
        f = lambda: self.parent.pushDialogKwargs(self.makeKwargs())
        f_c = lambda: self.parent.pushDialogKwargs({'ABORT': None})
        self.doneButton.clicked.connect(f)
        self.cancelButton.clicked.connect(f_c)
        self.show()

    def makeKwargs(self):
        kwargs = {'text': self.textLine.text()}
        return kwargs


class ListEntry:
    def __init__(self, name, id):
        self.name = name
        self.id = id
        self.descr = ''''''

    def __lt__(self, other):
        return self.id < other.id


class ListWidget(QListWidget):
    def __init__(self):
        super().__init__()
        self.initList()
        self.entries = []
        self.entries_count = 0

    def initList(self):
        from PyQt5.QtWidgets import QAbstractItemView
        self.setDragDropMode(QAbstractItemView.InternalMove)

    def getListElems(self):
        return self.entries

    def addListEntry(self, name):
        print('arg repr: {}'.format(name))
        self.entries.append(ListEntry(name, self.entries_count))
        self.entries_count += 1
        self._updateList()

    def removeListEntry(self, index):
        del self.entries[index]
        self.entries_count -= 1
        self._updateList()

    def _updateList(self):
        print('update list called')
        self.clear()
        for e in self.entries:
            self.addItem(e.name + '[{}]'.format(str(e.id)))

    def dropEvent(self, dropEvent: QDropEvent):
        print('overrided dropevent called')


class InfoBox(QTextEdit):
    def __init__(self):
        super().__init__()
        self.init()

    def init(self):
        self.setText("Info will be displayed here...")
        self.setReadOnly(True)


class Tools(QWidget):
    def __init__(self):
        super().__init__()
        self.setLayout(QBoxLayout(QBoxLayout.LeftToRight))
        self.addActionButton = AddButton(self)
        self.removeActionButton = RemoveButton(self)
        self.toolsCombo = ToolsCombobox(self)
        self.checkbox = CheckBox(self)
        self.init()

    def init(self):
        self.layout().addWidget(self.addActionButton)
        self.layout().addWidget(self.removeActionButton)
        self.layout().addWidget(self.toolsCombo)
        self.layout().addWidget(self.checkbox)


class ToolsCombobox(QComboBox):
    def __init__(self, parent):
        super().__init__(parent)
        self.initCombobox()

    def initCombobox(self):
        self.addItem('Select action...')
        self.addItem('Alert message')
        self.addItem('Timer / Sleep')
        self.addItem('Click at coords')

    def getSelectedData(self):
        return self.currentIndex(), self.currentText()


class AddButton(QToolButton):
    def __init__(self, parent):
        super().__init__(parent)
        self.initButton()

    def initButton(self):
        self.setText('Add action')


class RemoveButton(QToolButton):
    def __init__(self, parent):
        super().__init__(parent)
        self.initButton()

    def initButton(self):
        self.setText('Remove action')


class CheckBox(QCheckBox):
    def __init__(self, parent):
        super().__init__(parent)
        self.initCheckBox()

    def initCheckBox(self):
        self.setText('Enable')
