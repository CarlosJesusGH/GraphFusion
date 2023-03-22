
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
args = sys.argv[1:]
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
os.chdir("/home/Downloads/GC3-WWW/www/GC3Env/GC3/WebServer/ProbabilisticNetworksNetAnalysis/scripts")
import Script_Parallel_Nodes_Count_Dist

# Set the paths:
Name_Network   = args[0]
network_path   = args[1]
save_directory = args[1]
Run_path   = "/home/Downloads/GC3-WWW/www/GC3Env/GC3/WebServer/ProbabilisticNetworksNetAnalysis/scripts/Release/"
undir_path = args[1]

# -------------------------------------------

#  Preprocess the edge list:

'''
Con esta functión lo que haremos será adaptar el edge list original. Concretamente guardaremos el nombre de los genes y asignaremos a cada gene un número en formato
int. De ese modo gen1 - gen2 serán 1-2 concretamente. Esta asignación queda guardada para ser capaces de volver siempre al original. Del mismo modo, la función genera
la red en formato binario y en formato de probabilidad.
'''

Script_Parallel_Nodes_Count_Dist.Creat_Network(Name_Network, save_directory, network_path)


# -------------------------------------------

# Count the Orbits:

Name_Network_Prob = f'Work_Network_Prob_{Name_Network}'
Name_Network_Bin  = f'Work_Network_Bin_{Name_Network}'

total_nodes = (len(open(f'{save_directory}Gene_Names_{Name_Network}').readlines(  ))) - 1 # Restamos 1 porque la primera linea corresponde al nombre de las columnas.


# -------------------------------------------

# pon aquí el directorio donde quieres que se ejecute todo 
# %cd $Run_path
os.chdir(Run_path)

# -------------------------------------------

# Conteo de las que son binarias:
Script_Parallel_Nodes_Count_Dist.Compute_Orbits_Spliting_Nodes(Name_Network_Bin, total_nodes, network_path, save_directory, 
                                                               Run_path, undir_path, threads = 1)  

# -------------------------------------------

# Conteo de las que son probabilisticas:
# Script_Parallel_Nodes_Count_Dist.Compute_Orbits_Spliting_Nodes(Name_Network_Bin, total_nodes, network_path, save_directory, 
#                                                                Run_path, undir_path, threads = 1) 
Script_Parallel_Nodes_Count_Dist.Compute_Orbits_Spliting_Nodes(Name_Network_Prob, total_nodes, network_path, save_directory, 
                                                               Run_path, undir_path, threads = 1) 

# -------------------------------------------

# Finalmente creamos la matriz con todos los conteos:

Script_Parallel_Nodes_Count_Dist.Prepare_Matrix_GDV(Name_Network_Bin, save_directory)
Script_Parallel_Nodes_Count_Dist.Prepare_Matrix_GDV(Name_Network_Prob, save_directory)


# -------------------------------------------

print("line:", get_linenumber(), "subprocess ls:", subprocess.check_output("ls", shell=True))

# -------------------------------------------
