__author__ = 'varun'

from .AbstractDiGraphModelGenerator import AbstractDiGraphModelGenerator
import random
import networkx as nx


class DiSFGDGraphModelGenerator(AbstractDiGraphModelGenerator):
    def __init__(self, number_of_nodes, number_of_edges):
        AbstractDiGraphModelGenerator.__init__(self, number_of_nodes=number_of_nodes, number_of_edges=number_of_edges)
        self.number_of_edges = number_of_edges
        self.number_of_nodes = number_of_nodes

    def get_graph(self):
        # values obtained from: WebServer/DataVsModelAnalysis/SFGDGraphModelGenerator.py
        nodeCount, edgeCount, p, q, ec = self.number_of_nodes, self.number_of_edges, 0.5, 0.5, 500

        qstep = 0
        
        while q >= 0 and q <= 1:
            avg_nodes = 0
            avg_edges = 0
            
            for i in range(ec):
                # Create the graph with an edge
                graph = nx.DiGraph()
                graph.add_edge(0, 1)
                
                for i in range(2, nodeCount):
                    RND = random.choice(graph.nodes())
                    
                    # Add the new node
                    graph.add_node(i)
                    
                    # Add the edge between RND and new node with probability p, but the decide on directionality with 50% chances in favour both options
                    choose_prob = random.random()
                    if choose_prob <= p:
                                            num=random.random() #generise random broj u [0.0, 1.0), pa je dobra podjela [0.0,0.5) i [0.5,1.0)
                                            if num < 0.5:
                                                graph.add_edge(i,RND)
                                            else:
                                                graph.add_edge(RND,i)
                        
                    
                    # Connect the node 'i' to all the neighbours of RND
                    for succ in graph.successors(RND):
                        if succ <> i:
                            graph.add_edge(i, succ)
                    for pred in graph.predecessors(RND):
                        if pred <> i:
                            graph.add_edge(pred, i)
                    
                    # Mutate the new node by removing the edges
                    successors_i = graph.successors(i)
                    predecessors_i = graph.predecessors(i)
                    list_of_neigbors=list()
                    for successor in successors_i:
                                        list_of_neigbors.append(successor)
                    for predecessor in predecessors_i:
                                        list_of_neigbors.append(predecessor)

                    for neigbor in list_of_neigbors:
                        if neigbor <> RND:
                            choose_prob = random.random()
                            if choose_prob < q:
                                if neigbor in successors_i and neigbor in predecessors_i:# Remove the edge (i - sucessor) or the edge (predecessor - i) with equal probabilities
                                    num=random.random() #generise random broj u [0.0, 1.0), pa je dobra podjela [0.0,0.5) i [0.5,1.0)
                                    if num < 0.5:
                                        graph.remove_edge(i,neigbor)
                                    else:
                                        graph.remove_edge(neigbor,i)
                                else: 
                                    if neigbor in successors_i:# Remove the edge (i - sucessor)
                                        graph.remove_edge(i, neigbor)
                                    if neigbor in predecessors_i:# Remove the edge (predecessor - i)
                                        graph.remove_edge(neigbor,i)

                if graph.number_of_edges() >= (0.99 * edgeCount) and graph.number_of_edges() <= (1.01 * edgeCount):
                    return graph
                
                avg_edges += float(graph.number_of_edges()) / ec
            
            if avg_edges < edgeCount:
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
        
        print 'ERROR! No SFGD graph could be generated'
        return None