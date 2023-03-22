__author__ = 'varun'

import logging

from .AlignmentRunner import InvalidConstructionError, make_system_call, AlignmentRunnerException
from NetworkAlignment.settings import MI_GRAAL_PATH
from .ORCAAlignmentRunner import ORCAAlignmentRunner


LOGGER = logging.getLogger(__name__)


class MIGRAALRunner(ORCAAlignmentRunner):
    def __init__(self, user, graph1=None, graph2=None, graph1_name=None, graph2_name=None, cost_matrix=1, name=""):
        if graph1 is None or graph2 is None:
            raise InvalidConstructionError("No Task ID Given")
        ORCAAlignmentRunner.__init__(self, name=name, graph1_name=graph1_name, graph2_name=graph2_name, graph1=graph1,
                                     graph2=graph2, user=user)
        self.cost_matrix = cost_matrix

    def run_alignment_algorithm(self):
        LOGGER.info("Running MI-GRAAL")
        result = make_system_call(MI_GRAAL_PATH + " " + self.get_path_for_graph_1() + " " +
                                  self.get_path_for_graph_2() + " " + self.get_path_for_graph_1() + ".res.ndump2 " +
                                  self.get_path_for_graph_2() + ".res.ndump2 " +
                                  self.RESULT_FILE_NAME + " -p " + str(self.cost_matrix)
                                  , working_dir=self.operational_dir)
        if "Done" not in result.stdout:
            raise AlignmentRunnerException(
                "Error Occurred while running GRAAL. Output from GRAAL: " + str(result.stdout))