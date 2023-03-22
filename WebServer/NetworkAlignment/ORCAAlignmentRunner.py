from abc import ABCMeta
from NetworkAlignment.AlignmentRunner import AlignmentRunner, LOGGER
from NetworkAlignment.ORCAThreadRunner import ORCAParallelRunner

__author__ = 'varun'


class ORCAAlignmentRunner(AlignmentRunner):
    __metaclass__ = ABCMeta
    RESULT_FILE_NAME = "result"

    def __init__(self, user, name, graph1, graph2, graph1_name, graph2_name):
        AlignmentRunner.__init__(self, name=name, graph1=graph1, graph2=graph2, graph1_name=graph1_name,
                                 graph2_name=graph2_name, user=user)

    def __run_orca(self):
        LOGGER.info("Running NCount in parallel")
        runner1 = ORCAParallelRunner(self.get_path_for_graph_1())
        runner2 = ORCAParallelRunner(self.get_path_for_graph_2())
        runner1.start()
        runner2.start()
        runner1.join()
        runner2.join()

    def run_algorithm(self):
        self.__run_orca()
        self.run_alignment_algorithm()

    def __save_results(self):
        LOGGER.info("Saving Results")
        self.__get_result_properties()
        self.__get_alignment()
        self.result.save_results()