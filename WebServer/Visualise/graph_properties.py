__author__ = 'varun'
from NetworkProperties.NetworkProperties import Graph
from TaskFactory.models import Task
from NetworkAlignment.AlignmentRunner import COMPUTATIONS_DIR
from .CombineGraphsForAlignment import AlignmentGraph
from NetworkAlignment.settings import NAMES_MAPPING_FILE
import networkx as nx
import os.path


def __get_edges(edges, nodes):
    result = []
    nodes = dict(nodes)
    for x, y in edges:
        result.append((nodes[x], nodes[y]))

    return result


def get_graph_nodes_and_edges(network_data):
    return get_nodes_and_edges_from_graph(get_graph_from_string(network_data))


def get_graph_from_string(network_data):
    graph = Graph()
    graph.parse_content(network_data.split("\n"))
    return graph


def get_node_colour(mapping, nodes):
    colours = ['#A1D9F7'] * len(nodes)
    if mapping:
        for i in range(0, len(nodes)):
            if mapping.has_key(nodes[i]):
                colours[i] = '#A3F58E'
            else:
                colours[i] = '#F7A1A1'
    return colours


def get_nodes_and_edges_from_graph(graph, mapping=None):
    nodes = graph.nodes()
    colours = get_node_colour(nodes=nodes, mapping=mapping)
    nodes_with_colours = zip(nodes, range(1, len(nodes) + 1), colours)
    nodes_with_id = zip(nodes, range(1, len(nodes) + 1))
    edges = __get_edges(graph.edges(), nodes_with_id)
    return nodes_with_colours, edges


def get_nodes_and_edges_for_task(task_id, user):
    task = Task.objects.get(taskId=task_id)
    if task is not None and task.user == user and task.finished:
        operational_dir = COMPUTATIONS_DIR + "/" + task.operational_directory
        alignment_file_path = operational_dir + "/alignment.gml"
        alignment = open(operational_dir + "/result.aln", "r").read()
        graph1 = get_graph_from_string(open(operational_dir + "/1", "r").read())
        graph2 = get_graph_from_string(open(operational_dir + "/2", "r").read())
        alignment_graph = AlignmentGraph(graph1=graph1, graph2=graph2, alignment=alignment)

        graph_1_nodes, graph_1_edges = get_nodes_and_edges_from_graph(graph1)
        graph_2_nodes, graph_2_edges = get_nodes_and_edges_from_graph(graph2, mapping={v: k for k, v in
                                                                                       alignment_graph.alignment.items()})

        if os.path.isfile(alignment_file_path):
            combined_network = nx.read_graphml(alignment_file_path)
        else:
            combined_network = alignment_graph.get_aligned_graph()
            nx.write_graphml(combined_network, alignment_file_path)
        alignment_nodes, alignment_edges = get_nodes_and_edges_from_graph(combined_network)
        graph_names = eval(open(operational_dir + "/" + NAMES_MAPPING_FILE, 'r').read())
        return [(1, graph_names[0], graph_1_nodes, graph_1_edges),
                (2, graph_names[1], graph_2_nodes, graph_2_edges),
                (3, "Alignment", alignment_nodes, alignment_edges)]
    return None