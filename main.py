from gui1.main_widget import MainWidget
from PyQt5.QtWidgets import QApplication
import sys
from handler.TaskHandler import TasksHandler
from PyQt5.QtCore import pyqtSlot


class Application(QApplication):
    def __init__(self, args):
        super().__init__(args)
        self.gui = MainWidget()
        self.taskhandler = None
        self.initSignals()
        self.initTaskHandler()

    def initTaskHandler(self):
        self.taskhandler = TasksHandler(self.gui)
        self.taskhandler.start()

    def initSignals(self):
        self.gui.pushkwargsSig.connect(self.pushArgsFromDialog)
        self.gui.removeactionSig.connect(self.removeAction)
        self.gui.checkboxSig.connect(self.toggleHandler)

    @pyqtSlot(tuple, dict)
    def pushArgsFromDialog(self, lastTask, kwargs):
        self.taskhandler.add_task(lastTask[0], kwargs)

    @pyqtSlot(int)
    def removeAction(self, index):
        self.taskhandler.remove_task(index)

    @pyqtSlot(bool)
    def toggleHandler(self, state):
        self.taskhandler.isEnabled = state

if __name__ == '__main__':
    app = Application(sys.argv)
    sys.exit(app.exec_())
