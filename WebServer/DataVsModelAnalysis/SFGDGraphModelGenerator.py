__author__ = 'varun'

from .AbstractGraphModelGenerator import AbstractGraphModelGenerator
import random
import networkx as nx


class SFGDGraphModelGenerator(AbstractGraphModelGenerator):
    def __init__(self, number_of_nodes, number_of_edges):
        AbstractGraphModelGenerator.__init__(self, number_of_nodes=number_of_nodes, number_of_edges=number_of_edges)
        self.number_of_edges = number_of_edges
        self.number_of_nodes = number_of_nodes

    def get_graph(self):
        p = 0.5
        q = 0.5
        ec = 500
        qstep = 0
        while q >= 0 and q <= 1:
            avg_nodes = 0
            avg_edges = 0

            for i in range(ec):
                # Create the graph with an edge
                graph = nx.Graph()
                graph.add_edge(0, 1)

                for i in range(2, self.number_of_nodes):
                    RND = random.choice(graph.nodes())

                    # Add the new node
                    graph.add_node(i)

                    # Add the edge between RND and new node with probability p
                    choose_prob = random.random()

                    if choose_prob <= p:
                        graph.add_edge(i, RND)

                    # Connect the node to all the neighbours of RND
                    for neigh in graph[RND]:
                        if neigh <> i:
                            graph.add_edge(i, neigh)

                    # Mutate the new node by removing the edges
                    neighbours = graph[i].copy()

                    for neigh in neighbours:
                        if neigh <> RND:
                            choose_prob_1 = random.random()
                            choose_prob_2 = random.random()

                            if choose_prob_1 < 0.5:
                                # Remove the edge (i - neigh) with probability q
                                if choose_prob_2 < q:
                                    graph.remove_edge(i, neigh)
                            else:
                                # Remove the edge (RND - neigh) with probability q
                                if choose_prob_2 < q:
                                    graph.remove_edge(RND, neigh)

                if (0.99 * self.number_of_edges) <= graph.number_of_edges() <= (1.01 * self.number_of_edges):
                    return graph

                avg_edges += float(graph.number_of_edges()) / ec

            if avg_edges < self.number_of_edges:
                if qstep == 0:
                    qstep = -0.1
                elif qstep > 0:
                    qstep = (-1 * qstep) / 2
            else:
                if qstep == 0:
                    qstep = 0.1
                elif qstep < 0:
                    qstep = (-1 * qstep) / 2

            q += qstep
        return None