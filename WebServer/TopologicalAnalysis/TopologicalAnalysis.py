__author__ = 'carlos garcia-hernandez'  # using as reference: WebServer/CanonicalCorrelationAnalysis/CanonicalAnalysis.py

from TaskFactory.ParallelComputationExecutor import Runnable
from .settings import COMPUTATIONS_DIR, TOPOLOGICAL_ANALYSIS_TASK, NAMES_MAPPINGS_FILE
from utils.SystemCall import make_system_call
from TaskFactory.models import Task
from datetime import datetime
import traceback
import logging
import os
import uuid

LOGGER = logging.getLogger(__name__)


class TopologicalAnalysis(Runnable):
    def __init__(self, graphs, user, task_name):
        Runnable.__init__(self)
        self.graphs = graphs
        temp = uuid.uuid4().hex
        while os.path.isdir(COMPUTATIONS_DIR + "/" + temp):
            temp = uuid.uuid4().hex
        self.operational_directory = COMPUTATIONS_DIR + "/" + temp
        self.task = self.__initialise_task(task_name, temp, user)
        self.results = []
        self.deg_dists = []

    @classmethod
    def __initialise_task(cls, task_name, temp, user):
        task = Task()
        task.task_type = TopologicalAnalysis_TASK
        task.operational_directory = temp
        task.user = user
        task.taskName = task_name
        task.save()
        return task

    def __set_task_finished(self):
        self.task.finished = True
        self.task.error_occurred = False
        self.task.finished_at = datetime.now()
        self.task.save()

    def __initialise_operational_directory(self):
        LOGGER.info("Initialising directory for computation :" + self.operational_directory)
        make_system_call("mkdir " + self.operational_directory)

    def run(self):
        try:
            self.__initialise_operational_directory()
        except Exception as e:
            LOGGER.error(traceback.format_exc())