from PyQt5.QtCore import (pyqtSlot, Qt)
from PyQt5.QtWidgets import (QWidget, QMessageBox, QGridLayout)

# from gui1.dialogs import (DialogAlerter, DialogTimer, DialogClicker,
#                           DialogFindAndClick, DialogFindOnScreen,
#                           DialogPressKey, DialogHoldKey, DialogReleaseKey)
from gui1.widgets import Tools, InfoBox, ListWidget
from helpers.helpers import randomId


class MainWidget(QWidget):
    """
    Widget class for main window
    """
    def __init__(self):
        super().__init__()
        # Some kind of enumeration to add tasks to TaskHandler by index
        # self.TaskWidgetMap = {1: DialogAlerter, 2: DialogTimer, 3: DialogClicker,
        #                       4: DialogFindAndClick, 5: DialogFindOnScreen, 6: DialogPressKey,
        #                       7: DialogHoldKey, 8: DialogReleaseKey}
        self.setWindowTitle('Autotasker228')
        self.layout_ = QGridLayout()
        self.setLayout(self.layout_)
        self.taskList = ListWidget()
        self.toolBox = Tools(parent=self)
        self.infoBox = InfoBox()  # info about tasks
        self.msgBox = QMessageBox()  # alert msg box
        self.lastTask = None
        self.lastDialogWindow = None
        self.initUI()
        self.initSignals()
        self.taskhandler_ref = None  # ptr to task handler obj

    def initUI(self):
        self.layout_.addWidget(self.toolBox, 0, 0)
        self.layout_.addWidget(self.taskList, 1, 0)
        self.layout_.addWidget(self.infoBox, 1, 1, 1, 2)
        self.setGeometry(100, 100, 1024, 768)
        self.show()

    def initSignals(self):
        # self.toolBox.addActionButton.clicked.connect(self.onAddButtonClicked)
        self.toolBox.removeActionButton.clicked.connect(self.onRemoveButtonClicked)
        self.toolBox.checkbox.clicked.connect(self.onCheckBoxChange)

    def addTask(self, taskCls, taskDialog):
        self.lastTask = taskCls
        self.lastDialogWindow = taskDialog(parent=self)

    # def onAddButtonClicked(self):
    #     comboData = self.toolBox.toolsCombo.getSelectedData()
    #     taskId, taskName = comboData
    #     if not taskId:
    #         return
    #     self.lastTask = (taskId, taskName)
    #     self.startDialogWidget(taskId)

    # def startDialogWidget(self, taskId):
    #     cls = self.TaskWidgetMap[taskId]  # task class
    #     self.lastDialogWindow = cls(parent=self)

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
        self.taskhandler_ref.add_task(self.lastTask, newId, kwargs)
        self.taskList.addListEntry(self.lastTask.__name__, newId)
        if self.lastDialogWindow:
            self.lastDialogWindow.close()
            self.lastDialogWindow = None

    def onRemoveButtonClicked(self):
        self.taskList.removeCurrentListEntry()

    def onCheckBoxChange(self):
        boxstate = self.toolBox.checkbox.isChecked()
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
