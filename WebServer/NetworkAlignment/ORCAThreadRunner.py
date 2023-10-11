__author__ = 'varun'

import threading
import logging

import os

from NetworkAlignment.settings import ORCA_PATH

from NetworkAlignment.AlignmentRunner import AlignmentRunnerException
from utils.SystemCall import make_system_call


LOGGER = logging.getLogger(__name__)


class ORCAExecutable:
    def __init__(self, file_path):
        self.file_path = file_path
        if '.' in file_path:
            file_name = file_path.split(".")[0]
        else:
            file_name = file_path
        self.output_file_name = file_name + '_orca.txt'
        self.temp_n_dump_2_file = file_name + '_temp.ndump2'
        self.original_n_dump_2 = file_name + '.res.ndump2'

    def read_leda(self):
        # g = Graph()
        # g.parse_content(open(self.file_path).read().split("\n"))
        # return g.nodes(), g.edges()
        node_list = []
        edge_list = []
        f_read = open(self.file_path, 'r')
        mode = 0

        for line in f_read:
            if mode == 0 and line.startswith('|'):
                mode = 1
            if mode == 1 and line.startswith('|'):
                node_list.append(line.strip().strip('|').strip('{').strip('}'))
            elif mode == 1 and not line.startswith('|'):
                mode = 2
            elif mode == 2 and line.strip().endswith('}|'):
                tokens = line.strip().split(' ')
                edge_list.append([int(tokens[0]) - 1, int(tokens[1]) - 1])
        f_read.close()
        return node_list, edge_list

    def write_orca(self, edge_list, node_count):
        # print("log - write_orca", edge_list, node_count)
        f_write = open(self.output_file_name, 'w')
        f_write.write(str(node_count) + ' ' + str(len(edge_list)) + '\n')

        for edge in edge_list:
            f_write.write(str(edge[0]) + ' ' + str(edge[1]) + '\n')
        f_write.close()

    def format_n_dump(self, node_list):
        f_read = open(self.temp_n_dump_2_file, 'r')
        f_write = open(self.original_n_dump_2, 'w')
        line_id = 0
        for line in f_read:
            f_write.write(str(node_list[line_id]) + ' ' + line)
            line_id += 1
        f_read.close()
        f_write.close()

    def remove_computational_files(self):
        os.remove(self.output_file_name)
        os.remove(self.temp_n_dump_2_file)

    def __parse_gdd_count(self):
        gdd_signatures = []
        for line in open(self.temp_n_dump_2_file):
            gdd_signatures.append(line.split())
        return gdd_signatures

    def get_gdd_count(self):
        LOGGER.info("Running GDD computation using ORCA for " + str(self.file_path))
        node_list, edge_list = self.read_leda()
        self.write_orca(edge_list, len(node_list))

        result = make_system_call(ORCA_PATH + ' 5 ' + self.output_file_name + ' ' + self.temp_n_dump_2_file)
        if result.return_code != 0: # or result.stderr:
            raise AlignmentRunnerException("Error while running parallel runner for ORCA: " + str(result.stderr))
        return self.__parse_gdd_count()

    def run(self):
        LOGGER.info("Running ORCA for " + str(self.file_path))
        node_list, edge_list = self.read_leda()
        # print("log - node_list", node_list, "edge_list", edge_list)
        self.write_orca(edge_list, len(node_list))

        result = make_system_call(ORCA_PATH + ' 5 ' + self.output_file_name + ' ' + self.temp_n_dump_2_file)
        print("log - orca result", result)
        if result.return_code != 0:# or result.stderr:
            print("log - orca ERROR", result.stderr)
            # os.remove(self.original_n_dump_2)
            raise AlignmentRunnerException("Error while running parallel runner for ORCA: " + str(result.stderr))
            # raise Exception("Error while running parallel runner for ORCA: " + str(result.stderr))
        self.format_n_dump(node_list)
        self.remove_computational_files()


class ORCAParallelRunner(threading.Thread):
    def __init__(self, file_path):
        threading.Thread.__init__(self)
        self.orca_executable = ORCAExecutable(file_path=file_path)

    def run(self):
        self.orca_executable.run()

