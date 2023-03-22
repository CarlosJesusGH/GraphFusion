__author__ = 'varun'

from .settings import CANONICAL_CORRELATION_COMPUTATIONS_DIR, CCA_RESULT_FIGURE_PREFIX
from PIL import Image
import base64
import StringIO
import os
from fnmatch import fnmatch


def get_all_results(task):
    results = []
    op_dir = CANONICAL_CORRELATION_COMPUTATIONS_DIR + "/" + task.operational_directory

    i = 1
    while i != 11:
        name = CCA_RESULT_FIGURE_PREFIX + str(i) + ".png"
        if os.path.isfile(os.path.join(op_dir, name)):
            results.append(
                CanonicalAnalysisResult(title="Result " + str(i), graph_file_path=os.path.join(op_dir, name)))
        else:
            break
        i += 1

    return results, (i == 11 and os.path.isfile(os.path.join(op_dir, CCA_RESULT_FIGURE_PREFIX + "11.png")))


def get_all_downloadable_results(task):
    results = []
    op_dir = CANONICAL_CORRELATION_COMPUTATIONS_DIR + "/" + task.operational_directory
    pattern = CCA_RESULT_FIGURE_PREFIX + "*.png"
    for path, _, files in os.walk(op_dir):
        for name in files:
            if fnmatch(name, pattern):
                results.append((name, open(os.path.join(path, name)).read()))
    return results


def get_string_for_png(file_path):
    output = StringIO.StringIO()
    im = Image.open(file_path)
    im.save(output, format='PNG')
    output.seek(0)
    output_s = output.read()
    b64 = base64.b64encode(output_s)
    return '{0}'.format(b64)


class CanonicalAnalysisResult:
    def __init__(self, title, graph_file_path):
        self.title = title
        self.result_graph = get_string_for_png(graph_file_path)

    def get_graph_image(self):
        return self.result_graph

    def get_title(self):
        return self.title