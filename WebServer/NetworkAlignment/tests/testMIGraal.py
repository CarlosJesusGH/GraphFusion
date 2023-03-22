__author__ = 'varun'

from .utils import TestAlignmentRunner, FILE_DIR
from NetworkAlignment.MIGRAALRunner import MIGRAALRunner


class TestMIGRAALRunnerWithLedaFilesWithCostMatrixSignatureSimilarities(TestAlignmentRunner):
    graph_1_filepath = FILE_DIR + "/resources/test/graph1_leda_format.txt"
    graph_2_filepath = FILE_DIR + "/resources/test/graph2_leda_format.txt"
    graph_1_name = "test1"
    graph_2_name = "test2"

    def setUp(self):
        TestAlignmentRunner.setUp(self)
        self.aligner = MIGRAALRunner(graph1=self.get_file_as_text(self.graph_1_filepath),
                                     graph2=self.get_file_as_text(self.graph_2_filepath),
                                     graph1_name=self.graph_1_name,
                                     graph2_name=self.graph_2_name,
                                     cost_matrix=2,
                                     user=self.user)


class TestMIGRAALRunnerWithListFilesWithCostMatrixSignatureSimilarities(TestAlignmentRunner):
    graph_1_filepath = FILE_DIR + "/resources/test/VZV.txt"
    graph_2_filepath = FILE_DIR + "/resources/test/VZV.txt"
    graph_1_name = "VZV"
    graph_2_name = "VZV"

    def setUp(self):
        TestAlignmentRunner.setUp(self)
        self.aligner = MIGRAALRunner(graph1=self.get_file_as_text(self.graph_1_filepath),
                                     graph2=self.get_file_as_text(self.graph_2_filepath),
                                     graph1_name=self.graph_1_name,
                                     graph2_name=self.graph_2_name,
                                     cost_matrix=2,
                                     user=self.user)


class TestMIGRAALRunnerWithMixFilesWithCostMatrixSignatureSimilarities(TestAlignmentRunner):
    graph_1_filepath = FILE_DIR + "/resources/test/VZV.txt"
    graph_2_filepath = FILE_DIR + "/resources/test/graph2_leda_format.txt"
    graph_1_name = "VZV"
    graph_2_name = "VZV"

    def setUp(self):
        TestAlignmentRunner.setUp(self)
        self.aligner = MIGRAALRunner(graph1=self.get_file_as_text(self.graph_1_filepath),
                                     graph2=self.get_file_as_text(self.graph_2_filepath),
                                     graph1_name=self.graph_1_name,
                                     graph2_name=self.graph_2_name,
                                     cost_matrix=2,
                                     user=self.user)


class TestMIGRAALRunnerWithLedaFilesWithCostMatrixDegrees(TestAlignmentRunner):
    graph_1_filepath = FILE_DIR + "/resources/test/graph1_leda_format.txt"
    graph_2_filepath = FILE_DIR + "/resources/test/graph2_leda_format.txt"
    graph_1_name = "test1"
    graph_2_name = "test2"

    def setUp(self):
        TestAlignmentRunner.setUp(self)
        self.aligner = MIGRAALRunner(graph1=self.get_file_as_text(self.graph_1_filepath),
                                     graph2=self.get_file_as_text(self.graph_2_filepath),
                                     graph1_name=self.graph_1_name,
                                     graph2_name=self.graph_2_name,
                                     cost_matrix=2,
                                     user=self.user)


class TestMIGRAALRunnerWithLedaFilesWithCostMatrixClusteringCoefficients(TestAlignmentRunner):
    graph_1_filepath = FILE_DIR + "/resources/test/graph1_leda_format.txt"
    graph_2_filepath = FILE_DIR + "/resources/test/graph2_leda_format.txt"
    graph_1_name = "test1"
    graph_2_name = "test2"

    def setUp(self):
        TestAlignmentRunner.setUp(self)
        self.aligner = MIGRAALRunner(graph1=self.get_file_as_text(self.graph_1_filepath),
                                     graph2=self.get_file_as_text(self.graph_2_filepath),
                                     graph1_name=self.graph_1_name,
                                     graph2_name=self.graph_2_name,
                                     cost_matrix=4,
                                     user=self.user)


class TestMIGRAALRunnerWithLedaFilesWithCostMatrixEccentricities(TestAlignmentRunner):
    graph_1_filepath = FILE_DIR + "/resources/test/graph1_leda_format.txt"
    graph_2_filepath = FILE_DIR + "/resources/test/graph2_leda_format.txt"
    graph_1_name = "test1"
    graph_2_name = "test2"

    def setUp(self):
        TestAlignmentRunner.setUp(self)
        self.aligner = MIGRAALRunner(graph1=self.get_file_as_text(self.graph_1_filepath),
                                     graph2=self.get_file_as_text(self.graph_2_filepath),
                                     graph1_name=self.graph_1_name,
                                     graph2_name=self.graph_2_name,
                                     cost_matrix=8,
                                     user=self.user)


class TestMIGRAALRunnerWithLedaFilesWithCostBetweennessCentralities(TestAlignmentRunner):
    graph_1_filepath = FILE_DIR + "/resources/test/graph1_leda_format.txt"
    graph_2_filepath = FILE_DIR + "/resources/test/graph2_leda_format.txt"
    graph_1_name = "test1"
    graph_2_name = "test2"

    def setUp(self):
        TestAlignmentRunner.setUp(self)
        self.aligner = MIGRAALRunner(graph1=self.get_file_as_text(self.graph_1_filepath),
                                     graph2=self.get_file_as_text(self.graph_2_filepath),
                                     graph1_name=self.graph_1_name,
                                     graph2_name=self.graph_2_name,
                                     cost_matrix=32,
                                     user=self.user)