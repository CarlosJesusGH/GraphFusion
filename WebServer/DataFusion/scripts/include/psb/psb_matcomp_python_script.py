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
op_dir, fact_id, outputfile_dist, outputfile_pred, entitylist_rows_filename, entitylist_cols_filename = args
fact_id = int(fact_id)

# remove old output files
cmd = "rm -f " + outputfile_dist
print("cmd:", cmd, " res:", os.system(cmd))

# load info from data-fusion
facts = pickle.load(open("./facts.pkl", "rb"))
print("facts", facts)
print("type(facts)", type(facts))
print("type(facts[fact_id])", type(facts[fact_id]))
print("facts[fact_id].keys()", facts[fact_id].keys())

# Load matrices
R_reconstruct = reconstructR(op_dir, facts[fact_id]["factType"], facts[fact_id]["M1_name"], facts[fact_id]["M2_name"], facts[fact_id]["M3_name"])
# r = np.load('../Data/Matrices/Matrix_R23.npy')
# with h5py.File("./graphs/" + facts[0]["M0"], "r") as f:
#     r = np.array(f.get('dataset'))
r = np.loadtxt(open("./graphs/" + facts[fact_id]["M0"], "rb"), delimiter="\t", skiprows=0)
print("r.shape, R_reconstruct.shape", r.shape, R_reconstruct.shape)
# print("r", r); print("R_reconstruct", R_reconstruct)

# find threshold using PRcurve
maxF1, thresholdF1, precisionMaxF1, recallMaxF1, precision, recall, pr_auc = computePRCurve(r, R_reconstruct)
# plotPRCurve(precision, recall, maxF1, thresholdF1, precisionMaxF1, recallMaxF1, pr_auc, ouputfile_dist)

# compute distribution of association scores
valuesNotInOriginal, alreadyPaired_inReconstructed = computeNewPairs(R_reconstruct, r)  
plotAssociationScores(valuesNotInOriginal, alreadyPaired_inReconstructed, thresholdF1, outputfile_dist)

# compute predictions
entitylist_rows = pd.read_csv(op_dir + "/" + entitylist_rows_filename).iloc[:,0].values
entitylist_cols = pd.read_csv(op_dir + "/" + entitylist_cols_filename).iloc[:,0].values

# TODO: remove later. (removed on 2023-01-25, maybe i'll need to include it again later)
# entitylist_rows, entitylist_cols = entitylist_rows[0:204], entitylist_cols[0:204]

print("entitylist_rows.shape[0], entitylist_cols.shape[0]", entitylist_rows.shape[0], entitylist_cols.shape[0])
# print("entitylist_rows", entitylist_rows)

restricDTIs(thresholdF1, R_reconstruct, r, entitylist_cols, entitylist_rows, outputfile_pred)

# end
print("\t\tend python script")
print("\t\t************************")