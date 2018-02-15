import logging
from abc import abstractmethod
from time import time

import pyautogui
from PyQt5.QtCore import pyqtSignal, QObject, QThread

from handlers import cv2handler as cv2

logging.basicConfig(format="%(filename)s [line:%(lineno)s] :: %(levelname)-8s:: %(message)s",
                    level=logging.DEBUG)


class TaskHandlerThread(QThread):
    def __init__(self, guiRef):
        super().__init__()
        self.taskhandler = TaskHandler(guiRef)

    def run(self):
        self.taskhandler.mainloop()


class TaskHandler(QObject):
    def __init__(self, guiRef):
        super().__init__()
        logging.debug("[TaskHandler]: Initializing...")

        self.guiRef = guiRef
        self.tasks = {}  # tasks are in map (uid: taskobj)
        # self.order = []  # this is the map order (are py dicts ordered??)
        self.isEnabled = False  # enable switch
        self.TaskMap = {1: Alerter, 2: Timer, 3: Clicker, 4: FindAndClick,
                        5: FindOnScreen, 6: PressKeyOnce, 7: HoldKey,
                        8: ReleaseKey}  # same enum is present in main.py

        logging.debug("[TaskHandler]: Initialized...")

    def add_task(self, taskId, uid, kwargs):
        cls = self.TaskMap[taskId]
        newTask = cls(self.guiRef, kwargs)
        newTask.setID(uid)
        self.tasks[uid] = newTask

        logging.debug(f"[TaskHandler]: Added new {newTask} with id={uid}")
        logging.debug(f"[TaskHandler]: Internal stack dict:\n\t{self.tasks}")

    def remove_task(self, uid):
        task = self.tasks.pop(uid)

        logging.debug(f"[TaskHandler]: Removed {task} with id={uid}")
        logging.debug(f"[TaskHandler]: Internal stack dict:\n\t{self.tasks}")

    def reorder(self, new_order):
        logging.debug("[TaskHandler]: Reordering task list")
        logging.debug(f"[TaskHandler]: List before:\n\t{self.tasks}")

        self.tasks = {uid: task for uid, task in zip(new_order, self.tasks.values())}

        logging.debug(f"[TaskHandler]: List after:\n\t{self.tasks}")

    def getTask(self, uid: str):
        logging.debug(f"[TaskHandler]: Getting task under id={uid}")

        return self.tasks[uid]

    def mainloop(self):
        while True:
            if len(self.tasks) and self.isEnabled:
                for task in self.tasks.values():
                    task.perform()


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
