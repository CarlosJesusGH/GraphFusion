#!/bin/bash
script_name="icell_shell_script.sh"
echo -e "\t************************"   # -e stands for 'enable interpretation of backslash escapes'
echo -e "\tbeginning of script '$script_name'"
# ----------------------------------------------
# activate virtual environment
source ~/miniconda3/etc/profile.d/conda.sh
conda activate env_27
echo -e "\tCONDA: "$CONDA_PREFIX
# echo -e "\tPYTHON: "$(python --version)
echo -e "\tPWD: "$(pwd)

echo -e "rm " "$3"
rm -f ./"$3"

# call python script
python ../../scripts/include/icell/Make_iCell.py "$@"




# ----------------------------------------------
echo -e "\tend of script '$script_name'"
echo -e "\t************************"