#!/Users/derickober/anaconda3/bin/python
import derickEssentials as de
import numpy as np 
import sys 
import matplotlib.pyplot as plt

#provide full path for the read file
deformFile = sys.argv[1]
compositionFile = sys.argv[2]
customTitle = 'ZrN Rocksalt Basis Deformation'                    #change to false for automatic title

deformation = np.loadtxt(deformFile, usecols=2)
deformationLabels = np.genfromtxt(deformFile, dtype='str', usecols=0)


atomCount = np.loadtxt(compositionFile, skiprows=1, usecols=(-2,-3))         #data in form of #N, #Zr
compositionVec = np.loadtxt(compositionFile, skiprows=1, usecols=0)                #direct N/Zr ratio
labels = np.genfromtxt(compositionFile, dtype='str', skip_header=1, usecols=-1)                    #vector of SCEL(...) names
labelLookup = dict(zip(labels,compositionVec))

plotData = np.zeros((len(deformation),2))
for i in range(len(deformation)):
    composition = labelLookup[deformationLabels[i]]
    plotData[i,:] = np.array([composition, deformation[i]]) 

plotData = de.columnSort(plotData, 0)

plt.scatter(plotData[:,0], plotData[:,1], color='xkcd:crimson')
if customTitle:
    plt.title(customTitle, fontsize=30)
else:
    plt.title(deformFile.split('/')[-1], fontsize=30)
plt.xlabel('Composition [N/Zr]', fontsize=18)
plt.ylabel('Mapping Score', fontsize=18)                  #units unknown, probably angstroms
plt.show()
