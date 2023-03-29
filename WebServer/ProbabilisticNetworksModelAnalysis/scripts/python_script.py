
import os
import sys

# add path to sys
# sys.path.append(os.path.join(sys.path[0], '../psb/scripts/')); # print("sys.path", sys.path)
# from ResultsAnalysis.enrichementAnalysis import *

# ---------------------------------------------------------------
# ADD FUNCTIONS

# ---------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------
print("Hello world from python script")
operational_dir = sys.argv[1]
args = sys.argv[2:]
print("args", args)

import os
import subprocess
from inspect import currentframe

def get_linenumber():
    cf = currentframe()
    return cf.f_back.f_lineno

print("os.getcwd()", os.getcwd() + "/")
print("line:", get_linenumber(), "subprocess ls:", subprocess.check_output("ls", shell=True))

# Our packages:
# os.chdir("/home/Downloads/GC3-WWW/www/GC3Env/GC3/WebServer/ProbabilisticNetworksModelAnalysis/scripts")
os.chdir("/home/iconbi_graphcrunch/WebServer/ProbabilisticNetworksModelAnalysis/scripts")
import Network_Models

model_name = args[0]
distribution_name = args[1]
model_nodes = int(args[2])
model_radius = int(args[3])
model_density = float(args[4])
distribution_mean = float(args[5])
distribution_variance = float(args[6])
distribution_empirical_file = args[7]

if model_name == "hyper_geometric":
    # 1.1 Hyper Geometric:
    G = Network_Models.get_Hyper_Geometric(Node=model_nodes, Radius=model_radius)
elif model_name == "barabasi_albert":
    # 1.2 Barabasi
    G = Network_Models.get_m_for_barabasi_albert(Nodes=model_nodes, density=model_density)
elif model_name == "erdos_renyi":
    # 1.3 Erdos Renyi
    G = Network_Models.get_Erdos_Renyi(Nodes=model_nodes, density=model_density)
else:
    print("error model_name:", model_name)

print("len(G.nodes)", len(G.nodes))
print("len(G.edges)", len(G.edges))

if distribution_name == "uniform":
    # 2.1.1 Uniform_distribution
    # distribution = Uniform_distribution(nodes=len(G.nodes))
    distribution = Network_Models.Uniform_distribution(nodes=len(G.edges))    
elif distribution_name == "beta":
    # 2.1.2 Beta_distribution
    # Note: The mean is the average of a group of numbers, and the variance measures the average degree to which each number is different from the mean.
    distribution = Network_Models.Beta_distribution(nodes=len(G.edges), mean=0.5, variance=0.2)
elif distribution_name == "empirical":
    # 2.1.3 Empirical_Distribution
    distribution = Network_Models.Empirical_Distribution(path=operational_dir+"distribution_empirical_file", size=len(G.edges))

print("len(distribution)", len(distribution))
print("distribution", distribution)

Network_Models.Apply_Prob(G=G, save_directory=operational_dir, distribution=distribution, Name="model_created")