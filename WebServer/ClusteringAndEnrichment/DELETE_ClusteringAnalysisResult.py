__author__ = 'carlos garcia-hernandez'

import os
import pickle
from fnmatch import fnmatch
# import h5py
import numpy as np
import logging
from PIL import Image
import base64
import StringIO
import csv
import ast

from django.template import Context
from django.template.loader import get_template
from .settings import *
from utils.SystemCall import make_system_call

LOGGER = logging.getLogger(__name__)

def compute_template_extra_task(op_dir, fact_name):
    sys_call_result = make_system_call("bash " + PSB_MATCOMP_SCRIPT_PATH + " " + op_dir + " " + fact_name + " " + PSB_MATCOMP_OUT_FILES[0] + " " + PSB_MATCOMP_OUT_FILES[1] + " " + PSB_MATCOMP_ENTITYLIST_ROWS + " " + PSB_MATCOMP_ENTITYLIST_COLS, working_dir=op_dir)
    print("sys_call_result", sys_call_result)
    psb_matcomp_img = []
    if os.path.isfile(os.path.join(op_dir, PSB_MATCOMP_OUT_FILES[0])):
        psb_matcomp_img.append('{0}'.format(get_string_for_png(os.path.join(op_dir, PSB_MATCOMP_OUT_FILES[0]))))
    return psb_matcomp_img

def get_all_results_simple(task):
    op_dir = COMPUTATIONS_DIR + "/" + task.operational_directory + "/"
    with open(op_dir + RESULT_FILES[0], 'rb') as f:
        reader = csv.reader(f, delimiter='\t')
        table_values = []
        for i,row in enumerate(reader):
            if i > 0:
                table_values.append((row[0], row[1], row[2]))
    if False: # if want it sorted
        table_values = sorted(table_values, key=lambda tup: tup[2], reverse=True)
    max_rows = 50
    if len(table_values) > max_rows:
        table_values = table_values[0:max_rows]
    return table_values, [output[0] for output in get_all_downloadable_results(task)]

def get_string_for_png(file_path):
    output = StringIO.StringIO()
    im = Image.open(file_path)
    im.save(output, format='PNG')
    output.seek(0)
    output_s = output.read()
    b64 = base64.b64encode(output_s)
    return '{0}'.format(b64)

def get_all_downloadable_results(task):
    results = []
    op_dir = COMPUTATIONS_DIR + "/" + task.operational_directory
    for r_file in RESULT_FILES:
        if r_file.endswith("*"):
            pattern = r_file
            for path, _, files in os.walk(op_dir):
                for name in files:
                    if fnmatch(name, pattern):
                        results.append((name, open(os.path.join(path, name)).read()))
        else:
            file_path = COMPUTATIONS_DIR + "/" + task.operational_directory + "/" + r_file
            if os.path.isfile(file_path):
                results.append([r_file, open(file_path).read()])
    return results


def get_result_for_task(task):
    # from networkalignment
    return open(COMPUTATIONS_DIR + "/" + task.operational_directory + "/" + RESULT_VIEW_FILE).read()

def get_all_pairwise_analysis_results(task):
    return get_all_results(task, COMPUTATIONS_DIR)

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
                ClusteringAnalysisResult(
                    mapping=mappings,
                    title=result_name,
                    file_path=file_path,
                    f_name=f_name,
                    net_1=net_1,
                    net_2=net_2))
    return result

class ClusteringAnalysisResult:
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
        lines = f.read().splitlines()
        # lines = map(lambda x: x.split('\t'), lines)
        # print("*** lines", lines)
        heading = self.__get_heading(heading_from_file=lines[0])
        # print("*** heading", heading)
        self.hashed_matrix = self.__get_hash_map_for_matrix(lines)
        # print("*** self.hashed_matrix",self.hashed_matrix)
        # print("*** self.net_1", self.net_1)
        # print("*** self.mapping", self.mapping)
        if self.net_1:
            for net1 in self.net_1:
                row = [self.mapping[net1]]
                for net2 in self.net_2:
                    row.append(self.hashed_matrix[(net1.split("/")[-1], net2.split("/")[-1])])
                result.append(row)
        else:
            for i in range(1, len(lines)):
                tokens = lines[i].split()
                tokens[0] = self.mapping[tokens[0]]
                result.append(tokens)
        return heading, result

    def __get_heading(self, heading_from_file):
        heading = [""]
        # print("*** heading_from_file.split", heading_from_file.split('\t'))
        if self.net_2:
            for net in self.net_2:
                heading.append(self.mapping[net])
        else:
            heading += map(lambda x: self.mapping[x], heading_from_file.split('\t'))
        return heading


    @classmethod
    def __get_hash_map_for_matrix(cls, lines):
        # print("*** in __get_hash_map_for_matrix")
        # print("*** lines", lines)
        lines = map(lambda x: x.split('\t'), lines)
        lines = map(lambda x: [item.replace('.//','') for item in x], lines)
        # print("*** lines", lines)
        result = {}
        for i in range(1, len(lines)):
            for j in range(1, len(lines)):
                result[(lines[i][0], lines[j][0])] = lines[i][j]
        return result
