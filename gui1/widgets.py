from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QDropEvent
from PyQt5.QtWidgets import (QListWidget, QComboBox, QToolButton,
                             QHBoxLayout)

from gui1.dialogs import *
from handlers.TaskHandler import *


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
        logging.debug(f"[ListWidget]: Deleting enty {selected_entry}")
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
        self.default_text = 'Click task to show info...'
        self.init()

    def init(self):
        self.setText(self.default_text)

    @pyqtSlot(str)
    def updateInfo(self, uid):
        task = self.taskhandler_ref.getTask(uid)
        if task:  # check that task exists
            description = task.getDescription()
            self.setText(description)
        else:
            self.setText(self.default_text)


class Tools(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        # self.parent = parent
        self.setLayout(QHBoxLayout())
        # self.addActionButton = QToolButton(self)
        self.removeActionButton = QToolButton(self)
        # self.toolsCombo = ToolsCombobox(self)
        self.checkbox = CheckBox(self)
        self.actions = {"Alert message": (Alerter, DialogAlerter),
                        "Timer / Sleep": (Timer, DialogTimer),
                        "Click at coords": (Clicker, DialogClicker),
                        "Find on screen and click": (FindAndClick, DialogFindAndClick),
                        "Try to find on screen": (FindOnScreen, DialogFindOnScreen),
                        "Press key once": (PressKeyOnce, DialogPressKey),
                        "Hold key": (HoldKey, DialogHoldKey),
                        "Release key": (ReleaseKey, DialogReleaseKey)}
        self.init()

    def init(self):
        # self.addActionButton.setText("Add Action")
        self.removeActionButton.setText("Remove Action")

        for actionName, action in self.actions.items():
            button = QToolButton(self)
            button.setText(actionName)
            button.clicked.connect(lambda a=action: self.parent().addTask(*a))
            self.layout().addWidget(button)

        # self.layout().addWidget(self.addActionButton)
        self.layout().addWidget(self.removeActionButton)
        # self.layout().addWidget(self.toolsCombo)
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


class CheckBox(QCheckBox):
    def __init__(self, parent):
        super().__init__(parent)
        self.initCheckBox()

    def initCheckBox(self):
        self.setText('Enable')
