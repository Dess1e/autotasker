from PyQt5.QtCore import (pyqtSlot, Qt)
from PyQt5.QtWidgets import (QWidget, QMessageBox, QGridLayout)

from gui1.widgets import Tools, InfoBox, ListWidget
from helpers.helpers import randomId


class MainWidget(QWidget):
    """
    Widget class for main window
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Autotasker228')
        self.setLayout(QGridLayout(self))
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
        self.layout().addWidget(self.toolBox, 0, 0, 1, 2)
        self.layout().addWidget(self.taskList, 1, 0)
        self.layout().addWidget(self.infoBox, 1, 1)
        self.setGeometry(100, 100, 1024, 768)
        self.show()

    def initSignals(self):
        self.toolBox.removeActionButton.clicked.connect(self.onRemoveButtonClicked)
        self.toolBox.checkbox.clicked.connect(self.onCheckBoxChange)

    def addTask(self, taskCls, taskDialog):
        self.lastTask = taskCls
        self.lastDialogWindow = taskDialog(parent=self)

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
