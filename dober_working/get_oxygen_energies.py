#!/Users/derickober/anaconda3/bin/python

import numpy as np
import os
import sys
import djVaspLib as dj
import derickEssentials as de

searchDir = sys.argv[1]
output = sys.argv[2]

energies = []
heights = []
e0 = 0
for subdir, dirs, files in os.walk(searchDir):
        #name = subdir.split('/')[-5] + '__' + subdir.split('/')[-4]

        for carFile in files:
            
            #get the number of atoms in the unit cell, and the number of each type
            
            #get energy of the static run
            if carFile == 'vasp.out':
                with open(subdir + '/' + carFile) as vaspOut:
                    for line in vaspOut:
                        if len(line.split()) > 4:
                            if line.split()[3] == 'E0=':
                                e0 = float(line.split()[4])
            
            if carFile == 'POSCAR':
                poscar = dj.poscar(os.path.join(subdir, 'POSCAR'))
                height = poscar.coords[-1,-1]
                
        
        heights.append(height)
        energies.append(e0)

        data = np.zeros((len(energies),2))
        data[:,0] = heights[:]
        data[:,1] = energies[:]

        data = de.columnSort(data,0)
        
        #normalize by number of atoms
        data[:,1] = data[:,1] / 2

        with open(output, 'w') as outfile:
            outfile.write('height[Angstrom] energy[eV]\n')
            for i in range(len(energies)):
                outfile.write('%s %s\n' % (data[i,0], data[i,1]))
        
