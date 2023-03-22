#!/bin/bash
script_name="pan_gdvsim_shell_script.sh"
echo -e "\t************************"   # -e stands for 'enable interpretation of backslash escapes'
echo -e "\tbeginning of script '$script_name'"
# ----------------------------------------------
# activate virtual environment
source ~/miniconda3/etc/profile.d/conda.sh
conda activate env_27
echo -e "\tCONDA: "$CONDA_PREFIX
# echo -e "\tPYTHON: "$(python --version)
echo -e "\tPWD: "$(pwd)

echo -e "all_args:" "$@"

# call python script
python ../../scripts/include/gdvsim/pan-cancer_expression_gdvs.py "$@"


# ----------------------------------------------
echo -e "\tend of script '$script_name'"
echo -e "\t************************"

# --- calling example ---
# bash ../../scripts/include/gdvsim/pan_gdvsim_shell_script.sh genelist.csv ../e11c23ed48c74b71a3488d3dbc9f5a75/iCell.ndump2 ../d14eef3d79f1476298dd8b7bef1eb5b9/iCell.ndump2 iCell_rewired.csv 
