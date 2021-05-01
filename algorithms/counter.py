import abc
import contextlib
import dataclasses
import logging
from abc import ABC


class AbstractCounter(ABC):
    @abc.abstractmethod
    def increase(self, name: str):
        pass

    @abc.abstractmethod
    def finish(self, msg: str = ""):
        pass


class FakeCounter(AbstractCounter):
    @staticmethod
    def increase(name: str):
        pass

    @staticmethod
    def finish(msg: str = ""):
        pass


@dataclasses.dataclass(init=False)
class Counter(AbstractCounter):
    value: int

    def __init__(self, name: str):
        self.value = 0
        self.logger = logging.getLogger(name)

    def increase(self, msg: str):
        self.value += 1
        self.logger.debug("{}. {}".format(self.value, msg))

    def finish(self, msg: str = ""):
        if not msg:
            self.logger.debug("{}. Done.".format(self.value))
        else:
            self.logger.debug("{}. Done. {}".format(self.value, msg))


@contextlib.contextmanager
def get_counter(fn):
    counter = Counter(name="{}.{}".format(fn.__module__, fn.__name__))
    yield counter
