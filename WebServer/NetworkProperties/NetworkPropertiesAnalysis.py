__author__ = 'varun and carlos garcia-hernandez'

from TaskFactory.ParallelComputationExecutor import Runnable
from .NetworkProperties import NetworkProperties
from .settings import NETWORK_PROPERTIES_COMPUTATIONS_DIR, NETWORK_PROPERTIES_TASK, NETWORKS_NAMES_MAPPINGS_FILE_NAME
from utils.SystemCall import make_system_call
# from TaskFactory.models import Task
from TaskFactory.TaskFactorySingleton import Task
from TaskFactory.models import Task as TaskModel
from django.db import connection
from datetime import datetime
import traceback
import logging
import os
import uuid

LOGGER = logging.getLogger(__name__)


def _get_matrix_table_for_results(props):
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
        gcm_raw_data.append([prop.name, prop.get_gcm_matrix_svg_data()])
    return heading, rows, gcm_raw_data, network_names


def get_network_properties_for_graphs(graphs, user, task_name):
    LOGGER.info("Starting parallel analysis")
    network_analysis_runnable = NetworkPropertiesAnalysis(graphs=graphs, user=user, task_name=task_name)
    # network_analysis_runnable.run()
    network_analysis_runnable.submit()
    LOGGER.info("Finished parallel analysis for network properties")
    # heading, rows, gcm_raw_data, network_names = __get_matrix_table_for_results(network_analysis_runnable.results)
    # return heading, rows, network_analysis_runnable.deg_dists, gcm_raw_data, \
    #        network_names, network_analysis_runnable.task
    return True


class NetworkPropertiesAnalysis(Task):
    def __init__(self, graphs, user, task_name):
        Task.__init__(self, name=task_name, task_id=-1)
        self.user = user
        self.graphs = graphs
        self.task = TaskModel()
        temp = self.__get_fresh_dir()
        self.operational_dir = NETWORK_PROPERTIES_COMPUTATIONS_DIR + "/" + temp + "/"
        # self.graph_path = self.operational_dir
        self.__initialise_operational_directory()
        self.__save_task_began(user=user, task_name=task_name, directory=temp)
        self.task_id = self.task.taskId
        self.results = []
        self.deg_dists = []
        

    @classmethod
    def __get_fresh_dir(cls):
        temp = uuid.uuid4().hex
        while os.path.isdir(NETWORK_PROPERTIES_COMPUTATIONS_DIR + "/" + temp):
            temp = uuid.uuid4().hex
        return temp

    def __initialise_operational_directory(self):
        LOGGER.info("Initialising directory for computation :" + self.operational_dir)
        make_system_call("mkdir " + self.operational_dir)

    def __save_task_began(self, user, task_name, directory):
        LOGGER.info("Starting task for " + str(self.task_id))
        self.task.task_type = NETWORK_PROPERTIES_TASK
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

    # def run(self):
    def run_task(self):
        try:
            # self.__initialise_operational_directory()
            i = 0
            mappings = []
            for graph_name, graph_data in self.graphs:
                network = NetworkProperties(graph_name=graph_name + str(i), operational_dir=self.operational_dir)
                network.parse_content(graph_data)
                network.evaluate_properties()
                result = network.result
                result.id = i
                mappings.append((graph_name + str(i), graph_name))
                result.name = graph_name
                i += 1
                self.deg_dists.append((graph_name, result.get_degree_dist()))
                self.results.append(result)
            with open(self.operational_dir + "/" + NETWORKS_NAMES_MAPPINGS_FILE_NAME, "w") as f:
                f.write(str(mappings))
            # Compute the 'rendered_view' also in the background
            from django.template import Context
            from django.template.loader import get_template
            from .settings import NETWORK_RESULT_VIEW_FILE_NAME
            from .views import _save_deg_dist_image
            heading, rows, gcm_raw_data, network_names = _get_matrix_table_for_results(self.results)
            context = Context({
            'heading': heading,
            'rows': rows,
            'gcm_raw_data': gcm_raw_data,
            'network_names': network_names,
            'deg_dist': _save_deg_dist_image(self.deg_dists, task=self.task)
            })
            rendered_view = get_template("networkProperties/properties.html").render(context)
            with open(NETWORK_PROPERTIES_COMPUTATIONS_DIR + "/" + self.task.operational_directory +
                            "/" + NETWORK_RESULT_VIEW_FILE_NAME, "w") as f:
                f.write(rendered_view)
            # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
            # self.__set_task_finished()
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