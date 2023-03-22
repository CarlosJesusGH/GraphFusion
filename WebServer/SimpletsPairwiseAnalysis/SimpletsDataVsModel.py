__author__ = 'carlos garcia-hernandez'
"""
This file is used for Data Vs Model Analysis. Change __get_model_generator method to add further models.
Any new model generators should extend the abstract class 'ModelGeneratorAbstract' and should override get_graph
method where a String graph object should be returned.
"""

from datetime import datetime
import logging
import traceback
from .SimpletsDvmResultGraphGenerator import SimpletsDvmResultGraphGenerator
from .ModelGeneratorALL import ModelGeneratorALL
import networkx as nx
from SimpletsPairwiseAnalysis import SimpletsPairwiseAnalysis
from TaskFactory.ParallelComputationExecutor import ParallelComputationTask
from .settings import *
from .scripts.getInfoFromSC import *
from utils.SystemCall import make_system_call

LOGGER = logging.getLogger(__name__)


class SimpletsDataVsModel(SimpletsPairwiseAnalysis):
    def __init__(self, graph_content, models, task_name, user, distances):
        SimpletsPairwiseAnalysis.__init__(self, graphs=[[graph_content]], user=user, task_name=task_name, distances=distances)
        self.operational_dir = COMPUTATIONS_DIR + "/" + self.task.operational_directory
        make_system_call("mkdir -p " + self.operational_dir)
        self.task.task_type = SIMPLETS_DVM_ANALYSIS_TASK
        self.task.save()
        self.graph_name = graph_content[0]
        self.models = models
        self.model_graphs = []
        self.number_of_nodes, self.number_of_edges, self.oneD_density = get_values_from_sc(list_of_lines=graph_content[1].splitlines())

    def __get_model_generator(self, model_name):
        # if model_name == "RCC":
        return ModelGeneratorALL(number_of_nodes=self.number_of_nodes,
                                    number_of_edges=self.number_of_edges,
                                    oneD_density=self.oneD_density,
                                    operational_dir=self.operational_dir,
                                    model_type=model_name)
        # if model_name == "DiGEO":
        #     return DiGeometricGraphModelGenerator(number_of_nodes=self.number_of_nodes,
        #                                         number_of_edges=self.number_of_edges,
        #                                         bin_count=10)
        # if model_name == "DiGEOGD":
        #     return DiGeoGDGraphModelModelModelGenerator(number_of_nodes=self.number_of_nodes,
        #                                               number_of_edges=self.number_of_edges,
        #                                               bin_count=10)
        # if model_name == "DiSF":
        #     return DiSFGraphModelGenerator(number_of_nodes=self.number_of_nodes,
        #                                  number_of_edges=self.number_of_edges)
        # if model_name == "DiSFGD":
        #     return DiSFGDGraphModelGenerator(number_of_nodes=self.number_of_nodes,
        #                                    number_of_edges=self.number_of_edges)
        # if model_name == "DiER":
        #     return DiERGraphModelModelGenerator(number_of_nodes=self.number_of_nodes,
        #                                       number_of_edges=self.number_of_edges)
        # 
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
            SimpletsDvmResultGraphGenerator(task=self.task, models=self.models).generate_graph_images()
        except Exception as e:
            LOGGER.error(e.message)
            LOGGER.error(traceback.format_exc())
            self.task.error_occurred = True
            self.task.error_text = e.message
            self.task.finished = True
            self.task.finished_at = datetime.now()
            self.task.save()