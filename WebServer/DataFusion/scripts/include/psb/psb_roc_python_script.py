print("\t\t************************")
print("\t\tbeginning python script")
# ../../scripts/include/psb/psb_shell_script.sh
# from ./scripts/Data/creatingMatrices.py import *
# from scripts.Data.creatingMatrices import *

import os
import sys
import pickle
import numpy as np
import h5py

# print pwd
print("pwd", os.system("pwd"))

# append additional paths to sys
sys.path.append('../../scripts/include/psb/scripts/ResultsAnalysis/')
sys.path.append('../../scripts/include/psb/scripts/')

# extra imports
from PRandROCcurves import *
from plots import *

# get parameters
args = sys.argv[1:]; print("args", args)
op_dir, fact_id, ouputfile = args[0], int(args[1]), args[2]

# remove old output files
cmd = "rm -f " + ouputfile
print("cmd:", cmd, " res:", os.system(cmd))

# load info from data-fusion
facts = pickle.load(open("./facts.pkl", "rb"))
print("facts", facts)
print("type(facts)", type(facts))
print("type(facts[fact_id])", type(facts[fact_id]))
print("facts[fact_id].keys()", facts[fact_id].keys())

# Load matrices
# G1_name, H12_name, G2_name = facts[fact_id]["M1_name"], facts[fact_id]["M2_name"], facts[fact_id]["M3_name"]
# If matrix name doesn't exist, use None
G1_name = facts[fact_id]["M1_name"] if "M1_name" in facts[fact_id] else None
H12_name = facts[fact_id]["M2_name"] if "M2_name" in facts[fact_id] else None
G2_name = facts[fact_id]["M3_name"] if "M3_name" in facts[fact_id] else None
R_reconstruct = reconstructR(op_dir, facts[fact_id]["factType"], G1_name, H12_name, G2_name)
# r = np.load('../Data/Matrices/Matrix_R23.npy')
# with h5py.File("./graphs/" + facts[0]["M0"], "r") as f:
#     r = np.array(f.get('dataset'))
r = np.loadtxt(open("./graphs/" + facts[fact_id]["M0"], "rb"), delimiter="\t", skiprows=0)
print("r.shape, R_reconstruct.shape", r.shape, R_reconstruct.shape)
# print("r", r); print("R_reconstruct", R_reconstruct)

# compute roc curve
fpr, tpr, roc_auc = computeROC(r, R_reconstruct)
plotROCCurve(fpr, tpr, roc_auc, ouputfile)

# end
print("\t\tend python script")
print("\t\t************************")