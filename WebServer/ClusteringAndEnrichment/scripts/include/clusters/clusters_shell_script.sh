#!/bin/bash
script_name="clusters_shell_script.sh"
echo -e "\t************************"   # -e stands for 'enable interpretation of backslash escapes'
echo -e "\tbeginning of script '$script_name'"
# ----------------------------------------------
# activate virtual environment
source ~/miniconda3/etc/profile.d/conda.sh
conda activate env_37
echo -e "\tCONDA: "$CONDA_PREFIX
# echo -e "\tPYTHON: "$(python --version)
echo -e "\tPWD: "$(pwd)

rm -f ./clusters.npy && rm -f ./clusters_from_factor.svg

# call python script
python ../../scripts/include/clusters/clusterization.py "$@"


# ----------------------------------------------
echo -e "\tend of script '$script_name'"
echo -e "\t************************"