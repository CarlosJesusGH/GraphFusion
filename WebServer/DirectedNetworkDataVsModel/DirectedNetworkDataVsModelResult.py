__author__ = 'varun'

from .settings import RESULT_IMAGE_FILES, DATA_VS_MODEL_COMPUTATIONS_DIR
from PIL import Image
import base64
import StringIO
import os
from utils.ImageParser import get_string_for_svg


def get_all_results_for_task(task):
    results = []
    for f_name, title in RESULT_IMAGE_FILES.items():
        image_path = DATA_VS_MODEL_COMPUTATIONS_DIR + "/" + task.operational_directory + "/" + f_name
        if os.path.isfile(image_path):
            results.append(DirectedNetworkDataVsModelResult(title=title, graph_file_path=image_path))
    return results


class DirectedNetworkDataVsModelResult:
    def __init__(self, title, graph_file_path):
        self.title = title
        self.result_graph = get_string_for_svg(graph_file_path)

    def get_graph_image(self):
        return self.result_graph

    def get_title(self):
        return self.title