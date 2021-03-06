import logging
import sys
import traceback

from PyQt5.QtCore import QT_VERSION, qFatal
from PyQt5.QtWidgets import QApplication

from gui1.main_widget import MainWidget
from handlers.TaskHandler import TaskHandlerThread

logging.basicConfig(format="%(filename)-15s [line:%(lineno)s] ::%(levelname)-8s:: %(message)s",
                    level=logging.DEBUG)


class Application(QApplication):
    def __init__(self, args):
        super().__init__(args)
        self.gui = MainWidget()
        self.taskhandler = None
        self.taskhandler_thr = None
        self.initSignals()
        self.initTaskHandler()
        self.passTaskHandlerRef()

    def initTaskHandler(self):
        self.taskhandler_thr = TaskHandlerThread(self.gui)
        self.taskhandler_thr.start()
        self.taskhandler = self.taskhandler_thr.taskhandler

    def passTaskHandlerRef(self):
        self.gui.taskList.taskhandler_ref = self.taskhandler
        self.gui.infoBox.taskhandler_ref = self.taskhandler
        self.gui.taskhandler_ref = self.taskhandler

    def initSignals(self):
        self.gui.taskList.requestInfoUpdateSig.connect(self.gui.infoBox.updateInfo)


if __name__ == '__main__':
    if QT_VERSION >= 0x50501:
        def excepthook(type_, value, traceback_):
            traceback.print_exception(type_, value, traceback_)
            qFatal('')
        sys.excepthook = excepthook

    app = Application(sys.argv)
    sys.exit(app.exec_())
