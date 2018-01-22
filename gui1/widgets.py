from PyQt5.QtGui import QDropEvent
from PyQt5.QtWidgets import (QWidget, QListWidget, QComboBox, QToolButton, QGridLayout, QBoxLayout, QPushButton,
                             QTextEdit, QLineEdit, QCheckBox)
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from helpers.helpers import DescriptionMap


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
        self.layout().addWidget(self.timeLine, 0, 0, 1, 2)
        self.layout().addWidget(self.doneButton, 1, 0)
        self.layout().addWidget(self.cancelButton, 1, 1)
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
        self.layout().addWidget(self.textLine, 0, 0, 1, 2)
        self.layout().addWidget(self.doneButton, 1, 0)
        self.layout().addWidget(self.cancelButton, 1, 1)
        f = lambda: self.parent.pushDialogKwargs(self.makeKwargs())
        f_c = lambda: self.parent.pushDialogKwargs({'ABORT': None})
        self.doneButton.clicked.connect(f)
        self.cancelButton.clicked.connect(f_c)
        self.show()

    def makeKwargs(self):
        kwargs = {'text': self.textLine.text()}
        return kwargs


class DialogClicker(DialogWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setLayout(QGridLayout())
        self.xline = QLineEdit(self)
        self.yline = QLineEdit(self)
        self.setWindowTitle('Select clicker properies')
        self.layout().addWidget(self.xline, 0, 0)
        self.layout().addWidget(self.yline, 0, 1)
        self.layout().addWidget(self.doneButton, 1, 0)
        self.layout().addWidget(self.cancelButton, 1, 1)
        f = lambda: self.parent.pushDialogKwargs(self.makeKwargs())
        f_c = lambda: self.parent.pushDialogKwargs({'ABORT': None})
        self.doneButton.clicked.connect(f)
        self.cancelButton.clicked.connect(f_c)
        self.show()

    def makeKwargs(self):
        kwargs = {'x': self.xline.text(), 'y': self.yline.text()}
        return kwargs


class ListEntry:
    def __init__(self, name, uniqueId):
        self.name = name
        self.uid = uniqueId
        self.descr = ''''''

    def __repr__(self):
        return '<ListEntry #{} ({})>'.format(self.uid, self.name)


class ListWidget(QListWidget):
    requestInfoUpdateSig = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.initList()
        self.entries = {}
        self.order = []
        self.taskhandler_ref = None

    def initList(self):
        from PyQt5.QtWidgets import QAbstractItemView
        self.setDragDropMode(QAbstractItemView.InternalMove)
        self.setDragDropOverwriteMode(False)
        self.setDragEnabled(True)

        self.currentRowChanged.connect(self.onEntryClick)

    def getEntries(self):
        return self.entries

    def _getListElems(self) -> list:
        lst = []
        for i in range(self.count()):
            lst.append(self.item(i))
        return lst

    def addListEntry(self, name, uniqueId):
        self.entries[uniqueId] = ListEntry(name, uniqueId)
        self.order.append(uniqueId)
        self._updateList()

    def removeCurrentListEntry(self):
        selected_entry = self.currentItem()
        if selected_entry:
            curr_id = selected_entry.text()[-7:-1]
            del self.entries[curr_id]
            self.order.remove(curr_id)
            self._updateList()
            self.taskhandler_ref.remove_task(curr_id)

    def getCurrElemUid(self):
        elem = self.currentItem()
        if elem:
            return elem.text()[-7:-1]
        else:
            return None

    def _updateList(self):
        self.clear()
        order = self.order
        for uid in order:
            curr = self.entries[uid]
            self.addItem(curr.name + '[{}]'.format(str(curr.uid)))

    def getUpdatedOrder(self) -> list:
        order = [e.text()[-7:-1] for e in self._getListElems()]
        return order

    def dropEvent(self, dropEvent: QDropEvent):
        super().dropEvent(dropEvent)
        order = self.getUpdatedOrder()
        self.taskhandler_ref.reorder(order)

    def onEntryClick(self):
        self.requestInfoUpdateSig.emit(self.getCurrElemUid())


class InfoBox(QTextEdit):
    def __init__(self):
        super().__init__()
        self.taskhandler_ref = None
        self.desc_map = DescriptionMap()
        self.init()

    def init(self):
        self.setText("Info will be displayed here...")
        self.setReadOnly(True)

    @pyqtSlot(str)
    def updateInfo(self, uid):
        d = self.desc_map.createDescription(self.taskhandler_ref.getTask(uid), uid)
        self.setText(d)


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
