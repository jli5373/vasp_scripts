#!/bin/bash
#user inputs $1 = fit number $2 = directory path
cd $2
pwd
#method='lassoCV'
method='lasso'
#method='genetic_alg'
#conda activate casm
casm-learn -s ${method}_settings.json --select $1
casm query -k "comp,clex,formation_energy" > checkhull_${method}_settings_$1_all
#conda activate my_pymatgen