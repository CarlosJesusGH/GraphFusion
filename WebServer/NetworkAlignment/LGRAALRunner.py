__author__ = 'varun'

import logging

from .AlignmentRunner import InvalidConstructionError, make_system_call, AlignmentRunnerException
from NetworkAlignment.settings import L_GRAAL_PATH
from .ORCAAlignmentRunner import ORCAAlignmentRunner


LOGGER = logging.getLogger(__name__)


class LGRAALRunner(ORCAAlignmentRunner):
    def __init__(self, user, graph1=None, graph2=None, graph1_name=None, graph2_name=None, sequence_similarity=None,
                 name=""):
        if graph1 is None or graph2 is None or sequence_similarity is None:
            raise InvalidConstructionError("No Task ID Given")
        ORCAAlignmentRunner.__init__(self, graph1_name=graph1_name, graph2_name=graph2_name, graph1=graph1,
                                     graph2=graph2, user=user, name=name)
        self.sequence_similarity_file_path = self.operational_dir + "/sequenceSimilarity.txt"
        f = open(self.sequence_similarity_file_path, "w")
        f.write(sequence_similarity)
        f.close()

    def run_alignment_algorithm(self):
        LOGGER.info("Running MI-GRAAL")
        result = make_system_call(
            L_GRAAL_PATH + " -Q " + self.get_path_for_graph_1() + " -T " + self.get_path_for_graph_2() + " -q " +
            self.get_path_for_graph_1() + ".res.ndump2 -t " + self.get_path_for_graph_2() + ".res.ndump2 -B " +
            self.sequence_similarity_file_path + " -o " + self.RESULT_FILE_NAME + ".aln"
            , working_dir=self.operational_dir)
        if len(open(self.operational_dir + "/" + self.RESULT_FILE_NAME + ".aln").read().strip()) == 0:
            raise AlignmentRunnerException(
                "Error Occurred while running GRAAL. Output from GRAAL: " + str(result.stdout))