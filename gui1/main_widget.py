from PyQt5.QtCore import (pyqtSlot, pyqtSignal, Qt)
from PyQt5.QtWidgets import (QWidget, QMessageBox)

from gui1.dialogs import (DialogAlerter, DialogTimer, DialogClicker, DialogFindAndClick,
                          DialogFindOnScreen, DialogPressKey, DialogHoldKey, DialogReleaseKey)
from gui1.layouts import MainLayout
from gui1.widgets import ListWidget, Tools, InfoBox
from helpers.helpers import randomId


class MainWidget(QWidget):
    """
    Widget class for main window
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle('unnamed')
        # Some kind of enumeration to add tasks to TaskHandler by index
        self.TaskWidgetMap = {1: DialogAlerter, 2: DialogTimer, 3: DialogClicker,
                              4: DialogFindAndClick, 5: DialogFindOnScreen, 6: DialogPressKey,
                              7: DialogHoldKey, 8: DialogReleaseKey}
        self.layout_ = MainLayout()
        self.setLayout(self.layout_)
        self.taskList = ListWidget()
        self.toolsBox = Tools()
        self.infoBox = InfoBox()  # info about tasks
        self.msgBox = QMessageBox()  # alert msg box
        self.lastTask = None
        self.lastDialogWindow = None
        self.initUI()
        self.initSignals()
        self.taskhandler_ref = None  # ptr to task handler obj

    def initUI(self):
        self.layout_.addWidget(self.toolsBox, 0, 0)
        self.layout_.addWidget(self.taskList, 1, 0)
        self.layout_.addWidget(self.infoBox, 1, 1)
        self.setGeometry(100, 100, 1024, 768)
        self.show()

    def initSignals(self):
        self.toolsBox.addActionButton.clicked.connect(self.onAddButtonClicked)
        self.toolsBox.removeActionButton.clicked.connect(self.onRemoveButtonClicked)
        self.toolsBox.checkbox.clicked.connect(self.onCheckBoxChange)

    def onAddButtonClicked(self):
        comboData = self.toolsBox.toolsCombo.getSelectedData()
        taskId, taskName = comboData
        if not taskId:
            return
        self.lastTask = (taskId, taskName)
        self.startDialogWidget(taskId)

    def startDialogWidget(self, taskId):
        cls = self.TaskWidgetMap[taskId]  # task class
        self.lastDialogWindow = cls(parent=self)

    def pushDialogKwargs(self, kwargs):
        """
        Gets data from dialog and adds tasks to task handler
        """
        if not kwargs:
            self.lastDialogWindow.close()
            self.lastDialogWindow = None
            return
        entries = self.taskList.getEntries()
        while True:
            newId = randomId(6)
            if newId not in entries:
                break
        self.taskhandler_ref.add_task(self.lastTask[0], newId, kwargs)
        self.taskList.addListEntry(self.lastTask[1], newId)
        if self.lastDialogWindow:
            self.lastDialogWindow.close()
            self.lastDialogWindow = None

    def onRemoveButtonClicked(self):
        self.taskList.removeCurrentListEntry()

    def onCheckBoxChange(self):
        boxstate = self.toolsBox.checkbox.isChecked()
        print(boxstate)
        self.taskhandler_ref.isEnabled = bool(boxstate)

    @pyqtSlot(str)
    def showMessageBox(self, text):
        """
        Method to pop up msgbox (self.msgbox)
        """
        self.msgBox.setText(text)
        self.msgBox.setWindowTitle('Alert')
        self.setWindowFlag(Qt.Window)
        self.msgBox.setGeometry(200, 100, 100, 100)
        self.msgBox.show()
