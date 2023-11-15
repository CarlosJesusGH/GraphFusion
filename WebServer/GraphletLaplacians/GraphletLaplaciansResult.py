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

from django.template import Context
from django.template.loader import get_template
from .settings import *
from utils.SystemCall import make_system_call
from utils.ImageParser import get_string_for_svg

LOGGER = logging.getLogger(__name__)

def compute_template_extra_task(op_dir, fact_name):
    sys_call_result = make_system_call("bash " + PSB_MATCOMP_SCRIPT_PATH + " " + op_dir + " " + fact_name + " " + PSB_MATCOMP_OUT_FILES[0] + " " + PSB_MATCOMP_OUT_FILES[1] + " " + PSB_MATCOMP_ENTITYLIST_ROWS + " " + PSB_MATCOMP_ENTITYLIST_COLS, working_dir=op_dir)
    print("sys_call_result", sys_call_result)
    psb_matcomp_img = []
    if os.path.isfile(os.path.join(op_dir, PSB_MATCOMP_OUT_FILES[0])):
        psb_matcomp_img.append('{0}'.format(get_string_for_svg(os.path.join(op_dir, PSB_MATCOMP_OUT_FILES[0]))))
    return psb_matcomp_img

def get_all_results(task):
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

class GraphletLaplaciansResult:
    def __init__(self, title, fact):
        self.title = title
        self.fact = fact
        self.counter = fact["counter"]
        self.props = []
        for key in fact.keys():
            self.props.append((key, fact[key]))


    # def get_graph_image(self):
    #     return self.result_graph

    def get_properties(self):
        return self.props

    def get_title(self):
        return self.title

    def get_counter(self):
        return self.counter

    def get_output_files(self):
        return 
