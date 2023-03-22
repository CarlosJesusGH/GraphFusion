__author__ = 'varun'

from .utils import TestAlignmentRunner, FILE_DIR
from NetworkAlignment.LGRAALRunner import LGRAALRunner


class TestLGRAALRunnerWithLedaFilesWithCostMatrixSignatureSimilarities(TestAlignmentRunner):
    graph_1_filepath = FILE_DIR + "/resources/test/graph1_leda_format.txt"
    graph_2_filepath = FILE_DIR + "/resources/test/graph2_leda_format.txt"
    sequenceSimilarityFile = FILE_DIR + "/resources/test/sequenceSimilarityEBV_EBV.txt"
    graph_1_name = "test1"
    graph_2_name = "test2"

    def setUp(self):
        TestAlignmentRunner.setUp(self)
        self.aligner = LGRAALRunner(graph1=self.get_file_as_text(self.graph_1_filepath),
                                    graph2=self.get_file_as_text(self.graph_2_filepath),
                                    graph1_name=self.graph_1_name,
                                    graph2_name=self.graph_2_name,
                                    cost_matrix=2,
                                    user=self.user,
                                    sequence_similarity=self.get_file_as_text(self.sequenceSimilarityFile))