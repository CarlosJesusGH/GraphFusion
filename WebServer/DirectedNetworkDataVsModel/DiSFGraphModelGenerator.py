__author__ = 'varun'

from .AbstractDiGraphModelGenerator import AbstractDiGraphModelGenerator
import networkx as nx
import random
import math
from networkx.generators.classic import path_graph


class DiSFGraphModelGenerator(AbstractDiGraphModelGenerator):
    def __init__(self, number_of_nodes, number_of_edges):
        AbstractDiGraphModelGenerator.__init__(self, number_of_edges=number_of_edges, number_of_nodes=number_of_nodes)

    def get_graph(self):
        # m = self.number_of_edges / self.number_of_nodes
        # return nx.barabasi_albert_graph(self.number_of_nodes, m + 1)

        n, num_of_edges = self.number_of_nodes, self.number_of_edges
        alpha, beta, gamma, delta_in, delta_out = 0.5,0,0.5,0,0
        create_using, seed = None, None

        def _choose_node(G,distribution,delta):
            cumsum=0.0
            # normalization 
            psum=float(sum(distribution.values()))+float(delta)*len(distribution)
            r=random.random()
            for i in range(0,len(distribution)):
                div = (distribution[i]+delta)/psum if psum else 0
                cumsum+=div
                if r < cumsum:  
                    break
            return i

        #find size of seed network
        B=n-(beta/float(alpha+gamma))
        D=math.pow(B, 2)-4*(num_of_edges - float(beta*n)/(alpha+gamma))
        m=int((B-math.sqrt(D))/2)
        
        #m_corr=int(float(num_of_edges-(float(beta*n)/(alpha+gamma)))/n)
        #m=int(float(num_of_edges-(float(beta*(n-m_corr))/(alpha+gamma)))/(n-m_corr))
        #print m
        if create_using is None:
            # start with 3-cycle
            
            H=path_graph(m)
            G=nx.DiGraph(H)
        else:
            # keep existing graph structure?
            G = create_using
            if not G.is_directed():
                raise nx.NetworkXError(\
                    "MultiDiGraph required in create_using")

        if alpha <= 0:
            raise ValueError('alpha must be >= 0.')
        if beta < 0:
            raise ValueError('beta must be <>=0.')
        if gamma <= 0:
            raise ValueError('beta must be >= 0.')

        if alpha+beta+gamma !=1.0:
            raise ValueError('alpha+beta+gamma must equal 1.')
            
        
        # seed random number generated (uses None as default)
        random.seed(seed)

        
        while len(G)<n:
            r = random.random()
            # random choice in alpha,beta,gamma ranges
            if r<alpha:
                # alpha
                # add new node v
                v = len(G) 
                # choose m nodes w according to in-degree and delta_in
                counter=0
                while counter<m:
                    w = _choose_node(G, G.in_degree(),delta_in)
                    if (v,w) not in G.edges():
                        G.add_edge(v,w)
                        counter=counter+1
            elif r < alpha+beta:
                # beta
                # choose v according to out-degree and delta_out
                v = _choose_node(G, G.out_degree(),delta_out)
                # choose w according to in-degree and delta_in
                w = _choose_node(G, G.in_degree(),delta_in)
                G.add_edge(v,w)
            else:
                # gamma
                w = len(G)
                # choose m nodes v according to out-degree and delta_out
                counter=0
                while counter<m:
                    v = _choose_node(G, G.out_degree(),delta_out)
                    if (v,w) not in G.edges():
                        G.add_edge(v,w)
                        counter=counter+1
        return G