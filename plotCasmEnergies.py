#!/Users/derickober/anaconda3/bin/python
import numpy as np 
import matplotlib.pyplot as plt
import sys

#This script can plot the formation energy of a 2-element mixture given the E0 energy from a vasp static calculation and the number of each of two species
#This script assumes that "speciesA" occupies interstitial sites with a fixed sublattice of "speciesB" (assuming speciesA can be exchanged with vacancies, 
#while speciesB cannot be exchanged with a vacancy) 

#get species labels for plotting
speciesA = 'N'
speciesB = 'Zr'

#provide the path to the data file
dataFile = sys.argv[1]

#import data
data = np.loadtxt(dataFile, usecols=(0,1,2,3), skiprows=1)
names = np.loadtxt(dataFile, usecols=(4), skiprows=1, dtype=str)


#normalize energy to eV/Zr_atoms
numberFixedAtoms = data[:,-1]
energyPerFixedAtom = data[:,1] / numberFixedAtoms


#get the ratio of atomA(interstitial species) to atomB (fixed species)
ratio_N_Zr = data[:,0]

#find energies for no-vacancies and full vacancies
for i in range(len(energyPerFixedAtom)):
    if ratio_N_Zr[i] == 1:
        noVacanciesEnergy = energyPerFixedAtom[i]
    elif ratio_N_Zr[i] == 0:
        allVacanciesEnergy = energyPerFixedAtom[i]

#Calculate formation energy
formationEnergy = energyPerFixedAtom - ratio_N_Zr*noVacanciesEnergy - (1-ratio_N_Zr)*allVacanciesEnergy



#write formation energies and simulation names to a temporary file for easy lookup
with open('/Users/derickober/Research/ZrN_project/mostRecentCasmEnergies.tmp', 'w') as outfille:
    for i in range(len(formationEnergy)):
        outfille.write(str(formationEnergy[i]) + ' ' + names[i] + '\n')
    outfille.close()

#plot formation energy 
plt.scatter(ratio_N_Zr,formationEnergy, color='xkcd:crimson')
plt.xlabel(r'Ratio of $\frac{%s}{%s}$'%(speciesA,speciesB), fontsize=18)
plt.ylabel('Formation Energy per %s Atom [eV/atom]'%(speciesB), fontsize=18)
plt.title('%s'%(dataFile.split('.')[0]), fontsize=30)
plt.show()

