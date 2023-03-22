4nr_gdvdist.py: -> For each gene that is expressed in both cancer and control tissue, compute its rewiring in cancer as 1. minus the non-redundant, 2- to 4-node graphlet degree vector similarity.

requires the list of expressed genes in cancer and control tissues and the GDV signature files of the networks
e.g., for the rewiring in iCell of breast cancer:

python 4nr_gdvdist.py breast_cancer_expressed.csv breast_glandular-cells_expressed.csv breast-cancer_iCell_100.ndump2 breast_glandular-cells_iCell_100.ndump2 breast-cancer_rewired_iCell_100.csv

folder GDVdist contains all the rewirings we computed for the cancer specific study