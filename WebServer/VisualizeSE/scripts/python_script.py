import os
import sys
import networkx as nx
from pyvis.network import Network
sys.path.append(os.path.join(sys.path[0], '..')); # print("sys.path", sys.path)
from settings import *

# from ResultsAnalysis.enrichementAnalysis import *

# ---------------------------------------------------------------
# ADD FUNCTIONS

# ---------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------
def main():
    print("flag: python main")
    print("os.getcwd()", os.getcwd())
    
    args = sys.argv[1:]
    print("args", args)

    network_name = args[0]
    directed = args[1]
    # Make directed a boolean
    directed = directed.lower() == 'true'
    print("directed", directed)
    print("type(directed)", type(directed))
    working_dir = args[2]
    network_path = working_dir + network_name

    # load network from file
    G = nx.read_edgelist(network_path) 
    
    n_nodes = len(G.nodes())
    n_edges = len(G.edges())
    print(n_nodes)
    print(n_edges)

    # Create a pyvis network
    net = Network(directed=directed) # height="1000px", width="50%"
    net.from_nx(G)

    # Triggering the toggle_physics() method allows for more fluid graph interactions
    net.toggle_physics(False)
    net.show_buttons(filter_=['physics'])
    output_file = working_dir + "/" + RESULT_VIEW_FILE
    net.save_graph(output_file)
    

if __name__ == "__main__":
    main()


