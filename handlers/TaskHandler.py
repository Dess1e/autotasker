from PyQt5.QtCore import pyqtSignal, QObject, QThread
from time import time
from handlers import cv2handler as cv2
import pyautogui


class TaskHandlerThread(QThread):
    def __init__(self, guiRef):
        super().__init__()
        self.taskhandler = TasksHandler(guiRef)

    def run(self):
        self.taskhandler.mainloop()


class TasksHandler(QObject):
    def __init__(self, guiRef):
        super().__init__()
        self.guiRef = guiRef
        self.tasks = {}
        self.order = []
        self.isEnabled = False
        self.TaskMap = {1: Alerter, 2: Timer, 3: Clicker, 4: FindAndClick}

    def add_task(self, taskId, uid, kwargs):
        cls = self.TaskMap[taskId]
        newTask = cls(self.guiRef, kwargs)
        self.tasks[uid] = newTask
        self.order.append(uid)

    def remove_task(self, uid):
        del self.tasks[uid]
        self.order.remove(uid)

    def reorder(self, new_order):
        self.order = new_order

    def getTask(self, uid):
        if uid in self.tasks:
            return self.tasks[uid]
        else:
            return None

    def mainloop(self):
        while True:
            tasks = self.tasks
            if len(tasks) and self.isEnabled:
                for each in self.order:
                    self.tasks[each].perform()


class Task(QObject):
    def __init__(self, guiRef, kwargs):
        super().__init__()
        self.guiRef = guiRef
        self.kwargs = kwargs
        self.taskInfo = ''''''
        self.guiRef = guiRef
        self.kwargs = kwargs

    def perform(self):
        pass


class Timer(Task):
    def __init__(self, guiRef, kwargs):
        super().__init__(guiRef, kwargs)
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


class FindAndClick(Task):
    def __init__(self, guiRef, kwargs):
        super().__init__(guiRef, kwargs)
        self.imgPath = kwargs['path']
        self.isContinious = kwargs['continueIfNotFound']
        self.imgData = cv2.readImage(self.imgPath)

    def perform(self):
        screenshot = cv2.makeScreenshot()
        if self.isContinious:
            coords = cv2.matchAndGetCoords(self.imgData, screenshot)
            if coords:
                pyautogui.click(coords[0], coords[1])
                print('found clicking')
            else:
                print('not found exiting')
                return
        else:
            while True:
                coords = cv2.matchAndGetCoords(self.imgData, screenshot)
                if coords:
                    pyautogui.click(coords[0], coords[1])
                    print('found clicking exiting [loop]')
                    return
                print('not found still searching[loop]')
