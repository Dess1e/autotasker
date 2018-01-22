from gui1.main_widget import MainWidget
from PyQt5.QtWidgets import QApplication
from handler.TaskHandler import TasksHandler
from PyQt5.QtCore import pyqtSlot, QT_VERSION, qFatal
import sys, traceback


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
        self.gui.taskList.removeactionSig.connect(self.removeAction)
        self.gui.checkboxSig.connect(self.toggleHandler)
        self.gui.taskList.dropeventSig.connect(self.listReorder)

    @pyqtSlot(tuple, str, dict)
    def pushArgsFromDialog(self, lastTask, uid, kwargs):
        self.taskhandler.add_task(lastTask[0], uid, kwargs)

    @pyqtSlot(str)
    def removeAction(self, uid):
        self.taskhandler.remove_task(uid)

    @pyqtSlot(bool)
    def toggleHandler(self, state):
        self.taskhandler.isEnabled = state

    @pyqtSlot(list)
    def listReorder(self, order):
        self.taskhandler.reorder(order)

if __name__ == '__main__':
    if QT_VERSION >= 0x50501:
        def excepthook(type_, value, traceback_):
            traceback.print_exception(type_, value, traceback_)
            qFatal('')
        sys.excepthook = excepthook

    app = Application(sys.argv)
    sys.exit(app.exec_())
