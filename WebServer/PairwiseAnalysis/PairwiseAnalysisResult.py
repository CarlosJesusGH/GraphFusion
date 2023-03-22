__author__ = 'varun'

from .settings import PAIRWISE_ANALYSIS_COMPUTATIONS_DIR, RESULT_FILES, NAMES_MAPPING_FILE, NAMES_OF_NETWORKS_LIST_FILES
import ast
import os


def get_all_results(task, directory):
    operational_directory = directory + "/" + task.operational_directory + "/"
    with open(operational_directory + NAMES_MAPPING_FILE, "r") as mappings_file:
        mappings = ast.literal_eval(mappings_file.read())
    net_1 = None
    if os.path.isfile(operational_directory + NAMES_OF_NETWORKS_LIST_FILES[0]):
        with open(operational_directory + NAMES_OF_NETWORKS_LIST_FILES[0], "r") as f:
            net_1 = ast.literal_eval(f.read())
    net_2 = None
    if os.path.isfile(operational_directory + NAMES_OF_NETWORKS_LIST_FILES[1]):
        with open(operational_directory + NAMES_OF_NETWORKS_LIST_FILES[1], "r") as f:
            net_2 = ast.literal_eval(f.read())
    result = []
    for f_name, result_name in RESULT_FILES.items():
        file_path = operational_directory + f_name
        if os.path.isfile(file_path):
            result.append(
                PairwiseAnalysisResult(
                    mapping=mappings,
                    title=result_name,
                    file_path=file_path,
                    f_name=f_name,
                    net_1=net_1,
                    net_2=net_2))
    return result


def get_all_pairwise_analysis_results(task):
    return get_all_results(task, PAIRWISE_ANALYSIS_COMPUTATIONS_DIR)


class PairwiseAnalysisResult:
    def __init__(self, title, mapping, file_path, f_name, net_1, net_2):
        self.net_1 = net_1
        self.net_2 = net_2
        self.title = title
        self.mapping = mapping
        self.f_name = f_name
        self.hashed_matrix = {}
        self.heading, self.rows = self.get_matrix_from_file(file_path=file_path)

    def get_title(self):
        return self.title

    def get_heading(self):
        return self.heading

    def get_rows(self):
        return self.rows

    def get_matrix_from_file(self, file_path):
        result = []
        f = open(file_path, "r")
        lines = f.readlines()
        heading = self.__get_heading(heading_from_file=lines[0])
        self.hashed_matrix = self.__get_hash_map_for_matrix(lines)
        if self.net_1:
            for net1 in self.net_1:
                row = [self.mapping[net1]]
                for net2 in self.net_2:
                    row.append(self.hashed_matrix[(net1, net2)])
                result.append(row)
        else:
            for i in range(1, len(lines)):
                tokens = lines[i].split()
                tokens[0] = self.mapping[tokens[0]]
                result.append(tokens)
        return heading, result

    def __get_heading(self, heading_from_file):
        heading = [""]
        if self.net_2:
            for net in self.net_2:
                heading.append(self.mapping[net])
        else:
            heading += map(lambda x: self.mapping[x], heading_from_file.split())
        return heading


    @classmethod
    def __get_hash_map_for_matrix(cls, lines):
        lines = map(lambda x: x.split(), lines)
        result = {}
        for i in range(1, len(lines)):
            for j in range(1, len(lines)):
                result[(lines[i][0], lines[j][0])] = lines[i][j]
        return result