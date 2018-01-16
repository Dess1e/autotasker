from PyQt5.QtWidgets import (QWidget, QListWidget, QComboBox, QToolButton, QGridLayout, QBoxLayout, QPushButton,
                             QTextEdit, QLineEdit, QCheckBox, QMessageBox)
from PyQt5.QtCore import pyqtSlot
from TaskHandler import TasksHandler
from PyQt5.QtCore import Qt


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
        self.taskList.addItem(self.lastTask[1])
        if self.lastDialogWindow:
            self.lastDialogWindow.close()
            self.lastDialogWindow = None

    @pyqtSlot()
    def onRemoveButtonClicked(self):
        index = self.taskList.currentRow()
        self.taskHandlerThread.remove_task(index)
        self.taskList.takeItem(index)

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


class MainLayout(QGridLayout):
    def __init__(self):
        super().__init__()
        self.initLayout()

    def initLayout(self):
        pass


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


class ListWidget(QListWidget):
    def __init__(self):
        super().__init__()
        self.initList()

    def initList(self):
        pass

    def addAction(self, name):
        self.addItem(name)


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
