#!/bin/bash
script_name="MultipleAlignment"
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
# python ../../scripts/$script_name/python_script_$script_name.py "$@"

echo -e "\t************************"
echo -e "\trunning Fuse-NMTF"
cp ../../scripts/fuse_nmtf/*.m .
octave octave_script.m --no-window-system
rm block_matrices.m factorization.m run_nmtf.m top_export.m

echo -e "\t************************"
echo -e "\trunning Fuse-Alignment"
cp ../../scripts/fuse_alignment/FUSE.out .
./FUSE.out -n network_list.txt -s sequence_scores.lst -t nmtf_scores.lst -o fuse_alignment_output.txt
rm FUSE.out

# ----------------------------------------------
echo -e "\tend of script '$shell_script_name'"
echo -e "\t************************"