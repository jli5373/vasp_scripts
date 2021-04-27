#!/Users/derickober/anaconda3/bin/python

import numpy as np 
import matplotlib.pyplot as plt
import sys
import os
import seaborn as sns


#User input:
spin_polarized = True
singleElementDos = False             #True will selectively plot the DOS for only one element
combineLikeOrbitals = True              #True will sum px,py,pz, same for d
atomOfInterest = 'Zr'               #Only plot the DOS for this element
normalizeAtom = 'Zr'                #Normalize by the number of these atoms (typically the metal)
customEnergyDomain = [-9,19]         #Set to False for automatic plot scaling
customDosRange = [0,3]               #set to False for automaic plot scaling

#provide path to the DOSCAR simulation directory
simulationDir = sys.argv[1]
doscar = os.path.join(simulationDir, 'DOSCAR')
poscar = os.path.join(simulationDir, 'POSCAR')
print('Spin polarized == %s' % str(spin_polarized))
print('Single Element Dos == %s' % str(singleElementDos))
print('Atom of Interest is %s' % atomOfInterest)
print('Normalize atom is %s' % normalizeAtom)


#Read in the element types and number of each element from the poscar, store in a dictionary
with open(poscar) as infile:
    lineCount = 0
    for line in infile:
        
        if lineCount == 5:
            identities = line.split()

        if lineCount == 6:
            numberOfAtoms = np.array(line.split()).astype(int)
            lineCount += 1 
        else:
            lineCount += 1
    infile.close()
atomNumberLookup = dict(zip(identities, numberOfAtoms))
print('Number of normalize atoms is %s' % str(atomNumberLookup[normalizeAtom]))


#Get doscar parameters: E(max), E(min), (the energy range in which the DOS is given), NEDOS,  E(fermi), 1.0000
#These parameters also act as a flag to mark transition from data for one atom to the next
atomCount = 0       #keep track of which atom the file read is on. 0 corresponds to the general DOS
lineCount = 0
fullDos = []
atomDos = []        #holds full dos data matrix for each atom: array of matrices, one matrix per atom
doscarParams = None
with open(doscar) as f:
    for line in f:

        #line = np.array(line.split()).astype(float)
        if lineCount == 5:
            doscarParams = np.array(line.split()).astype(float)

        lineCount = lineCount + 1

        #grab DOS data for full DOS and atom projected DOS
        if lineCount > 6:
            if not np.array_equal(np.array(line.split()).astype(float), doscarParams):
                l = np.array(line.split()).astype(float)
                if atomCount == 0:              #data for full (general) DOS
                    fullDos.append(l)        #data in the form:  [energy     DOS(up) DOS(dwn)  integrated DOS(up) integrated DOS(dwn)]

                
                elif atomCount > 0:             #data for atom projected DOS
                    atomDos[-1].append(l)    #in the form: [energy  s(u,d)  p_y(u,d) p_z(u,d) p_x(u,d) d_{xy}(u,d) d_{yz}(u,d) d_{z2-r2}(u,d) d_{xz}(u,d) d_{x2-y2}(u,d)


            elif np.array_equal(np.array(line.split()).astype(float), doscarParams):
                atomCount = atomCount + 1
                atomDos.append([])              #create a new array for each atom DOS data
    f.close()


#Assemble full dos data for spin up and spin down
if spin_polarized:
    fullDos = np.array(fullDos)
    simpleCombinedUpDownDos = (fullDos[:,1] + fullDos[:,2]) / atomNumberLookup[normalizeAtom]
else:
    fullDos = np.array(fullDos)
    simpleCombinedUpDownDos = fullDos[:,1] / atomNumberLookup[normalizeAtom]    


#Sum like orbitals across all atoms (or element specific breakdown)
if singleElementDos == False:
    projectedDos = np.array(atomDos[0])
    for i in range(1,len(atomDos)):
        projectedDos = projectedDos + np.array(atomDos[i])

elif singleElementDos == True:
    atomSkip = 0
    for element in identities:
        if element != atomOfInterest:
            atomSkip = atomSkip + atomNumberLookup[element]
        elif element == atomOfInterest:
            atomReadEnd = atomSkip + atomNumberLookup[element]
            atomOfInterestRange = list(range(atomSkip, atomReadEnd ))
    
    projectedDos = np.array(atomDos[atomSkip])
    for i in atomOfInterestRange:
        projectedDos = projectedDos + np.array(atomDos[i])


if spin_polarized:
    #Sum spin up and spin down states for each orbital
    combinedSpinsDos = np.zeros((len(projectedDos), 10))
    combinedSpinsDos[:,0] = projectedDos[:,0]
    for i in range(1,10):

        j = (2*i) - 1
        combinedSpinsDos[:,i] = (projectedDos[:,j] +  projectedDos[:,j+1]) 
    combinedSpinsDos = combinedSpinsDos
else:
    combinedSpinsDos = projectedDos / atomNumberLookup[normalizeAtom]





