__author__ = 'varun'

from abc import abstractmethod, ABCMeta
from cStringIO import StringIO
from TaskFactory.ParallelComputationExecutor import Runnable


class AbstractGraphModelGenerator(Runnable):
    __metaclass__ = ABCMeta

    def __init__(self, number_of_nodes, number_of_edges):
        Runnable.__init__(self)
        self.number_of_nodes = number_of_nodes
        self.number_of_edges = number_of_edges
        self.graph_string = None
        self.model_name = ""

    @abstractmethod
    def get_graph(self):
        pass

    @classmethod
    def __get_network_as_leda_string(cls, network):
        list_of_nodes = network.nodes()
        node_indexes = {}
        for i in range(len(list_of_nodes)):
            node_indexes[list_of_nodes[i]] = (i + 1)

        network_string = StringIO()
        network_string.write('LEDA.GRAPH\n')
        network_string.write('string\n')
        network_string.write('double\n')
        network_string.write('-2\n')
        network_string.write(str(len(list_of_nodes)) + '\n')

        for node in list_of_nodes:
            network_string.write('|{' + str(node) + '}|\n')

        network_string.write(str(network.number_of_edges()) + '\n')

        for edge in network.edges():
            network_string.write(str(node_indexes[edge[0]]) + ' ' + str(node_indexes[edge[1]]) + ' 0 |{}|\n')

        return network_string.getvalue()

    def run(self):
        self.graph_string = self.__get_network_as_leda_string(self.get_graph())