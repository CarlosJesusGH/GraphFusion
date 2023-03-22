__author__ = 'varun'

from TaskFactory.TaskFactorySingleton import Task
from .settings import CANONICAL_CORRELATION_COMPUTATIONS_DIR, CANONICAL_CORRELATION_TASK, NAMES_MAPPING_FILE_NAME, \
    ANNOTATIONS_TYPE, ANNOTATIONS_FILENAME, MAKE_GO_MATRIX_SCRIPT_PATH, GO_MATRIX_FILE_NAME, CCA_GENERATION_SCRIPT_PATH, \
    GENERATE_PLOT_SCRIPT_PATH, ANNOTATIONS_RETRIEVER_SCRIPT_PATH, GENE_TO_GO_FILE, OBO_FILE, CCA_RESULT_FILENAME, \
    CCA_R_SCRIPT, PLOT_FILE_KEEP_VARIABLE
from utils.SystemCall import make_system_call
from NetworkAlignment.GraphFileConverter import ListToLeda
from NetworkAlignment.ORCAThreadRunner import ORCAExecutable
from TaskFactory.models import Task as TaskModel
from datetime import datetime
from django.db import connection
from WebServer.settings import PYTHON_PATH
import traceback
import uuid
import os
import logging


LOGGER = logging.getLogger(__name__)


class CanonicalAnalysisException(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)


class CanonicalAnalysis(Task):
    def __init__(self, name, user, graph, graph_name, log_scale, annotations=None, annotations_type=None):
        Task.__init__(self, name=name, task_id=-1)
        self.user = user
        self.graph = graph
        self.graph_name = graph_name
        self.log_scale = log_scale
        self.annotations = annotations
        self.annotation_type = annotations_type
        self.task = TaskModel()
        temp = self.__get_fresh_dir()
        self.operational_dir = CANONICAL_CORRELATION_COMPUTATIONS_DIR + "/" + temp
        self.graph_path = self.operational_dir + "/graph"
        self.__initialise_operational_directory()
        self.__save_task_began(user=user, task_name=name, directory=temp)
        self.task_id = self.task.taskId

    def __save_task_began(self, user, task_name, directory):
        LOGGER.info("Starting task for Canonical Analysis " + str(self.task_id))
        self.task.task_type = CANONICAL_CORRELATION_TASK
        self.task.taskName = task_name
        self.task.user = user
        self.task.operational_directory = directory
        self.task.save()

    def __save_task_finished(self):
        LOGGER.info("Task Finished, id:" + str(self.task_id) + " ,op_dir:" + str(self.operational_dir))
        connection.close()
        self.task.finished_at = datetime.now()
        self.task.finished = True
        self.task.save()

    def __initialise_operational_directory(self):
        LOGGER.info("Initialising directory for task: " + self.operational_dir)
        make_system_call("mkdir " + self.operational_dir)

    def __save_graph(self):
        LOGGER.info("Saving graphs for {task_id: " + str(self.task_id) + ", task_name: " + str(self.name) + "}")
        with open(self.graph_path, "w") as f:
            if self.graph.startswith("LEDA.GRAPH"):
                f.write(self.graph)
            else:
                f.write(ListToLeda(graph_list=self.graph).convert_to_leda())

        f = open(self.operational_dir + "/" + NAMES_MAPPING_FILE_NAME, "w")
        f.write(str([self.graph_name]))
        f.close()

    def __retrieve_annotations(self):
        LOGGER.info("Retrieving Annotations for task_id:" + str(self.task_id) + " ,op_dir:" + self.operational_dir)
        if self.annotations:
            with open(self.operational_dir + "/" + ANNOTATIONS_FILENAME, "w") as f:
                f.write(self.annotations)
        else:
            if self.annotation_type in zip(*ANNOTATIONS_TYPE)[0]:
                result = make_system_call(
                    PYTHON_PATH + " " +
                    ANNOTATIONS_RETRIEVER_SCRIPT_PATH + " " +
                    self.graph_path + " " +
                    GENE_TO_GO_FILE + " " +
                    OBO_FILE + " " +
                    self.annotation_type + " " +
                    self.operational_dir + "/" + ANNOTATIONS_FILENAME
                    , working_dir=self.operational_dir)
                LOGGER.info(result.stdout)
            else:
                raise CanonicalAnalysisException(
                    "Invalid annotation type given: " + self.annotation_type +
                    ". Please reload your page and re-submit your analysis.")

    def __run_orca_for_network(self):
        ORCAExecutable(file_path=self.graph_path).run()

    def __generate_go_matrix(self):
        return make_system_call(
            PYTHON_PATH + " " +
            MAKE_GO_MATRIX_SCRIPT_PATH + " " +
            self.graph_path + " " +
            self.graph_path + ".res.ndump2 " +
            ANNOTATIONS_FILENAME + " " +
            GO_MATRIX_FILE_NAME + " "
            , working_dir=self.operational_dir)

    def __run_cca(self):
        return make_system_call(
            PYTHON_PATH + " " +
            CCA_GENERATION_SCRIPT_PATH + " " +
            GO_MATRIX_FILE_NAME + "_GO " +
            GO_MATRIX_FILE_NAME + "_GDV " +
            self.operational_dir + " " +
            CCA_RESULT_FILENAME + " " +
            self.log_scale + " " +
            CCA_R_SCRIPT
            , working_dir=self.operational_dir)

    def __generate_result_figures(self):
        return make_system_call(
            PYTHON_PATH + " " +
            GENERATE_PLOT_SCRIPT_PATH + " " +
            GO_MATRIX_FILE_NAME + "_GO " +
            GO_MATRIX_FILE_NAME + "_GDV " +
            self.operational_dir + " " +
            CCA_RESULT_FILENAME + " " +
            PLOT_FILE_KEEP_VARIABLE
            , working_dir=self.operational_dir)

    @classmethod
    def __get_fresh_dir(cls):
        temp = uuid.uuid4().hex
        while os.path.isdir(CANONICAL_CORRELATION_COMPUTATIONS_DIR + "/" + temp):
            temp = uuid.uuid4().hex
        return temp

    def __check_annotations_file(self):
        if not os.path.isfile(self.operational_dir + "/" + ANNOTATIONS_FILENAME):
            raise CanonicalAnalysisException(
                "Annotations could not be created. " +
                "Please make sure that the input network contains Entrez Ids for node labelling.")
        elif len(open(self.operational_dir + "/" + ANNOTATIONS_FILENAME, "r").readlines()) == 0:
            raise CanonicalAnalysisException(
                "Annotations could not be created. " +
                "Please make sure that the input network contains Entrez Ids for node labelling.")

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