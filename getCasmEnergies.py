#!/usr/bin/python

import os
import sys
import numpy as np

#use absolute paths. searchDir should be the training data directory
searchDir = sys.argv[1]
output = sys.argv[2]

ratio_N_Zr = []
energies = []
trainingNames = []
numberNs = []
numberZrs = []

for subdir, dirs, files in os.walk(searchDir):
    if subdir.split('/')[-1] == 'run.final':
        name = subdir.split('/')[-5] + '__' + subdir.split('/')[-4]

        for carFile in files:
            
            #get the number of atoms in the unit cell, and the number of each type
            if carFile == 'POSCAR':
                with open(subdir +'/' + carFile) as poscar:
                    for i, line in enumerate(poscar):
                        if i == 6:
                            atoms = np.array(line.split()).astype(int)
                            numberOfAtoms = sum(atoms)
                            
                            if len(atoms) > 1:
                                numberN = atoms[0]
                                numberZr = atoms[1]
                            elif len(atoms) == 1:
                                numberN = 0
                                numberZr = atoms[0]

            #get energy of the static run
            if carFile == 'vasp.out':
                with open(subdir + '/' + carFile) as vaspOut:
                    for line in vaspOut:
                        if len(line.split()) > 4:
                            if line.split()[3] == 'E0=':
                                e0 = float(line.split()[4])
        
        trainingNames.append(name)
        energies.append(e0)
        numberNs.append(numberN)
        numberZrs.append(numberZr)
        ratio_N_Zr.append(numberN/numberZr)

data = np.zeros((len(trainingNames),4))
data[:,0] = ratio_N_Zr
data[:,1] = energies
#data[:,2] = trainingNames
data[:,2] = numberNs
data[:,3] = numberZrs

np.savetxt(output, data,header='N/Zr_rato  energies  trainingNames  number_of_Nitrogen number_of_Zirconium')
