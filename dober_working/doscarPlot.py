#!/Users/derickober/anaconda3/bin/python

import numpy as np 
import matplotlib.pyplot as plt
import sys
import os


#User input:
spin_polarized = False
singleElementDos = False             #True will selectively plot the DOS for only one element
atomOfInterest = 'Zr'               #Only plot the DOS for this element
normalizeAtom = 'Zr'                #Normalize by the number of these atoms (typically the metal)
customEnergyDomain = [-11,30]         #Set to False for automatic plot scaling
customDosRange = [0,3]               #set to False for automaic plot scaling

#provide path to the DOSCAR simulation directory
simulationDir = sys.argv[1]
doscar = os.path.join(simulationDir, 'DOSCAR')
poscar = os.path.join(simulationDir, 'POSCAR')
print('Spin polarized == %s' % str(spin_polarized))
print('Single Element Dos == %s' % str(singleElementDos))
print('Atom of Interest is %s' % atomOfInterest)


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


#Get doscar parameters: E(max), E(min), (the energy range in which the DOS is given), NEDOS,  E(fermi), 1.0000
#These parameters also act as a flag to mark transition from data for one atom to the next
atomCount = 0       #keep track of which atom the file read is on. 0 corresponds to the general DOS
lineCount = 0
fullDos = []
atomDos = []
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
elementBreakdownEnergies = np.zeros(len(atomDosArray[0]))
for i in range(len(numberOfAtoms)):
    collectElementDos = sum(atomDosArray[startIndex:startIndex+atomNumberLookup[identities[i]]]) / atomNumberLookup[normalizeAtom]
    elementBreakdownEnergies = elementBreakdownEnergies + collectElementDos[:,0]
    elementBreakdownDos.append(np.sum(collectElementDos[:,1:], axis=1))
    startIndex = startIndex + atomNumberLookup[identities[i]]

elementBreakdownPlot = np.array(elementBreakdownDos[0]).reshape(-1,1)
for j in range(1,len(elementBreakdownDos)):
    elementBreakdownPlot = np.append(elementBreakdownPlot, np.array(elementBreakdownDos[j]).reshape(-1,1), axis=1)


#plot stacks by element
plt.subplot(1,2,1)
a = elementBreakdownEnergies
b = elementBreakdownPlot.transpose()
plt.stackplot(a,b)
plt.vlines(doscarParams[-2],min(simpleCombinedUpDownDos), max(simpleCombinedUpDownDos), linestyles='dashed', color='k')
plt.legend(identities)
plt.xlabel('eV', fontsize=18)
plt.ylabel('DOS (eV / %s)'%(normalizeAtom), fontsize=18)
plt.title('Breakdown by Element', fontsize=20)
if customEnergyDomain:
    plt.xlim(customEnergyDomain)
if customDosRange:
    plt.ylim(customDosRange)
     

'''
plt.subplot(2,1,1)
plt.plot(fullDos[:,0], simpleCombinedUpDownDos)
plt.ylabel('DOS per atom', fontsize=18)
plt.title(doscar, fontsize=30)

plt.subplot(2,1,2)
'''


#plot stacks by orbital
plt.subplot(1,2,2)
print(atomNumberLookup[normalizeAtom])
x = combinedSpinsDos[:,0]
y = combinedSpinsDos[:,1:].transpose()
plt.stackplot(x,y)

plt.vlines(doscarParams[-2],min(simpleCombinedUpDownDos), max(simpleCombinedUpDownDos), linestyles='dashed', color='k')
plt.legend(['s(u,d)' , 'p_y(u,d)', 'p_z(u,d)', 'p_x(u,d)', 'd_[xy](u,d)', 'd_[yz](u,d)','d_[z2-r2](u,d)', 'd_[xz](u,d)', 'd_[x2-y2](u,d)]'], loc='upper left')
plt.xlabel('eV', fontsize=18)

caveat = ''
if singleElementDos:
    caveat = 'Only %s' % atomOfInterest
else:
    caveat = 'All atoms'
plt.title('Breakdown by Orbital (%s)' % caveat, fontsize=20)
if customEnergyDomain:
    plt.xlim(customEnergyDomain)
if customDosRange:
    plt.ylim(customDosRange)

fig = plt.gcf()
fig.set_size_inches(18.5, 10)
fig.savefig(os.path.join(simulationDir, 'doscarPlot.pdf'), dpi=100)
plt.show()