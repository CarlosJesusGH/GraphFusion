__author__ = 'varun'


class ListToLeda:
    def __init__(self, graph_list):
        self.graph_list = graph_list

    @classmethod
    def __get_graph_in_leda_format(cls, list_of_interactions, list_of_nodes, node_indexes, is_directed=False):
        result = ""
        result += 'LEDA.GRAPH\n'
        result += 'string\n'
        result += 'short\n'
        result += "-1\n" if is_directed else "-2\n"
        result += str(len(list_of_nodes)) + '\n'
        for node in list_of_nodes:
            result += '|{' + node + '}|\n'
        result += str(len(list_of_interactions)) + '\n'
        for edge in list_of_interactions:
            result += str(node_indexes[edge[0]]) + ' ' + str(node_indexes[edge[1]]) + ' 0 |{}|\n'
        return result

    def convert_to_leda(self):
        list_of_interactions = []
        list_of_nodes = []
        node_indexes = {}
        for line in self.graph_list.split("\n"):
            if line:
                tokens = line.strip().split()
                if tokens[0] != tokens[1]:
                    list_of_interactions.append((tokens[0], tokens[1]))

        node_count = 1
        for interaction in list_of_interactions:
            if interaction[0] not in node_indexes:
                list_of_nodes.append(interaction[0])
                node_indexes[interaction[0]] = node_count
                node_count += 1

            if interaction[1] not in node_indexes:
                list_of_nodes.append(interaction[1])
                node_indexes[interaction[1]] = node_count
                node_count += 1
        return self.__get_graph_in_leda_format(list_of_interactions, list_of_nodes, node_indexes)