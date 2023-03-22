from abc import ABCMeta

from NetworkAlignment.AlignmentRunner import AlignmentRunner, LOGGER
from NetworkAlignment.ParallelRunner import ParallelRunner
from NetworkAlignment.settings import NCOUNT_PATH


__author__ = 'varun'


class NcountAlignmentRunner(AlignmentRunner):
    __metaclass__ = ABCMeta
    RESULT_FILE_NAME = "result"

    def __init__(self, name, graph1, graph2, task, graph1_name, graph2_name):
        AlignmentRunner.__init__(self, name=name, graph1=graph1, graph2=graph2, task=task, graph1_name=graph1_name,
                                 graph2_name=graph2_name)

    def __run_ncount(self):
        LOGGER.info("Running NCount in parallel")
        runner1 = ParallelRunner(
            NCOUNT_PATH + " " + self.get_path_for_graph_1() + " " + self.get_path_for_graph_1() + ".res")
        runner2 = ParallelRunner(
            NCOUNT_PATH + " " + self.get_path_for_graph_2() + " " + self.get_path_for_graph_2() + ".res")
        runner1.start()
        runner2.start()
        runner1.join()
        runner2.join()

    def run_algorithm(self):
        self.__run_ncount()
        self.run_alignment_algorithm()

    def __save_results(self):
        LOGGER.info("Saving Results")
        self.__get_result_properties()
        self.__get_alignment()
        self.result.save_results()