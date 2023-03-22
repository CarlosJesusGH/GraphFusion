#!/usr/bin/env bash

# Get list of KEGG pathways
wget http://rest.kegg.jp/list/pathway/hsa

# Select metabolic pathways
grep -iP "metabolism|metabolic|glycolysis|TCA|oxidative phosphorylation|fatty acid|pentose|degradation|biosynthesis" hsa \
  | grep -v "RNA" > hsa_metabolism_pathways.txt

cut -f 1 hsa_metabolism_pathways.txt > hsa_metabolism_pathways_cut.txt  #cut the file taking only the first columns

# Download pathway information from KEGG
while read p; 
do
  echo $p;
  output=$(echo $p | sed "s/:/_/g"); #edit the pathway name replacing : for _
  wget -O $output http://rest.kegg.jp/get/${p};
done < hsa_metabolism_pathways_cut.txt;

# For each pathway, extract gene IDs (ENTREZ and HGNC)and create edgelist
touch KEGG_metabolic_network_entrez.edgelist
touch KEGG_metabolic_network_hgnc.edgelist
for pathfile in path_*; do
  # ENTREZ
  genes=$(grep "EC:" $pathfile | awk -F ' +' '{print $2}');
  for i in $genes; do
    for j in $genes; do
      if [[ "$i" != "$j" ]]; then
        echo -e "$i,$j" >> KEGG_metabolic_network_entrez.edgelist;
      fi
    done
  done
  # HGNC
  genesHGNC=$(grep "EC:" $pathfile | awk -F ' +' '{print $3}' | sed "s/;//g");
  for i in $genesHGNC; do
    for j in $genesHGNC; do
      if [[ "$i" != "$j" ]]; then
        echo -e "$i,$j" >> KEGG_metabolic_network_hgnc.edgelist;
      fi
    done
  done
done

# Remove duplicated entries from edgelist file
sort KEGG_metabolic_network_entrez.edgelist | uniq > tmp.txt
mv tmp.txt KEGG_metabolic_network_entrez.csv
sort KEGG_metabolic_network_hgnc.edgelist | uniq > tmp.txt
mv tmp.txt KEGG_metabolic_network_hgnc.csv
