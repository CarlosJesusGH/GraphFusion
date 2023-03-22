__author__ = 'varun'

from TaskFactory.ParallelComputationExecutor import Runnable
from .HyperGraphletsPropertiesResult import HyperGraphletsPropertiesResult
from .settings import COMPUTATIONS_DIR, HYPER_GRAPHLETS_PROPS_TASK, NAMES_MAPPINGS_FILE
from utils.SystemCall import make_system_call
from TaskFactory.models import Task
from datetime import datetime
import traceback
import logging
import os
import uuid

LOGGER = logging.getLogger(__name__)


def __get_matrix_table_for_results(props):
    heading = ["Name", "Nodes", "Edges", "Clustering Coefficient", "Average Path Length", "Diameter"]
    rows = []
    gcm_raw_data = []
    network_names = []
    for prop in props:
        rows.append([
            prop.name,
            prop.number_of_nodes,
            prop.number_of_edges,
            prop.ccoeff,
            prop.avg_path_length,
            prop.diameter
        ])
        network_names.append(prop.name)
        gcm_raw_data.append([prop.name, prop.get_gcm_matrix_png_data()])
    return heading, rows, gcm_raw_data, network_names


def get_network_properties_for_graphs(graphs, user, task_name):
    LOGGER.info("Starting parallel analysis")
    network_analysis_runnable = HyperGraphletsPropertiesAnalysis(graphs=graphs, user=user, task_name=task_name)
    network_analysis_runnable.run()
    LOGGER.info("Finished parallel analysis for network properties")
    heading, rows, gcm_raw_data, network_names = __get_matrix_table_for_results(network_analysis_runnable.results)
    return heading, rows, network_analysis_runnable.deg_dists, gcm_raw_data, \
           network_names, network_analysis_runnable.task


class HyperGraphletsPropertiesAnalysis(Runnable):
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
        task.task_type = HYPER_GRAPHLETS_PROPS_TASK
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
            i = 0
            mappings = []
            for graph_name, graph_data in self.graphs:
                network = HyperGraphletsPropertiesResult(graph_name=graph_name + str(i), operational_dir=self.operational_directory)
                network.parse_content(graph_data)
                network.evaluate_properties()
                result = network.result
                result.id = i
                mappings.append((graph_name + str(i), graph_name))
                result.name = graph_name
                i += 1
                self.deg_dists.append((graph_name, result.get_degree_dist()))
                self.results.append(result)
            with open(self.operational_directory + "/" + NAMES_MAPPINGS_FILE, "w") as f:
                f.write(str(mappings))
            self.__set_task_finished()
        except Exception as e:
            LOGGER.error(e.message)
            LOGGER.error(traceback.format_exc())
            self.task.error_occurred = True
            self.task.error_text = e.message
            self.task.finished = True
            self.task.finished_at = datetime.now()
            self.task.save()
