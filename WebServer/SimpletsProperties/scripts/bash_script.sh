#!/bin/bash
script_name="SimpletsProperties"
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

# call python script
python ../../scripts/$script_name/python_script_$script_name.py "$@"


# ----------------------------------------------
echo -e "\tend of script '$shell_script_name'"
echo -e "\t************************"