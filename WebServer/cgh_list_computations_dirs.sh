#!/bin/bash
DIR=( $(find -name "computations" -type d) ) 

for dir in "${DIR[@]}"; do
   printf "\n\n"$dir"\n------------------------------------\n"
   ls $dir
   printf "\n"
done