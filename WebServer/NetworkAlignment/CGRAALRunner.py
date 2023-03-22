from NetworkAlignment.AlignmentRunner import InvalidConstructionError, LOGGER, make_system_call, AlignmentRunner, \
    AlignmentRunnerException
from NetworkAlignment.settings import C_GRAAL_PATH

__author__ = 'varun'


class CGRAALRunner(AlignmentRunner):
    def __init__(self, alpha=0, graph1=None, graph2=None, task=None, graph1_name=None, graph2_name=None):
        if task is None or graph1 is None or graph2 is None:
            raise InvalidConstructionError("No Task ID Given")
        AlignmentRunner.__init__(self, name="Alignment Task: " + graph1_name + "-" + graph2_name,
                                 graph1_name=graph1_name, graph2_name=graph2_name, graph1=graph1, graph2=graph2,
                                 task=task)
        self.alpha = alpha

    def run_algorithm(self):
        self.run_alignment_algorithm()

    def run_alignment_algorithm(self):
        LOGGER.info("Running CGRAAL")
        result = make_system_call(C_GRAAL_PATH + " " + str(self.alpha) + " " + self.get_path_for_graph_1() + " " +
                                  self.get_path_for_graph_2() + " " + self.get_path_for_graph_1() + ".res.ndump2 " +
                                  self.get_path_for_graph_2() + ".res.ndump2 " + self.RESULT_FILE_NAME
                                  , working_dir=self.operational_dir)
        if "Done" not in result.stdout:
            raise AlignmentRunnerException(
                "Error Occurred while running C-GRAAL. Output from C-GRAAL: " + str(result.stdout))