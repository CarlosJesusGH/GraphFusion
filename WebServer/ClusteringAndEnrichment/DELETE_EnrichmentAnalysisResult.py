__author__ = 'varun'

from .settings import *
from PIL import Image
import base64
import StringIO
import os


def get_all_enrichment_results_for_task(task):
    results = []
    for f_name, title in RESULT_IMAGE_FILES.items():
        image_path = COMPUTATIONS_DIR + "/" + task.operational_directory + "/" + f_name
        if os.path.isfile(image_path):
            results.append(EnrichmentAnalysisResult(title=title, graph_file_path=image_path))
    return results


def get_string_for_png(file_path):
    output = StringIO.StringIO()
    im = Image.open(file_path)
    im.save(output, format='PNG')
    output.seek(0)
    output_s = output.read()
    b64 = base64.b64encode(output_s)
    return '{0}'.format(b64)


class EnrichmentAnalysisResult:
    def __init__(self, title, graph_file_path):
        self.title = title
        self.result_graph = get_string_for_png(graph_file_path)

    def get_graph_image(self):
        return self.result_graph

    def get_title(self):
        return self.title