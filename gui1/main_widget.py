from PyQt5.QtCore import (pyqtSlot, Qt)
from PyQt5.QtWidgets import (QWidget, QMessageBox)

from handler.TaskHandler import TasksHandler
from gui1.widgets import DialogAlerter, DialogTimer
from gui1.layouts import MainLayout
from gui1.widgets import ListWidget, Tools, InfoBox


class MainWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('unnamed')
        self.TaskWidgetMap = {1: DialogAlerter, 2: DialogTimer}
        self.layout_ = MainLayout()
        self.setLayout(self.layout_)
        self.taskList = ListWidget()
        self.toolsBox = Tools()
        self.infoBox = InfoBox()
        self.msgBox = QMessageBox()
        self.taskHandlerThread = None
        self.lastTask = None
        self.lastDialogWindow = None
        self.initUI()
        self.initSignals()
        self.initHandlerThread()

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

    def initHandlerThread(self):
        self.taskHandlerThread = TasksHandler(self)
        self.taskHandlerThread.start()

    @pyqtSlot()
    def onAddButtonClicked(self):
        comboData = self.toolsBox.toolsCombo.getSelectedData()
        taskId, taskName = comboData
        if not taskId:
            return
        self.lastTask = (taskId, taskName)
        self.startDialogWidget(taskId)

    def startDialogWidget(self, taskId):
        cls = self.TaskWidgetMap[taskId]
        self.lastDialogWindow = cls(self)

    def pushDialogKwargs(self, kwargs):
        if 'ABORT' in kwargs:
            self.lastDialogWindow.close()
            self.lastDialogWindow = None
            return
        self.taskHandlerThread.add_task(self.lastTask[0], kwargs)
        self.taskList.addListEntry(self.lastTask[1])
        if self.lastDialogWindow:
            self.lastDialogWindow.close()
            self.lastDialogWindow = None

    @pyqtSlot()
    def onRemoveButtonClicked(self):
        index = self.taskList.currentRow()
        self.taskHandlerThread.remove_task(index)
        self.taskList.removeListEntry(index)

    @pyqtSlot()
    def onCheckBoxChange(self):
        boxstate = self.toolsBox.checkbox.isChecked()
        self.taskHandlerThread.isEnabled = boxstate

    @pyqtSlot(str)
    def showMessageBox(self, text):
        self.msgBox.setText(text)
        self.msgBox.setWindowTitle('Alert')
        self.setWindowFlag(Qt.Window)
        self.msgBox.setGeometry(200, 100, 100, 100)
        self.msgBox.show()
