from random import randrange


def randomId(length):
    res = ''
    for i in range(length):
        res += hex(randrange(0, 15))[-1]
    return res
