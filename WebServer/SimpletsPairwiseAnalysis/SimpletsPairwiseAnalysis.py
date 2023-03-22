__author__ = 'carlos garcia-hernandez'

from datetime import datetime
from django.db import connection
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
from .settings import *
from utils.SystemCall import make_system_call

from NetworkAlignment.GraphFileConverter import ListToLeda
from TaskFactory.ParallelComputationExecutor import Runnable, ParallelComputationTask

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
            raise SimpletsPairwiseAnalysisException(
                "Distance " + analysis + " not currently supported. Please contact administrator for further reference.")
        runnable = NetworkComparisonRunnable(operational_dir=operational_dir, analysis_type=analysis,
                                             graph_paths=graph_paths)
        tasks.append(runnable)
    LOGGER.info("number of runnables are: " + str(len(tasks)))
    return tasks


class SimpletsPairwiseAnalysisException(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)


class NetworkComparisonRunnable(Runnable):
    def __init__(self, operational_dir, analysis_type, graph_paths):
        Runnable.__init__(self)
        self.operational_dir = operational_dir
        self.analysis_type = analysis_type
        self.graph_paths = graph_paths

    def run(self):
        LOGGER.info("Starting analysis for: " + str(self.analysis_type) + ", operational_dir: " + str(self.operational_dir))
        # result = make_system_call(
        #     PYTHON_PATH + " " +
        #     NETWORK_COMPARISON_SCRIPT + " " +
        #     str(self.operational_dir) + " " +
        #     str(self.analysis_type) + " " + str(NUMBER_OF_PROCESSES),
        #     working_dir=self.operational_dir)
        result = make_system_call(
            "bash " + SIMPLETS_COMPARISON_SCRIPT + " " + 
            # self.operational_dir + " " +
            str(self.analysis_type) + " " + str(NUMBER_OF_PROCESSES),
            working_dir=self.operational_dir)
        if result.stdout != "":
            LOGGER.info(result.stdout)
        if result.stderr != "":
            LOGGER.error(result.stderr)
        LOGGER.info(
            "Finished analysis for: " + str(self.analysis_type) + ", operational_dir: " + str(self.operational_dir))


class SDVRunnable(Runnable):
    def __init__(self, sdv_executable):
        Runnable.__init__(self)
        self.dgdv_executable = sdv_executable

    def run(self):
        self.dgdv_executable.run()


class SimpletsPairwiseAnalysis(Task):
    def __init__(self, graphs, user, task_name, distances):
        Task.__init__(self, name=task_name, task_id=-1)
        self.graphs = graphs
        self.distances = distances
        self.graph_paths = []
        self.task = TaskModel()
        temp = self.__get_fresh_dir()
        self.operational_dir = COMPUTATIONS_DIR + "/" + temp
        self.save_task_began(user=user, task_name=task_name, directory=temp)
        self.task_id = self.task.taskId

    @classmethod
    def __get_fresh_dir(cls):
        temp = uuid.uuid4().hex
        while os.path.isdir(COMPUTATIONS_DIR + "/" + temp):
            temp = uuid.uuid4().hex
        return temp

    def save_task_began(self, user, task_name, directory):
        self.task.task_type = SIMPLETS_PAIRWISE_ANALYSIS_TASK
        self.task.taskName = task_name
        self.task.user = user
        self.task.operational_directory = directory
        self.task.save()

    def save_task_finished(self):
        connection.close()
        self.task.finished_at = datetime.now()
        self.task.finished = True
        self.task.save()

    def run_sdv_signatures_for_all_networks_in_dir(self):
        runnable = []
        for graph_path in self.graph_paths:
            print("for graph_path:", graph_path)
            r = SDVRunnable(sdv_executable=SDVExecutable(file_path=graph_path))
            runnable.append(r)
        ParallelComputationTask(tasks=runnable).run_and_wait()

    def __save_list_of_graphs(self, graphs, i, mappings):
        nets = []
        for g_name, g in graphs:
            file_path = self.operational_dir + "/" + g_name + str(i)
            mappings[file_path] = g_name
            nets.append(file_path)
            self.graph_paths.append(file_path)
            f = open(file_path, "w")
            f.write(g)
            f.close()
            i += 1
        return nets

    def __save_list_of_graphs_old(self, graphs, i, mappings):
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
        make_system_call("mkdir -p " + self.operational_dir)
        self.save_graphs()
        self.run_sdv_signatures_for_all_networks_in_dir()
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


class SDVExecutable:
    def __init__(self, file_path):
        self.file_path = file_path
        self.output_file_name = ""

    def remove_computational_files(self):
        os.remove(self.output_file_name)

    def run(self):
        LOGGER.info("Running SDV for " + str(self.file_path))
        result = make_system_call(SDV_SIGNATURES_SCRIPT + ' ' + self.file_path + ' ' + self.file_path + "_signatures.sdv")
        if result.return_code != 0:
            raise SDVRunnerException("Error while running parallel runner for SDV: " + str(result.stderr))
        # self.remove_computational_files()


class SDVRunnerException(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)