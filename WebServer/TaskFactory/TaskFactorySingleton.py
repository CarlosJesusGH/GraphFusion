__author__ = 'varun'
from abc import abstractmethod, ABCMeta
from multiprocessing import Process
import traceback
import logging

LOGGER = logging.getLogger(__name__)


class Task(Process):
    __metaclass__ = ABCMeta

    def __init__(self, name, task_id):
        Process.__init__(self, name=name)
        self.task_id = task_id
        self.name = name

    @abstractmethod
    def run_task(self):
        pass

    def run(self):
        self.run_task()

    def submit(self):
        TASK_FACTORY.add_task(task=self)


class __TaskFactory:
    def __init__(self):
        self.running_tasks = {}
        pass

    def remove_task_from_running_list(self, task_id):
        if str(task_id) in self.running_tasks:
            del self.running_tasks[str(task_id)]

    def __terminate_children(self, task_id):
        task = self.running_tasks[str(task_id)]
        if getattr(task, "get_children", None) and callable(getattr(task, "get_children", None)):
            for child in task.get_children():
                child.terminate()

    def terminate_task(self, task_id):
        self.__terminate_children(task_id=task_id)
        # os.killpg(self.running_tasks[str(task_id)].pid, signal.SIGTERM)

    def add_task(self, task):
        self.running_tasks[str(task.task_id)] = task
        task.start()


TASK_FACTORY = __TaskFactory()


def terminate_task(task_id):
    try:
        TASK_FACTORY.terminate_task(task_id=task_id)
        return True
    except Exception as e:
        LOGGER.error(e)
        LOGGER.error(traceback.format_exc())
        return True