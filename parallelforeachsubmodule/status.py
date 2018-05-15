# -*- coding: utf-8 -*-

from threading import Lock
import copy


class Counter(object):
    def __init__(self, num_elements=0):
        self.__value = 0
        self.__num_elements = num_elements
        self.__lock = Lock()

    def get_value(self):
        self.__lock.acquire()
        val = copy.copy(self.__value)
        self.__lock.release()
        return val

    def set_value(self, val):
        self.__lock.acquire()
        self.__value = val
        self.__lock.release()

    def reset(self):
        self.__lock.acquire()
        self.__value = 0
        self.__lock.release()

    def increment_value(self, increment=1):
        self.__lock.acquire()
        self.__value = self.__value + increment
        val = copy.copy(self.__value)
        self.__lock.release()
        if self.__num_elements == 0:
            return val
        else:
            return "[" + str(val) + "/" + str(self.__num_elements) + "]"

    def decrement_value(self, decrement=1):
        self.__lock.acquire()
        self.__value = self.__value + decrement
        val = copy.copy(self.__value)
        self.__lock.release()
        if self.__num_elements == 0:
            return val
        else:
            return "[" + str(val) + "/" + str(self.__num_elements) + "]"
