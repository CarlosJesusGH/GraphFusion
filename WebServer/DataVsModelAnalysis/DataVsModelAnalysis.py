__author__ = 'varun'
"""
This file is used for Data Vs Model Analysis. Change __get_model_generator method to add further models.
Any new model generators should extend the abstract class 'AbstractGraphModelGenerator' and should override get_graph
method where a NetworkX graph object should be returned.
"""

from datetime import datetime
import logging
import traceback

import networkx as nx

from .GeoGDGraphModelGenerator import GeoGDGraphModelModelModelGenerator
from .GeometricGraphModelGenerator import GeometricGraphModelGenerator
from .SFGDGraphModelGenerator import SFGDGraphModelGenerator
from .SFGraphModelGenerator import SFGraphModelGenerator
from .ERGraphModelGenerator import ERGraphModelModelGenerator
from .StickyGraphModelGenerator import StickyGraphModelGenerator
from .DataVsModelResultGraphGenerator import DataVsModelResultGraphGenerator
from PairwiseAnalysis.PairwiseAnalysis import PairwiseAnalysis
from TaskFactory.ParallelComputationExecutor import ParallelComputationTask
from NetworkProperties.NetworkProperties import Graph
from .settings import DATA_VS_MODEL_COMPUTATIONS_DIR, DATA_VS_MODEL_TASK


LOGGER = logging.getLogger(__name__)


class DataVsModelAnalysis(PairwiseAnalysis):
    def __init__(self, graph_content, models, task_name, user, distances):
        PairwiseAnalysis.__init__(self, graphs=[[graph_content]], user=user, task_name=task_name,
                                  distances=distances)
        self.operational_dir = DATA_VS_MODEL_COMPUTATIONS_DIR + "/" + self.task.operational_directory
        self.task.task_type = DATA_VS_MODEL_TASK
        self.task.save()
        self.graph_name = graph_content[0]
        self.graph = Graph()
        self.graph.parse_content(graph_content[1])
        self.models = models
        self.model_graphs = []
        self.nodes = self.graph.nodes()
        self.number_of_nodes = len(self.nodes)
        self.number_of_edges = len(self.graph.edges())

    def __get_model_generator(self, model_name):
        if model_name == "GEO":
            return GeometricGraphModelGenerator(number_of_nodes=self.number_of_nodes,
                                                number_of_edges=self.number_of_edges,
                                                bin_count=10)
        if model_name == "GEOGD":
            return GeoGDGraphModelModelModelGenerator(number_of_nodes=self.number_of_nodes,
                                                      number_of_edges=self.number_of_edges,
                                                      bin_count=10)
        if model_name == "SF":
            return SFGraphModelGenerator(number_of_nodes=self.number_of_nodes,
                                         number_of_edges=self.number_of_edges)
        if model_name == "SFGD":
            return SFGDGraphModelGenerator(number_of_nodes=self.number_of_nodes,
                                           number_of_edges=self.number_of_edges)
        if model_name == "ER":
            return ERGraphModelModelGenerator(number_of_nodes=self.number_of_nodes,
                                              number_of_edges=self.number_of_edges)
        if model_name == "Sticky":
            return StickyGraphModelGenerator(nodes=self.nodes, degrees=self.graph.degrees())

        return None

    def generate_models(self):
        LOGGER.info("Generating models for task " + str(self.task.taskId) + " ,models= " + str(self.models))
        model_generator_runnable = []
        for model_name, number_of_models in self.models:
            for i in range(1, number_of_models + 1):
                model_generator = self.__get_model_generator(model_name)
                if model_generator:
                    model_generator.model_name = model_name + "_" + str(i)
                    model_generator_runnable.append(model_generator)
        ParallelComputationTask(tasks=model_generator_runnable).run_and_wait()
        for runnable in model_generator_runnable:
            self.model_graphs.append([runnable.model_name, runnable.graph_string])
        self.graphs.insert(0, self.model_graphs)

    def run_task(self):
        try:
            self.generate_models()
            self.run_analysis()
            DataVsModelResultGraphGenerator(task=self.task, models=self.models).generate_graph_images()
        except Exception as e:
            LOGGER.error(e.message)
            LOGGER.error(traceback.format_exc())
            self.task.error_occurred = True
            self.task.error_text = e.message
            self.task.finished = True
            self.task.finished_at = datetime.now()
            self.task.save()