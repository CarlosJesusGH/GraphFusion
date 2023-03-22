#!/bin/bash
script_name="pynmf_shell_script_OLD.sh"
echo -e "\t************************"   # -e stands for 'enable interpretation of backslash escapes'
echo -e "\tbeginning of script '$script_name'"
# ----------------------------------------------
# activate virtual environment
source ~/miniconda3/etc/profile.d/conda.sh
conda activate env_37
echo -e "\tCONDA: "$CONDA_PREFIX
echo -e "\tPYTHON: "$(python --version)
echo -e "\tPWD: "$(pwd)

# call python script
python ../../scripts/include/pynmf/pynmf.py




# ----------------------------------------------
echo -e "\tend of script '$script_name'"
echo -e "\t************************"