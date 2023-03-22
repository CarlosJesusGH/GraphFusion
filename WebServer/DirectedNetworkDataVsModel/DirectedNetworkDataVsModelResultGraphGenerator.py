__author__ = 'carlos garcia-hernandez'

from DirectedNetworkPairwise.DirectedNetworkPairwiseResult import get_all_results
from .settings import DATA_VS_MODEL_COMPUTATIONS_DIR
from DirectedNetworkPairwise.settings import RESULT_FILES

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import logging

LOGGER = logging.getLogger(__name__)


class DirectedNetworkDataVsModelResultGraphGenerator:
    def __init__(self, task, models):
        self.task = task
        self.models = models
        self.operational_dir = DATA_VS_MODEL_COMPUTATIONS_DIR + "/" + self.task.operational_directory

    def __group_models(self, result):
        groupings = {}
        reversed_mappings = {v: k for k, v in result.mapping.items()}
        for model_name, number_of_models in self.models:
            groupings[model_name] = []
            # print("*** result.net_2", result.net_2)
            # print("*** reversed_mappings", reversed_mappings)
            for i in range(1, number_of_models + 1):
                groupings[model_name].append(
                    result.hashed_matrix[
                        (result.net_2[0].split("/")[-1], reversed_mappings[model_name + "_" + str(i)].split("/")[-1])])
        return groupings

    @classmethod
    def __get_min_max_average(cls, data):
        min = float(data[0])
        max = float(data[0])
        running_total = 0
        for x in data:
            x = float(x)
            if x < min:
                min = x
            elif x > max:
                max = x
            running_total += x
        return min, max, running_total / len(data)

    @classmethod
    def __get_data_for_graph(cls, data):
        y_err_min = []
        y_err_max = []
        y = []
        x = []
        i = 1
        for x_label, points in data.items():
            x.append(i)
            i += 1
            y_err_min.append(points[2] - points[0])
            y_err_max.append(points[1] - points[2])
            y.append(points[2])
        return x, y, y_err_min, y_err_max

    def __save_image_for_graph_data(self, f_name, data):
        fig = plt.figure()
        sub_plot = fig.add_subplot(111)
        points = []
        x_labels = []
        for k, v in data.items():
            x_labels.append(k)
            points.append(map(float, v))
        sub_plot.boxplot(points)
        xtick_names = plt.setp(sub_plot, xticklabels=x_labels)
        plt.setp(xtick_names)
        sub_plot.set_title(RESULT_FILES[f_name])
        fig.savefig(self.operational_dir + "/" + f_name.replace("txt", "png"))

    def generate_graph_images(self):
        results = get_all_results(task=self.task, directory=DATA_VS_MODEL_COMPUTATIONS_DIR)
        groupings = []
        for result in results:
            grouped_data = self.__group_models(result)
            self.__save_image_for_graph_data(f_name=result.f_name, data=grouped_data)
        LOGGER.info(str(groupings))

