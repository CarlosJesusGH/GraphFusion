#!/usr/bin/env python

__author__ = 'carlos garcia-hernandez'
# reference: WebServer/PairwiseAnalysis/NetworkComparison.py

"""		
	Purpose of the script:
	----------------------
        Description here
		
	Notes on using the script:
	--------------------------
	    Notes here

	Run as:
    -------
		python test_script.py <parameter_1> <parameter_2> <process_count>
		
		<parameter_1>: Description of parameter
		
		<parameter_2>: Description of parameter
		
		<process_count>: Any number higher than or equal to 1. Determines the number of processes to be used
			
	Implemented by:
    ---------------
		Carlos Garcia-Hernandez
		
		First implementation 	= 2021-04-14 15:40
		Revision 1 				= ...
"""

import sys
import os

# import math
# import numpy
# import time
# import networkx as nx
# import multiprocessing, Queue

# import logging
import subprocess

# LOGGER = logging.getLogger(__name__)

"""
	Helper functions are defined here
"""

# The function to check whether the provided input parameters are meaningful
def checkInput(num_processes):
    if num_processes < 1:
        # LOGGER.info('ERROR: Enter a correct number for the number of processes...')
        exit(0)

def run(param_1, param_2, num_processes):
    # LOGGER.info("marker ini 'run' method")
    os.system("echo '\n************************'")
    os.system("echo 'DataFusionScript ini\n'$(date)")
    os.system("pwd")
    # subprocess.call(['sh', '../../scripts/include/psb/psb_shell_script.sh'])
    # subprocess_res = subprocess.call("../../scripts/include/psb/psb_shell_script.sh")
    subprocess_res = subprocess.call("../../scripts/include/pynmf/pynmf_shell_script.sh")
    print("subprocess_res:", subprocess_res)
    os.system("echo $(date)'\nDataFusionScript end'")
    os.system("echo '************************'")
    # LOGGER.info("Finished 'run' method")


"""
	Main code starts here
"""
if __name__ == "__main__":
    # print("marker ini DataFusionScript main")
    # Process the program parameters
    # param_1 = sys.argv[1]
    # param_2 = sys.argv[2]
    # num_processes = int(sys.argv[3])
    param_1, param_2, num_processes = 1, 1, 1

    # Check inputs
    checkInput(num_processes)

    # Call run method
    run(param_1 = param_1, param_2 = param_2, num_processes = num_processes)
    