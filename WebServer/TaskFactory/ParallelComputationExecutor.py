__author__ = 'varun'
from abc import abstractmethod, ABCMeta
import logging
import threading

LOGGER = logging.getLogger(__name__)


class Runnable(threading.Thread):
    __metaclass__ = ABCMeta

    @abstractmethod
    def run(self):
        pass


class ParallelComputationTask:
    def __init__(self, tasks):
        self.tasks = tasks

    def get_children(self):
        return self.tasks

    def run_sequential(self):
        for t in self.tasks:
            t.start()
            t.join()

    def run_and_wait(self):
        for t in self.tasks:
            t.start()
        for t in self.tasks:
            t.join()

    def run(self):
        for t in self.tasks:
            t.start()
