from random import randrange
from handlers.TaskHandler import Timer, Clicker, Alerter


def randomId(length):
    res = ''
    for i in range(length):
        res += hex(randrange(0, 15))[-1]
    return res


class DescriptionMap:
    def __init__(self):
        self.map = {Timer:
                    '''
                    This is Timer task. It will delay the execution of next task by selected time.
                    Task UID: {}
                    Time delay: {}
                    ''',
                    Clicker:
                    '''
                    This is Clicker task. It will click at selected coordinates.
                    Task UID: {}
                    X-Coordinate: {}
                    Y-Coordinate: {}
                    ''',
                    Alerter:
                    '''
                    This is Alerter task. It will Alert you by popping up alert box with selected message.
                    Task UID: {}
                    Alert message: {}
                    '''}

    def createDescription(self, task, uid) -> str:
        # TODO remove hardcoded jumptable and use getattr()
        task_type = type(task)
        if task_type in self.map:
            descr = self.map[task_type]
        else:
            return None
        if task_type == Timer:
            descr = descr.format(uid, task.sleep_time)
        elif task_type == Clicker:
            descr = descr.format(uid, task.coords[0], task.coords[1])
        elif task_type == Alerter:
            descr = descr.format(uid, task.alertText)
        return descr
