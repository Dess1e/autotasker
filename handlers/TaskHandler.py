from abc import abstractmethod
from time import time

import pyautogui
from PyQt5.QtCore import pyqtSignal, QObject, QThread

from handlers import cv2handler as cv2


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
        self.tasks = {}  # tasks are in map (uid: taskobj)
        self.order = []  # this is the map order (are py dicts ordered??)
        self.isEnabled = False  # enable switch
        self.TaskMap = {1: Alerter, 2: Timer, 3: Clicker, 4: FindAndClick,
                        5: FindOnScreen, 6: PressKeyOnce, 7: HoldKey,
                        8: ReleaseKey}  # same enum is present in main.py

    def add_task(self, taskId, uid, kwargs):
        cls = self.TaskMap[taskId]
        newTask = cls(self.guiRef, kwargs)
        newTask.setID(uid)
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
        self.taskInfo = ""
        self.__description = ""
        self.id = None

    @abstractmethod
    def perform(self):
        pass

    @abstractmethod
    def getDescription(self):
        pass

    def setID(self, id):
        self.id = id

    def getID(self):
        return self.id


class Timer(Task):
    def __init__(self, guiRef, kwargs):
        super().__init__(guiRef, kwargs)
        self.sleep_time = kwargs['time']
        self.__description = """
                    This is Timer task. It will delay the execution of next task by selected time.
                    Task UID: {}
                    Time delay: {}
        """

    def perform(self):
        stop_time = int(time()) + int(self.sleep_time)
        while int(time()) != stop_time:
            pass
        return

    def getDescription(self):
        return self.__description.format(self.id, self.sleep_time)


class Clicker(Task):
    def __init__(self, guiRef, kwargs):
        super().__init__(guiRef, kwargs)
        self.coords = (self.kwargs['x'], self.kwargs['y'])
        self.__description = """
                    This is Clicker task. It will click at selected coordinates.
                    Task UID: {}
                    X-Coordinate: {}
                    Y-Coordinate: {}
        """

    def perform(self):
        pyautogui.click(self.coords[0], self.coords[1])

    def getDescription(self):
        return self.__description.format(self.id, *self.coords)


class Alerter(Task):
    calledPerform = pyqtSignal(str)

    def __init__(self, guiRef, kwargs):
        super().__init__(guiRef, kwargs)
        self.alertText = self.kwargs['text']
        self.calledPerform.connect(self.guiRef.showMessageBox)
        self.__description = """
                    This is Alerter task. It will Alert you by popping up alert box with selected message.
                    Task UID: {}
                    Alert message: {}
        """

    def perform(self):
        self.showMsgBox(self.alertText)

    def showMsgBox(self, text):
        self.calledPerform.emit(text)

    def getDescription(self):
        return self.__description.format(self.id, self.alertText)


class FindAndClick(Task):
    def __init__(self, guiRef, kwargs):
        super().__init__(guiRef, kwargs)
        self.imgPath = kwargs['path']
        self.isContinious = kwargs['continueIfNotFound']
        self.imgData = cv2.readImage(self.imgPath)
        self.__description = """
                    Andrey napishi description!
                    Task UID: {}
                    Path: {}
        """

    def perform(self):
        if self.isContinious:
            screenshot = cv2.makeScreenshot()
            coords = cv2.matchAndGetCoords(self.imgData, screenshot)
            if coords:
                pyautogui.click(coords[0], coords[1])
                print('found clicking')
            else:
                print('not found exiting')
                return
        else:
            while True:
                screenshot = cv2.makeScreenshot()
                coords = cv2.matchAndGetCoords(self.imgData, screenshot)
                if coords:
                    pyautogui.click(coords[0], coords[1])
                    print('found clicking exiting [loop]')
                    return
                print('not found still searching[loop]')

    def getDescription(self):
        return self.__description.format(self.id, self.imgPath)


class FindOnScreen(Task):
    def __init__(self, guiRef, kwargs):
        super().__init__(guiRef, kwargs)
        self.imgPath = kwargs['path']
        self.imgData = cv2.readImage(self.imgPath)
        self.__description = """
                    Andrey napishi description!
                    Task UID: {}
                    Path: {}
        """

    def perform(self):
        while True:
            screenshot = cv2.makeScreenshot()
            coords = cv2.matchAndGetCoords(self.imgData, screenshot)
            if coords:
                return

    def getDescription(self):
        return self.__description.format(self.id, self.imgPath)


class PressKeyOnce(Task):
    def __init__(self, guiRef, kwargs):
        super().__init__(guiRef, kwargs)
        self.key = kwargs['key']
        self.__description = """
                    Andrey napishi description!
                    Task UID: {}
                    Key: {}
        """

    def perform(self):
        pyautogui.press(self.key)

    def getDescription(self):
        return self.__description.format(self.id, self.key)


class HoldKey(Task):
    def __init__(self, guiRef, kwargs):
        super().__init__(guiRef, kwargs)
        self.key = kwargs['key']
        self.__description = """
                    Andrey napishi description!
                    Task UID: {}
                    Key: {}
        """

    def perform(self):
        pyautogui.keyDown(self.key)

    def getDescription(self):
        return self.__description.format(self.id, self.key)


class ReleaseKey(Task):
    def __init__(self, guiRef, kwargs):
        super().__init__(guiRef, kwargs)
        self.key = kwargs['key']
        self.__description = """
                    Andrey napishi description!
                    Task UID: {}
                    Key: {}
        """

    def perform(self):
        pyautogui.keyUp(self.key)

    def getDescription(self):
        return self.__description.format(self.id, self.key)
