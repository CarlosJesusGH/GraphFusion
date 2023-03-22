#!/bin/bash
script_name="ProbabilisticNetworksModelAnalysis"
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

cp ../../scripts/undirs/* .

# call python script to create the model
python ../../scripts/python_script.py "$@"

# call python script to create the perform the probabilistic analysis
python ../../../ProbabilisticNetworksNetAnalysis/scripts/python_script.py Prob_model_created "$1"

rm undir*

# ----------------------------------------------
echo -e "\tend of script '$shell_script_name'"
echo -e "\t************************"