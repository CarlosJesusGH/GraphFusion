import logging
import traceback
import uuid
from datetime import datetime

import os
from abc import abstractmethod, ABCMeta

from utils.SystemCall import make_system_call
from .settings import ALIGNMENT_TASK, COMPUTATIONS_DIR, NAMES_MAPPING_FILE
from GraphFileConverter import ListToLeda
from TaskFactory.TaskFactorySingleton import Task
from TaskFactory.models import Task as TaskModel
from .AlignmentResultsDataStructure import AlignmentResult
from django.db import connection

LOGGER = logging.getLogger(__name__)


class InvalidConstructionError(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)


class AlignmentRunnerException(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)


class AlignmentRunner(Task):
    __metaclass__ = ABCMeta
    RESULT_FILE_NAME = "result"

    def __init__(self, name, graph1, graph2, graph1_name, graph2_name, user):
        name = "Alignment Task: " + graph1_name + "-" + graph2_name if not name or name == "" else name
        Task.__init__(self, name=name, task_id=-1)
        self.graph1 = graph1
        self.graph2 = graph2
        temp = self.__get_fresh_dir()
        self.operational_dir = COMPUTATIONS_DIR + "/" + temp
        self.result = AlignmentResult(operational_dir=self.operational_dir)
        self.result.graph1_name = graph1_name
        self.result.graph2_name = graph2_name
        self.user = user
        self.task = TaskModel()
        self.task_id = self.task.taskId
        self.__initialise_dir()
        self.save_task_began(operational_dir=temp)

    def run_input_checks(self):
        from Visualise.graph_properties import get_graph_nodes_and_edges

        g1_nodes, _ = get_graph_nodes_and_edges(self.graph1)
        g2_nodes, _ = get_graph_nodes_and_edges(self.graph2)
        if len(g1_nodes) > len(g2_nodes):
            self.result.error = "Number of nodes in first network should not be greater than second network."
            self.save_task_finished()
            raise AlignmentRunnerException(self.result.error)

    @classmethod
    def __get_fresh_dir(cls):
        temp = uuid.uuid4().hex
        while os.path.isdir(COMPUTATIONS_DIR + "/" + temp):
            temp = uuid.uuid4().hex
        return temp

    def save_task_began(self, operational_dir):
        self.task.taskName = self.name
        self.task.operational_directory = operational_dir
        self.task.task_type = ALIGNMENT_TASK
        self.task.user = self.user
        self.task.save()

    def save_task_finished(self):
        connection.close()
        LOGGER.info("Saving Task model")
        self.task.finished_at = datetime.now()
        self.task.finished = True
        self.task.error_text = self.result.error
        if self.result.error != "":
            self.task.error_occurred = True
        self.task.save()

    def get_path_for_graph_1(self):
        return self.operational_dir + "/1"

    def get_path_for_graph_2(self):
        return self.operational_dir + "/2"

    def __initialise_dir(self):
        LOGGER.info("Initialising directory for computation :" + self.operational_dir)
        make_system_call("mkdir " + self.operational_dir)
        self.__save_file(self.graph1, self.get_path_for_graph_1())
        self.__save_file(self.graph2, self.get_path_for_graph_2())

    def __convert_graphs_to_leda_if_not_in_leda(self):
        LOGGER.info("Converting graph to LEDA format")
        self.__convert_to_leda_graph(self.graph1, self.get_path_for_graph_1())
        self.__convert_to_leda_graph(self.graph2, self.get_path_for_graph_2())

    @classmethod
    def __save_file(cls, data, filepath):
        f = open(filepath, 'w')
        f.write(data)
        f.close()

    @classmethod
    def __convert_to_leda_graph(cls, graph, name):
        if not graph.startswith("LEDA.GRAPH"):
            converter = ListToLeda(graph_list=graph)
            f = open(str(name), 'w')
            f.write(converter.convert_to_leda())
            f.close()

    @abstractmethod
    def run_alignment_algorithm(self):
        pass

    def __get_result_properties(self):
        if os.path.isfile(self.operational_dir + "/" + self.RESULT_FILE_NAME + ".results"):
            for line in open(self.operational_dir + "/" + self.RESULT_FILE_NAME + ".results", "r"):
                tokens = line.split(":")
                if len(tokens) == 2:
                    self.result.properties.append((tokens[0].strip(), tokens[1].strip()))

    def __get_alignment(self):
        self.result.alignment = open(self.operational_dir + "/" + self.RESULT_FILE_NAME + ".aln", "r").read()

    def delete_operational_dir(self):
        LOGGER.info("Deleting operational directory: " + self.operational_dir)
        make_system_call("rm -r " + self.operational_dir)

    @abstractmethod
    def run_algorithm(self):
        pass

    def save_network_names(self):
        f = open(self.operational_dir + "/" + NAMES_MAPPING_FILE, "w")
        f.write(str([self.result.graph1_name, self.result.graph2_name]))
        f.close()

    def __save_results(self):
        LOGGER.info("Saving Results")
        self.__get_result_properties()
        self.__get_alignment()
        self.result.save_results()

    def run_task(self):
        try:
            self.__convert_graphs_to_leda_if_not_in_leda()
            self.run_algorithm()
            self.__save_results()
            self.save_network_names()
            self.save_task_finished()
            LOGGER.info("Alignment results saved for " + str(self.task.taskId) + " executed by " + str(self.task.user))
        except Exception as e:
            LOGGER.error(e)
            LOGGER.error(traceback.format_exc())
            self.result.error = str(e)
            self.result.save_results()
            self.save_task_finished()