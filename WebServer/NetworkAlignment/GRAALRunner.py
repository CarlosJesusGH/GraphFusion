from NetworkAlignment.AlignmentRunner import InvalidConstructionError, LOGGER, make_system_call, \
    AlignmentRunnerException
from NetworkAlignment.settings import GRAAL_PATH
from .ORCAAlignmentRunner import ORCAAlignmentRunner

__author__ = 'varun'


class GRAALRunner(ORCAAlignmentRunner):
    def __init__(self, user, alpha=0, graph1=None, graph2=None, graph1_name=None, graph2_name=None, seed=None, name=""):
        if graph1 is None or graph2 is None:
            raise InvalidConstructionError("No Task ID Given")
        ORCAAlignmentRunner.__init__(self, name=name,
                                     graph1_name=graph1_name, graph2_name=graph2_name, graph1=graph1, graph2=graph2,
                                     user=user)
        self.alpha = alpha
        self.seed = None if seed is None or seed == "" else int(seed)

    def run_alignment_algorithm(self):
        LOGGER.info("Running GRAAL")
        seed_value_option = "" if self.seed is None else " -s " + str(self.seed)
        result = make_system_call(GRAAL_PATH + " " + str(self.alpha) + " " + self.get_path_for_graph_1() + " " +
                                  self.get_path_for_graph_2() + " " + self.get_path_for_graph_1() + ".res.ndump2 " +
                                  self.get_path_for_graph_2() + ".res.ndump2 " + self.RESULT_FILE_NAME
                                  + seed_value_option, working_dir=self.operational_dir)
        LOGGER.info("GRAAL Output: " + result.stdout)
        if "Done" not in result.stdout:
            raise AlignmentRunnerException(
                "Error Occurred while running GRAAL. Output from GRAAL: " + str(result.stdout))