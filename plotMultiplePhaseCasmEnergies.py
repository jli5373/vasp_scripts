#!/Users/derickober/anaconda3/bin/python
import numpy as np 
import matplotlib.pyplot as plt
import sys
import os
import derickEssentials as de

#This script can plot the formation energy of a 2-element mixture given the E0 energy from a vasp static calculation and the number of each of two species
#This script assumes that "speciesA" occupies interstitial sites with a fixed sublattice of "speciesB" (assuming speciesA can be exchanged with vacancies, 
#while speciesB cannot be exchanged with a vacancy) 

convexHullFile = 'temporary_convex_hull.txt'               #read convex hull (composition, energy) from a provided file
print(len(sys.argv))
#if readConvexHull:
#    numberStructures = len(sys.argv) - 

#get species labels for plotting
speciesA = 'N'
speciesB = 'Zr'
customTitle = 'HCP and Rocksalt Formation Energies'        #change to False if you want the script to spit out the file names as the default title
customLabels = ['Convex Hull','HCP','Rocksalt']                                              #change to False for default naming
try:
    os.remove('/Users/derickober/Research/ZrN_project/mostRecentCasmEnergies.tmp')
except:
    print('most recent energies do not exist')

noVacanciesEnergy = False
allVacanciesEnergy = False

print(sys.argv)

#provide the path to the data file
for dataFile in sys.argv[1:]:


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
            if (noVacanciesEnergy == False) or (energyPerFixedAtom[i] < noVacanciesEnergy): 
                noVacanciesEnergy = energyPerFixedAtom[i]
        elif ratio_N_Zr[i] == 0:
            if (allVacanciesEnergy == False) or (energyPerFixedAtom[i] < allVacanciesEnergy):
                allVacanciesEnergy = energyPerFixedAtom[i]



for dataFile in sys.argv[1:]:
    #import data
    data = np.loadtxt(dataFile, usecols=(0,1,2,3), skiprows=1)
    names = np.loadtxt(dataFile, usecols=(4), skiprows=1, dtype=str)


    #normalize energy to eV/Zr_atoms
    numberFixedAtoms = data[:,-1]
    energyPerFixedAtom = data[:,1] / numberFixedAtoms

    #get the ratio of atomA(interstitial species) to atomB (fixed species)
    ratio_N_Zr = data[:,0]

    #Calculate formation energy
    formationEnergy = energyPerFixedAtom - ratio_N_Zr*noVacanciesEnergy - (1-ratio_N_Zr)*allVacanciesEnergy

    #write formation energies and simulation names to a temporary file for easy lookup

    if not os.path.isfile('/Users/derickober/Research/ZrN_project/mostRecentCasmEnergies.tmp'):
        write_header = True
    else:
        write_header = False

    with open('/Users/derickober/Research/ZrN_project/mostRecentCasmEnergies.tmp', 'a') as outfile:
        
        if write_header:
            outfile.write('formation_energy ratio_N_Zr SCEL_name original_data_file')
        for i in range(len(formationEnergy)):
            outfile.write(str(formationEnergy[i]) + ' ' + str(ratio_N_Zr[i]) + ' ' + names[i] + ' ' + dataFile.split('.')[0] + '\n')
        outfile.close()

    #plot formation energy 
    plt.scatter(ratio_N_Zr,formationEnergy)
    

if convexHullFile:
        convexHull = np.loadtxt( convexHullFile, skiprows=1)
        convexHull = de.columnSort(convexHull, 0)
        #plt.scatter(convexHull[:,0], convexHull[:,1], s=120, marker='o', color='none', edgecolor='k' )
        plt.plot(convexHull[:,0], convexHull[:,1], markersize=10, marker='o', markerfacecolor='none', markeredgecolor='k' , color='k')


plt.xlabel(r'Ratio of $\frac{%s}{%s}$'%(speciesA,speciesB), fontsize=18)
plt.ylabel('Formation Energy per %s Atom [eV/atom]'%(speciesB), fontsize=18)

if customTitle == False:   
    title = ''
    for name in sys.argv[1:]:
        title = title + name.split('.')[0]    
    plt.title('%s'%(title), fontsize=30)
else:
    plt.title('%s'%(customTitle), fontsize=30)

if customLabels == False:
    plt.legend(sys.argv[1:])
else:
    plt.legend(customLabels)

fig = plt.gcf()
fig.set_size_inches(18.5, 10)
fig.savefig(os.path.join('/Users/derickober/Research/ZrN_project/', 'formationEnergies.pdf'), dpi=100)
plt.show()