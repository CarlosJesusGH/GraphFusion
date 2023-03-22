__author__ = 'carlos garcia-hernandez'  # using as reference: WebServer/PairwiseAnalysis/PairwiseAnalysis.py

from datetime import datetime
from django.db import connection

# from WebServer.DataFusion.DataFusion import DataFusion
# from DataFusion import *
from .DataFusion import DataFusion
# from DataFusion.DataFusion import DataFusion
from .settings import COMPUTATIONS_DIR, DATA_FUSION_TASK, NAMES_MAPPING_FILE, \
    NAMES_OF_NETWORKS_LIST_FILES, DATA_FUSION_SCRIPT_PATH, TEST_SCRIPT_PATH
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


def get_runnable_for_comparison_analysis(operational_dir, graph_paths):
    print("marker ini get_runnable_for_comparison_analysis")
    tasks = []
    runnable = TestRunnable(operational_dir=operational_dir, graph_paths=graph_paths)
    tasks.append(runnable)
    LOGGER.info("number of runnables are: " + str(len(tasks)))
    return tasks

def get_runnable_for_datafusion_analysis(operational_dir, facts):
    print("marker ini get_runnable_for_datafusion_analysis")
    tasks = []
    runnable = DataFusionRunnable(operational_dir=operational_dir, facts=facts)
    tasks.append(runnable)
    LOGGER.info("number of runnables are: " + str(len(tasks)))
    return tasks

# ---------------------------------------------

class DataFusionAnalysisException(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)

# ---------------------------------------------

class TestRunnable(Runnable):
    def __init__(self, operational_dir, graph_paths):
        Runnable.__init__(self)
        self.operational_dir = operational_dir
        self.graph_paths = graph_paths

    def run(self):
        LOGGER.info("Starting analysis for: str(self.analysis_type), operational_dir: " + str(self.operational_dir))
        result = make_system_call(
            # PYTHON_PATH + " " +
            "python " +
            # TEST_SCRIPT_PATH + " " +
            DATA_FUSION_SCRIPT_PATH + " " +
            str(self.operational_dir) + " " + 
            str(self.operational_dir) + " " + 
            str(NUMBER_OF_PROCESSES),
            working_dir=self.operational_dir)
        if result.stdout != "":
            LOGGER.info(result.stdout)
        if result.stderr != "":
            LOGGER.error(result.stderr)
        LOGGER.info("Finished analysis for: str(self.analysis_type), operational_dir: " + str(self.operational_dir))

# ---------------------------------------------

class DataFusionRunnable(Runnable):
    def __init__(self, operational_directory, facts):
        Runnable.__init__(self)
        self.operational_directory = operational_directory
        self.facts = facts

    def __initialise_operational_directory(self):
        LOGGER.info("Initialising directory for computation :" + self.operational_directory)
        make_system_call("mkdir " + self.operational_directory)

    def DELETErun(self):
        LOGGER.info("Starting analysis for:", str(self.analysis_type), ", operational_dir: " + str(self.operational_dir))
        try:
            self.__initialise_operational_directory()
            # mappings = []
            df = DataFusion(operational_dir=self.operational_directory, facts=self.facts) (graph_name=graph_name + str(i), operational_dir=self.operational_directory)
            # network.parse_content(graph_data)
            # network.evaluate_properties()
            result = df.result
            result.id = 0
            # df.perform_datafusion()
            # mappings.append((graph_name + str(i), graph_name))
            # result.name = graph_name
            # self.deg_dists.append((graph_name, result.get_degree_dist()))
            # self.results.append(result)
            # with open(self.operational_directory + "/" + NETWORKS_NAMES_MAPPINGS_FILE_NAME, "w") as f:
            #     f.write(str(mappings))
            self.__set_task_finished()
        except Exception as e:
            LOGGER.error(e.message)
            LOGGER.error(traceback.format_exc())
            self.task.error_occurred = True
            self.task.error_text = e.message
            self.task.finished = True
            self.task.finished_at = datetime.now()
            self.task.save()
        LOGGER.info("Finished analysis for: str(self.analysis_type), operational_dir: " + str(self.operational_dir))

    def run_task(self):
        try:
            self.__save_graph()
            self.__run_orca_for_network()
            self.__retrieve_annotations()
            self.__check_annotations_file()
            result = self.__generate_go_matrix()
            if len(result.stderr):
                raise CanonicalAnalysisException(
                    "Error occurred while computing Gene Ontology Matrix: \n" + result.stderr)
            LOGGER.info(result)

            result = self.__run_cca()
            LOGGER.info(result)
            if len(result.stderr):
                raise CanonicalAnalysisException(
                    "Error occurred while computing CCA: \n\n" + result.stderr)

            result = self.__generate_result_figures()
            LOGGER.info(result)
            if len(result.stderr) and "RuntimeWarning" not in result.stderr:
                raise CanonicalAnalysisException(
                    "Error occurred while generating result figures: \n\n" + result.stderr)
            self.__save_task_finished()
        except Exception as e:
            connection.close()
            LOGGER.error(e)
            LOGGER.error(traceback.format_exc())
            self.task.error_occurred = True
            self.task.error_text = e.message
            self.task.finished = True
            self.task.finished_at = datetime.now()
            self.task.save()

