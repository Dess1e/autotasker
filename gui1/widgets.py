from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtGui import QDropEvent
from PyQt5.QtWidgets import (QWidget, QListWidget, QComboBox, QToolButton,
                             QBoxLayout, QLabel, QCheckBox)


class ListEntry:
    def __init__(self, name, uniqueId):
        self.name = name
        self.uid = uniqueId
        self.descr = ''''''

    def __repr__(self):
        return '<ListEntry #{} ({})>'.format(self.uid, self.name)  # the beautiful repr


class ListWidget(QListWidget):
    requestInfoUpdateSig = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.initList()
        self.entries = {}
        self.order = []  # tasks order
        self.taskhandler_ref = None  # task handler obj

    def initList(self):
        from PyQt5.QtWidgets import QAbstractItemView
        self.setDragDropMode(QAbstractItemView.InternalMove)
        self.setDragDropOverwriteMode(False)
        self.setDragEnabled(True)

        self.currentRowChanged.connect(self.onEntryClick)  # signal to change infobox

    def getEntries(self):
        return self.entries

    def _getListElems(self) -> list:  # priv function to get list of listview elems
        lst = []
        for i in range(self.count()):
            lst.append(self.item(i))
        return lst

    def addListEntry(self, name, uniqueId):
        self.entries[uniqueId] = ListEntry(name, uniqueId)
        self.order.append(uniqueId)
        self._updateList()

    def removeCurrentListEntry(self):  # removes selected lst entry
        selected_entry = self.currentItem()
        if selected_entry:
            curr_id = selected_entry.text()[-7:-1]  # format entry name to get entry id
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
            self.addItem(curr.name + ' [{}]'.format(str(curr.uid)))

    def getUpdatedOrder(self) -> list:
        order = [e.text()[-7:-1] for e in self._getListElems()]
        return order

    def dropEvent(self, dropEvent: QDropEvent):
        super().dropEvent(dropEvent)
        order = self.getUpdatedOrder()
        self.taskhandler_ref.reorder(order)

    def onEntryClick(self):
        self.requestInfoUpdateSig.emit(self.getCurrElemUid())


class InfoBox(QLabel):
    def __init__(self):
        super().__init__()
        self.taskhandler_ref = None
        # self.desc_map = DescriptionMap()
        self.default_text = 'Click task to show info...'
        self.init()

    def init(self):
        self.setText(self.default_text)

    @pyqtSlot(str)
    def updateInfo(self, uid):
        # d = self.desc_map.createDescription(self.taskhandler_ref.getTask(uid), uid)
        # if d:
        #     self.setText(d)
        # else:
        #     self.setText(self.default_text)
        task = self.taskhandler_ref.getTask(uid)
        description = task.getDescription()
        self.setText(description)


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
        self.addItem('Find on screen and click')
        self.addItem('Try to find on screen')
        self.addItem('Press key once')
        self.addItem('Hold key')
        self.addItem('Release key')

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
