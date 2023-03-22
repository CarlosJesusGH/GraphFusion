__author__ = 'varun'

from .utils import TestAlignmentRunner, FILE_DIR
from NetworkAlignment.GRAALRunner import GRAALRunner


class TestGRAALRunnerWithLedaFiles(TestAlignmentRunner):
    graph_1_filepath = FILE_DIR + "/resources/test/graph1_leda_format.txt"
    graph_2_filepath = FILE_DIR + "/resources/test/graph2_leda_format.txt"
    graph_1_name = "test1"
    graph_2_name = "test2"

    def setUp(self):
        TestAlignmentRunner.setUp(self)
        self.aligner = GRAALRunner(graph1=self.get_file_as_text(self.graph_1_filepath),
                                   graph2=self.get_file_as_text(self.graph_2_filepath),
                                   graph1_name=self.graph_1_name,
                                   graph2_name=self.graph_2_name,
                                   alpha=0.8,
                                   user=self.user)


class TestGRAALRunnerWithListFiles(TestAlignmentRunner):
    graph_1_filepath = FILE_DIR + "/resources/test/EBV.txt"
    graph_2_filepath = FILE_DIR + "/resources/test/EBV.txt"
    graph_1_name = "EBV"
    graph_2_name = "EBV"

    def setUp(self):
        TestAlignmentRunner.setUp(self)
        self.aligner = GRAALRunner(graph1=self.get_file_as_text(self.graph_1_filepath),
                                   graph2=self.get_file_as_text(self.graph_2_filepath),
                                   graph1_name=self.graph_1_name,
                                   graph2_name=self.graph_2_name,
                                   alpha=0.2,
                                   user=self.user)


class TestGRAALRunnerWithMixFiles(TestAlignmentRunner):
    graph_1_filepath = FILE_DIR + "/resources/test/VZV.txt"
    graph_2_filepath = FILE_DIR + "/resources/test/graph2_leda_format.txt"
    graph_1_name = "VZV"
    graph_2_name = "test2"

    def setUp(self):
        TestAlignmentRunner.setUp(self)
        self.aligner = GRAALRunner(graph1=self.get_file_as_text(self.graph_1_filepath),
                                   graph2=self.get_file_as_text(self.graph_2_filepath),
                                   graph1_name=self.graph_1_name,
                                   graph2_name=self.graph_2_name,
                                   alpha=0.5,
                                   user=self.user)