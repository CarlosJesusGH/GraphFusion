#!/bin/bash
script_name="HyperGraphletsNetAnalysis"
shell_script_name="shell_script_"$script_name".sh"
echo -e "\t************************"   # -e stands for 'enable interpretation of backslash escapes'
echo -e "\tbeginning of script '$shell_script_name'"
# ----------------------------------------------
# activate virtual environment
source ~/miniconda3/etc/profile.d/conda.sh
conda activate env_37
echo -e "\tCONDA: "$CONDA_PREFIX
# echo -e "\tPYTHON: "$(python --version)
echo -e "\tPWD: "$(pwd)

cp ../../scripts/hypergraphlet_counter/source/hypergraphlets_1_4_map .

# call python script
# python ../../scripts/python_script.py "$@"

# ./run_hypercounter -g "path_to_file/hyperedge.list" -o "path_to_output/name_of_output" -t "Number of threads, default 1" -b "Number of groups of genes to launch across the threads, default 50"
# ../../scripts/hypergraphlet_counter/source/run_hypercounter -g $1 -o output.hdv -t 1 -b 50

rm hypergraphlets_1_4_map

# ----------------------------------------------
echo -e "\tend of script '$shell_script_name'"
echo -e "\t************************"