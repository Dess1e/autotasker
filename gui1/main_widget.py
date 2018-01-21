from PyQt5.QtCore import (pyqtSlot, pyqtSignal, Qt)
from PyQt5.QtWidgets import (QWidget, QMessageBox)

from gui1.widgets import DialogAlerter, DialogTimer
from gui1.layouts import MainLayout
from gui1.widgets import ListWidget, Tools, InfoBox


class MainWidget(QWidget):
    pushkwargsSig = pyqtSignal(tuple, dict)
    removeactionSig = pyqtSignal(int)
    checkboxSig = pyqtSignal(bool)

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
        self.lastTask = None
        self.lastDialogWindow = None
        self.initUI()
        self.initSignals()

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
        self.pushkwargsSig.emit(self.lastTask, kwargs)
        if 'ABORT' in kwargs:
            self.lastDialogWindow.close()
            self.lastDialogWindow = None
            return
        self.taskList.addListEntry(self.lastTask[1])
        if self.lastDialogWindow:
            self.lastDialogWindow.close()
            self.lastDialogWindow = None

    def onRemoveButtonClicked(self):
        index = self.taskList.currentRow()
        self.removeactionSig.emit(index)
        self.taskList.removeListEntry(index)

    def onCheckBoxChange(self):
        boxstate = self.toolsBox.checkbox.isChecked()
        print(boxstate)
        self.checkboxSig.emit(bool(boxstate))

    @pyqtSlot(str)
    def showMessageBox(self, text):
        self.msgBox.setText(text)
        self.msgBox.setWindowTitle('Alert')
        self.setWindowFlag(Qt.Window)
        self.msgBox.setGeometry(200, 100, 100, 100)
        self.msgBox.show()
