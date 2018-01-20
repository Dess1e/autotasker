from PyQt5.QtCore import pyqtSignal, QObject, QThread
from time import time
import pyautogui


def trap_exception(*args):
    print(args)


class TasksHandler(QThread):
    def __init__(self, guiRef):
        super().__init__()
        self.guiRef = guiRef
        self.tasks = []
        self.isEnabled = False
        self.TaskMap = {1: Alerter, 2: Timer, 3: Clicker}

    def add_task(self, taskId, kwargs):
        cls = self.TaskMap[taskId]
        newTask = cls(self.guiRef, kwargs)
        self.tasks.append(newTask)

    def remove_task(self, index):
        del self.tasks[index]

    def run(self):
        self.mainloop()

    def mainloop(self):
        while True:
            tasks = self.tasks
            if len(tasks) and self.isEnabled:
                print(self.tasks)
                for each in tasks:
                    each.perform()


class Task(QObject):
    def __init__(self, guiRef, kwargs):
        super().__init__()
        self.taskInfo = ''''''
        self.guiRef = guiRef
        self.kwargs = kwargs

    def perform(self):
        pass


class Timer(Task):
    def __init__(self, guiRef, kwargs):
        super().__init__(guiRef, kwargs)
        print(kwargs)
        self.sleep_time = kwargs['time']

    def perform(self):
        stop_time = int(time()) + int(self.sleep_time)
        while int(time()) != stop_time:
            pass
        return


class Clicker(Task):
    def __init__(self, guiRef, kwargs):
        super().__init__(guiRef, kwargs)
        self.coords = (self.kwargs['x'], self.kwargs['y'])

    def perform(self):
        pyautogui.click(self.coords[0], self.coords[1])


class Alerter(Task):
    calledPerform = pyqtSignal(str)

    def __init__(self, guiRef, kwargs):
        super().__init__(guiRef, kwargs)
        self.alertText = self.kwargs['text']
        self.calledPerform.connect(self.guiRef.showMessageBox)

    def perform(self):
        self.showMsgBox(self.alertText)

    def showMsgBox(self, text):
        self.calledPerform.emit(text)
