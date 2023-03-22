#!/bin/bash
script_name="pairwise_gdvsim_shell_script.sh"
echo -e "\t************************"   # -e stands for 'enable interpretation of backslash escapes'
echo -e "\tbeginning of script '$script_name'"
# ----------------------------------------------
# activate virtual environment
source ~/miniconda3/etc/profile.d/conda.sh
conda activate env_27
echo -e "\tCONDA: "$CONDA_PREFIX
# echo -e "\tPYTHON: "$(python --version)
echo -e "\tPWD: "$(pwd)

echo -e "$1" 
echo -e "$2" 
echo -e "$3"

# call python script
python ../../scripts/include/gdvsim/4nr_gdvdist.py "$@"


# ----------------------------------------------
echo -e "\tend of script '$script_name'"
echo -e "\t************************"

# --- calling example ---
# bash ../../scripts/include/gdvsim/gdvsim_shell_script.sh ./breast-cancer_iCell_genelist.csv ../e11c23ed48c74b71a3488d3dbc9f5a75/breast-cancer_iCell_genelist.csv ./iCell.ndump2 ../e11c23ed48c74b71a3488d3dbc9f5a75/iCell.ndump2 iCell_rewired.csv