# ---------------------------------------------

class ORCARunnable(Runnable):
    def __init__(self, operational_dir, graph_paths):
        Runnable.__init__(self)
        self.operational_dir = operational_dir
        self.graph_paths = graph_paths

    def run(self):
        self.orca_executable.run()

# ---------------------------------------------

class DataFusionAnalysis_old(Task):
    def __init__(self, facts, user, task_name):
        Task.__init__(self, name=task_name, task_id=-1)
        self.facts = facts
        self.graph_paths = []
        self.task = TaskModel()
        temp = self.__get_fresh_dir()
        self.operational_dir = COMPUTATIONS_DIR + "/" + temp
        self.save_task_began(user=user, task_name=task_name, directory=temp)
        self.task_id = self.task.taskId

    @classmethod
    def __get_fresh_dir(cls):
        # print("marker ini __get_fresh_dir")
        temp = uuid.uuid4().hex
        while os.path.isdir(COMPUTATIONS_DIR + "/" + temp):
            temp = uuid.uuid4().hex
        return temp

    def save_task_began(self, user, task_name, directory):
        # print("marker ini save_task_began")
        self.task.task_type = DATA_FUSION_TASK
        self.task.taskName = task_name
        self.task.user = user
        self.task.operational_directory = directory
        self.task.save()

    def save_task_finished(self):
        # print("marker ini save_task_finished")
        connection.close()
        self.task.finished_at = datetime.now()
        self.task.finished = True
        self.task.save()

    def run_orca_for_all_networks_in_dir(self):
        # print("marker ini run_orca_for_all_networks_in_dir")
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
        # print("marker ini __save_list_of_graphs")
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
        # print("marker ini save_graphs")
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
        # print("marker end save_graphs")

    def remove_directory(self):
        # print("marker ini remove_directory")
        make_system_call("rm -r " + self.operational_dir)

    def __run_data_fusion_analysis(self):
        # print("marker ini __run_data_fusion_analysis")
        LOGGER.info("Running data fusion analysis")
        tasks = get_runnable_for_datafusion_analysis(operational_dir=self.operational_dir,
                                                     facts=self.facts)
        ParallelComputationTask(tasks=tasks).run_and_wait()
        self.save_task_finished()
        LOGGER.info("Finished data fusion analysis")

    def run_analysis(self):
        print("markere ini run_analysis")
        # LOGGER.info("Initialising directory for computation :" + self.operational_dir)
        # make_system_call("mkdir " + self.operational_dir)
        # self.save_graphs()
        # self.run_orca_for_all_networks_in_dir()
        # self.__run_network_properties_comparison()
        self.__run_data_fusion_analysis()

    def run_task(self):
        print("marker ini run_task")
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