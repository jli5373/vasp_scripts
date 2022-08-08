#!/bin/bash
for run in mu_*; do
    cd ./$run
    generate_POSCARs_from_MC 28 28
    cd ..
done