#do a breakdown by element ID
startIndex = 0
atomDosArray = np.array(atomDos)
elementBreakdownDos = []
elementBreakdownEnergies = atomDosArray[0][:,0]
numberOfOrbitals = []
#Iterating through "i" different elements in the poscar
for i in range(len(numberOfAtoms)):
    collectElementDos = sum(atomDosArray[startIndex:startIndex+atomNumberLookup[identities[i]]]) / atomNumberLookup[normalizeAtom]              #sum matrices of like atoms       
    

    if combineLikeOrbitals:
        combineS = np.reshape(np.array(collectElementDos[:,1]), (-1,1))
        combineP = np.reshape(np.sum(np.array(collectElementDos[:,2:5]), axis=1), (-1,1))
        combineD = np.reshape(np.sum(np.array(collectElementDos[:,5:]), axis=1), (-1,1))

        collectElementDos = np.concatenate((np.reshape(elementBreakdownEnergies,(-1,1) ), combineS, combineP, combineD ), axis=1)
        print('%s: %s number of energy points x (energy values + number of orbitals) ' %  (identities[i], str(np.shape(collectElementDos))))

    #VERY TEMPORARY FIX:
    #future fix: if a type of orbital is completely empty, remove it
    if identities[i] == 'N':
        if combineLikeOrbitals:
            collectElementDos = collectElementDos[:,0:3]
        else:
            collectElementDos = collectElementDos[:,0:5]
    
    elementBreakdownDos.append(collectElementDos[:,1:])                                                                                         #append summed matrix for element "i", excluding the summed energies
    numberOfOrbitals.append(len(collectElementDos[0,1:]))                       #count the number of different occupied orbitals for species i (EX: if Nitrogen, there is s,px,py,pz, no d: there are 4 occupied orbitals)
    #print(np.sum(collectElementDos, axis=0))
    startIndex = startIndex + atomNumberLookup[identities[i]]

#stack up orbital DOS for different atoms on top of each other (append matrix of orbital DOS to the right of an existing DOS matrix- axis 1 is append horizontal)
elementBreakdownPlot = np.array(elementBreakdownDos[0])
for j in range(1,len(elementBreakdownDos)):
    elementBreakdownPlot = np.append(elementBreakdownPlot, np.array(elementBreakdownDos[j]), axis=1)


#VERY TEMPORARY to plot full dos spin polarized
plt.plot(elementBreakdownEnergies , fullDos[:,1]/atomNumberLookup[normalizeAtom], color='k')
plt.plot(elementBreakdownEnergies, fullDos[:,2]/atomNumberLookup[normalizeAtom], color='xkcd:crimson')
plt.legend(['Spin Up' , 'Spin Down'])
plt.vlines(doscarParams[-2],min(simpleCombinedUpDownDos), max(simpleCombinedUpDownDos), linestyles='dashed', color='k')
plt.xlabel('eV', fontsize=18)
plt.ylabel('DOS (Per %s)'%(normalizeAtom), fontsize=18)
plt.title(simulationDir.split('/')[-4] + '/' + simulationDir.split('/')[-3], fontsize=30)
fig = plt.gcf()
fig.set_size_inches(18.5, 10)
fig.savefig(os.path.join(simulationDir, '%s_magneticFullDoscar.pdf' % (simulationDir.split('/')[-4] + '_' + simulationDir.split('/')[-3] )), dpi=100)
plt.show()



'''
#plot stacks by element and orbital
#generate labels for the stack plot
labels = []
if combineLikeOrbitals:
    orbitals = ['s', 'p', 'd']
else:
    orbitals = ['s(u,d)' , 'p_y(u,d)', 'p_z(u,d)', 'p_x(u,d)', 'd_[xy](u,d)', 'd_[yz](u,d)','d_[z2-r2](u,d)', 'd_[xz](u,d)', 'd_[x2-y2](u,d)]']

for i in range(len(numberOfAtoms)):
    for j in range(numberOfOrbitals[i]):
        labels.append('%s %s ' % (identities[i], orbitals[j]) )
a = elementBreakdownEnergies
b = elementBreakdownPlot.transpose()

if combineLikeOrbitals:
    plt.stackplot(a,b, colors=sns.color_palette('colorblind'))
else:
    plt.stackplot(a,b, colors=sns.color_palette('hls', sum(numberOfOrbitals)+1))
#plt.plot(a,simpleCombinedUpDownDos, color='b')
plt.vlines(doscarParams[-2],min(simpleCombinedUpDownDos), max(simpleCombinedUpDownDos), linestyles='dashed', color='k')
plt.legend(labels)
plt.xlabel('eV', fontsize=18)
plt.ylabel('DOS (Per %s)'%(normalizeAtom), fontsize=18)
plt.title('Breakdown by Element and Orbital', fontsize=20)
if customEnergyDomain:
    plt.xlim(customEnergyDomain)
if customDosRange:
    plt.ylim(customDosRange)

#for debugging    
#for i in elementBreakdownEnergies:
#    print(i)
print('fermi energy is: %s' % doscarParams[-2])

fig = plt.gcf()
fig.set_size_inches(18.5, 10)
fig.savefig(os.path.join(simulationDir, '%s_doscarPlot.pdf' % (simulationDir.split('/')[-4] + '_' + simulationDir.split('/')[-3] )), dpi=100)
plt.show()
'''
