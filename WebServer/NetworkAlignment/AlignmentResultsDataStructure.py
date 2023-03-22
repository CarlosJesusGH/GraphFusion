__author__ = 'varun'

from django.template import Context
from django.template.loader import get_template
from .settings import RESULT_VIEW_FILE, COMPUTATIONS_DIR


def get_alignment_result_for_task(task):
    return open(COMPUTATIONS_DIR + "/" + task.operational_directory + "/" + RESULT_VIEW_FILE).read()


class AlignmentResult():
    alignment = ""
    error = ""
    properties = []
    graph1_name = ""
    graph2_name = ""
    task = ""

    def __init__(self, properties=[], alignment=[], network_1_name=None, network_2_name=None, operational_dir=""):
        self.properties = properties
        self.alignment = alignment
        self.network_1_name = network_1_name
        self.network_2_name = network_2_name
        self.operational_dir = operational_dir

    def __format_alignment_string(self):
        result = []
        if isinstance(self.alignment, str):
            for pair in self.alignment.split("\n"):
                if pair:
                    nodes = pair.split()
                    if len(nodes) == 2:
                        result.append((nodes[0], nodes[1]))
        self.alignment = result

    def has_properties(self):
        return len(self.properties) != 0

    def error_occurred(self):
        return self.error != ""

    def get_error_text(self):
        return self.error

    def get_network_1_name(self):
        return self.graph1_name

    def get_network_2_name(self):
        return self.graph2_name

    def get_properties(self):
        return self.properties

    def get_alignment(self):
        return self.alignment

    def save_results(self):
        f = open(self.operational_dir + "/" + RESULT_VIEW_FILE, "w")
        self.__format_alignment_string()
        context = Context({'result': self})
        f.write(get_template("NetworkAlignment/alignment_result.html").render(context))
        f.close()

    def __str__(self):
        return "Alignment: " + str(self.alignment) + "Properties: " + str(self.properties)
