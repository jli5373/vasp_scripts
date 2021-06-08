#!/bin/bash
#user inputs $1 = fit number $2 = directory path
cd $2
pwd
#conda activate casm
casm-learn -s genetic_alg_settings.json --select $1
casm query -k "comp,clex,formation_energy" > checkhull_genetic_alg_settings_$1_all
#conda activate my_pymatgen