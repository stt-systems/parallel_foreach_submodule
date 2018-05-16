# -*- coding: utf-8 -*-

try:
    import queue
except ImportError:
    import Queue as queue   #Python 2 compatibility


class Scheduler(object):
    def __init__(self, submodules):
        self.__queue = queue.Queue()
        self.feed_queue(submodules)

    def feed_queue(self, submodules):

        for submodule in submodules:
            self.__queue.put(submodule)

    def get(self):
        return self.__queue.get()

    def empty(self):
        return self.__queue.empty()
