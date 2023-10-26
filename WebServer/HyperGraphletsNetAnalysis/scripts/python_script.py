
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
args = sys.argv[1:]
print("args", args)

# ./run_hypercounter -g "path_to_file/hyperedge.list" -o "path_to_output/name_of_output" -t "Number of threads, default 1" -b "Number of groups of genes to launch across the threads, default 50"
cmd = "../../scripts/hypergraphlet_counter/source/run_hypercounter -g " + args[0] + " -o output.hdv -t 1 -b 50"

os.system(cmd)