#!/bin/bash
script_name="simplets_pairwise_comp_shell_script.sh"
echo -e "\t************************"   # -e stands for 'enable interpretation of backslash escapes'
echo -e "\tbeginning of script '$script_name'"
# ----------------------------------------------
# activate virtual environment
source ~/miniconda3/etc/profile.d/conda.sh
# conda activate env_37
conda activate env_27
echo -e "\tCONDA: "$CONDA_PREFIX
echo -e "\tPYTHON: "$(python --version)
echo -e "\tPWD: "$(pwd)
echo -e "\tARGS: ""$@"

# call python script
python ../../scripts/Simplets_Distances.py . "$@"

# ----------------------------------------------
echo -e "\tend of script '$script_name'"
echo -e "\t************************"