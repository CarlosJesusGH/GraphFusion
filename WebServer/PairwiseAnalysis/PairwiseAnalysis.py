__author__ = 'varun'

from datetime import datetime
from django.db import connection
from .settings import PAIRWISE_ANALYSIS_COMPUTATIONS_DIR, PAIRWISE_ANALYSIS_TASK, NAMES_MAPPING_FILE, \
    NETWORK_COMPARISON_SCRIPT, DISTANCES, NAMES_OF_NETWORKS_LIST_FILES
from utils.SystemCall import make_system_call

from NetworkAlignment.GraphFileConverter import ListToLeda
from TaskFactory.ParallelComputationExecutor import Runnable, ParallelComputationTask

from NetworkAlignment.ORCAThreadRunner import ORCAExecutable
from TaskFactory.models import Task as TaskModel
from TaskFactory.TaskFactorySingleton import Task
from WebServer.settings import PYTHON_PATH
import uuid
import logging
import traceback
import os


LOGGER = logging.getLogger(__name__)
NUMBER_OF_PROCESSES = 1
__ALL_DISTANCES = list(zip(*DISTANCES)[0])


def get_runnable_for_comparison_analysis(operational_dir, graph_paths, distances):
    tasks = []
    for analysis in distances:
        if analysis not in __ALL_DISTANCES:
            raise PairwiseAnalysisException(
                "Distance " + analysis + " not currently supported. Please contact administrator for further reference.")
        runnable = NetworkComparisonRunnable(operational_dir=operational_dir, analysis_type=analysis,
                                             graph_paths=graph_paths)
        tasks.append(runnable)
    LOGGER.info("number of runnables are: " + str(len(tasks)))
    return tasks


class PairwiseAnalysisException(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)


class NetworkComparisonRunnable(Runnable):
    def __init__(self, operational_dir, analysis_type, graph_paths):
        Runnable.__init__(self)
        self.operational_dir = operational_dir
        self.analysis_type = analysis_type
        self.graph_paths = graph_paths

    def run(self):
        LOGGER.info(
            "Starting analysis for: " + str(self.analysis_type) + ", operational_dir: " + str(self.operational_dir))
        result = make_system_call(
            PYTHON_PATH + " " +
            NETWORK_COMPARISON_SCRIPT + " " +
            str(self.operational_dir) + " " +
            str(self.analysis_type) + " " + str(NUMBER_OF_PROCESSES),
            working_dir=self.operational_dir)
        if result.stdout != "":
            LOGGER.info(result.stdout)
        if result.stderr != "":
            LOGGER.error(result.stderr)
        LOGGER.info(
            "Finished analysis for: " + str(self.analysis_type) + ", operational_dir: " + str(self.operational_dir))


class ORCARunnable(Runnable):
    def __init__(self, orca_executable):
        Runnable.__init__(self)
        self.orca_executable = orca_executable

    def run(self):
        self.orca_executable.run()


class PairwiseAnalysis(Task):
    def __init__(self, graphs, user, task_name, distances):
        Task.__init__(self, name=task_name, task_id=-1)
        self.graphs = graphs
        self.distances = distances
        self.graph_paths = []
        self.task = TaskModel()
        temp = self.__get_fresh_dir()
        self.operational_dir = PAIRWISE_ANALYSIS_COMPUTATIONS_DIR + "/" + temp
        self.save_task_began(user=user, task_name=task_name, directory=temp)
        self.task_id = self.task.taskId

    @classmethod
    def __get_fresh_dir(cls):
        temp = uuid.uuid4().hex
        while os.path.isdir(PAIRWISE_ANALYSIS_COMPUTATIONS_DIR + "/" + temp):
            temp = uuid.uuid4().hex
        return temp

    def save_task_began(self, user, task_name, directory):
        self.task.task_type = PAIRWISE_ANALYSIS_TASK
        self.task.taskName = task_name
        self.task.user = user
        self.task.operational_directory = directory
        self.task.save()

    def save_task_finished(self):
        connection.close()
        self.task.finished_at = datetime.now()
        self.task.finished = True
        self.task.save()

    def run_orca_for_all_networks_in_dir(self):
        runnable = []
        for graph_path in self.graph_paths:
            r = ORCARunnable(orca_executable=ORCAExecutable(file_path=graph_path + ".gw"))
            runnable.append(r)
        ParallelComputationTask(tasks=runnable).run_and_wait()
        for _, _, file_names in os.walk(self.operational_dir):
            for f in file_names:
                if f.endswith('.res.ndump2'):
                    os.rename(self.operational_dir + "/" + f,
                              self.operational_dir + "/" + f.replace(".res.ndump2", ".ndump2"))

    def __save_list_of_graphs(self, graphs, i, mappings):
        nets = []
        for g_name, g in graphs:
            file_path = self.operational_dir + "/" + g_name + str(i)
            mappings[file_path] = g_name
            nets.append(file_path)
            self.graph_paths.append(file_path)
            f = open(file_path + ".gw", "w")
            if g.startswith("LEDA.GRAPH"):
                f.write(g)
            else:
                f.write(ListToLeda(graph_list=g).convert_to_leda())
            f.close()
            i += 1
        return nets

    def save_graphs(self):
        mappings = {}
        net_1 = self.__save_list_of_graphs(self.graphs[0], 0, mappings)
        net_2 = self.__save_list_of_graphs(self.graphs[1], len(net_1), mappings)
        self.graphs = None

        LOGGER.info("Saving mappings for: " + self.task.taskName + " by " + str(self.task.user))
        f = open(self.operational_dir + "/" + NAMES_MAPPING_FILE, "w")
        f.write(str(mappings))
        f.close()
        LOGGER.info("Saving list of networks in first and second list.")
        with open(self.operational_dir + "/" + NAMES_OF_NETWORKS_LIST_FILES[0], "w") as f:
            f.write(str(net_1))
        with open(self.operational_dir + "/" + NAMES_OF_NETWORKS_LIST_FILES[1], "w") as f:
            f.write(str(net_2))

    def remove_directory(self):
        make_system_call("rm -r " + self.operational_dir)

    def __run_network_properties_comparison(self):
        LOGGER.info("Running network comparison analysis")
        tasks = get_runnable_for_comparison_analysis(operational_dir=self.operational_dir,
                                                     graph_paths=self.graph_paths,
                                                     distances=self.distances)
        ParallelComputationTask(tasks=tasks).run_and_wait()
        self.save_task_finished()
        LOGGER.info("Finished network comparison analysis")

    def run_analysis(self):
        LOGGER.info("Initialising directory for computation :" + self.operational_dir)
        make_system_call("mkdir " + self.operational_dir)
        self.save_graphs()
        self.run_orca_for_all_networks_in_dir()
        self.__run_network_properties_comparison()

    def run_task(self):
        try:
            self.run_analysis()
        except Exception as e:
            LOGGER.error(e.message)
            LOGGER.error(traceback.format_exc())
            self.task.error_occurred = True
            self.task.error_text = e.message
            self.task.finished = True
            self.task.finished_at = datetime.now()
            self.task.save()