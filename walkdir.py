#!/usr/bin/python

import os
import sys

#provide a directory to search: the program iterates through all sub directories and pulls data from a specified file name
#provide an output file name

searchDir = sys.argv[1]
output = sys.argv[2]

encuts = []
finalEnergies = []


for subdir, dirs, files in os.walk(searchDir):
    for file in files:
        if file=='vasp.out':
            with open(os.path.join(subdir, file)) as vaspOut:
                print(subdir)
                for line in vaspOut:
                    if len(line.split()) > 4:
                        if line.split()[3] == 'E0=':

                            #get the encut value from the directory name
                            l = subdir.split('/')[-1].split('_')
                            encutValueIndex = l.index('encut') + 1
                            print(subdir)
                            encut = int(subdir.split('/')[-1].split('_')[encutValueIndex])
                            encuts.append(encut)


                            finalEnergies.append(float(line.split()[4]))
            vaspOut.close()
        print os.path.join(subdir, file)

with open(searchDir + output, "w") as outFile:
    for i in list(range(0,len(finalEnergies))):
        outFile.write(str(encuts[i]) + ' ' + str(finalEnergies[i]) + '\n')