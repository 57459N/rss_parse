from abc import ABCMeta, abstractmethod


class BaseOutputHandler(metaclass=ABCMeta):
    @staticmethod
    def out(data: list):
        raise NotImplementedError
