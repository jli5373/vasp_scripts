#!/Users/derickober/anaconda3/bin/python
import numpy as np
import sys
import os

#Script to read poscar, redefine poscar in a new (user-provided basis)
#new basis should be in a text file as a 3x3 matrix, space delimited 
#provide absolute path to poscar and new basis

poscarFile = sys.argv[1]
newBasis = sys.argv[2]
currentDirectory = ''
for i in range(len(poscarFile.split('/'))-1):
    currentDirectory =  currentDirectory + '/' + poscarFile.split('/')[i]
currentDirectory = currentDirectory[1:]
print(currentDirectory)


newBasis = np.loadtxt(newBasis)
posname = ''
speciesVec = []
speciesCountVec = np.array([])
scaling = 1
oldBasis = np.zeros((3,3))
directCoords = True                 #in vasp, direct == fractional
coords = []
readCoords = True

#read poscar
lineCount = 0
with open(poscarFile, 'r') as pfile:
    for line in pfile:
        
        
        if len(line.split()) == 0:
            #print('ERROR: unexpected empty line at line %s\nScript might not work properly.' % (lineCount +1) )
            #print("(if this is a CONTCAR and the problem line is after the coordinates, you're fine)\n\n")
            readCoords = False
        


        if lineCount == 0:
            posname = line
        elif lineCount == 1:
            scaling = float(line)
        elif lineCount > 1 and lineCount < 5:
            oldBasis[lineCount-2, :] = np.array(line.split()).astype(float)
        elif lineCount == 5:
            speciesVec = line.split()
        elif lineCount == 6:
            speciesCountVec = np.array(line.split()).astype(int)
        elif lineCount == 7:
            if line.split()[0][0] == 'd' or line.split()[0][0] == 'D':
                directCoords = True
            else:
                directCoords = False
        elif lineCount > 7 and readCoords:
            coords.append(line.split())
        lineCount += 1

    pfile.close()

oldBasis = (scaling * oldBasis).transpose()
coords = np.array(coords).astype(float).transpose()


'''
print('old basis:')
print(oldBasis)
print('\n')
print('coords:')
print(coords)
'''

if directCoords:
    absoluteCoords = np.matmul(oldBasis,coords)
else:
    absoluteCoords = coords

newFracCoords = np.matmul(np.linalg.inv(newBasis), absoluteCoords) 



#write to new poscar
newFracCoords = newFracCoords.transpose()
newBasis = newBasis.transpose()
with open( os.path.join(currentDirectory, 'newPoscar.vasp'), 'w') as newPoscar:
    newPoscar.write('new_poscar_'+ posname)
    newPoscar.write('1.000'+'\n')
    
    for row in newBasis:
        for element in row:
            newPoscar.write(str(element) + ' ')
        newPoscar.write('\n')
    
    for species in speciesVec:
        newPoscar.write(species + ' ')
    newPoscar.write('\n')

    for count in speciesCountVec:
        newPoscar.write(str(count) + ' ')
    newPoscar.write('\n')

    newPoscar.write('Direct\n')

    for row in newFracCoords:

        if True: #all(row < 1):
            for element in row:
                newPoscar.write(str(element) + ' ')
            newPoscar.write('\n')
    newPoscar.close()







                
        
