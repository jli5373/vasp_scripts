#!/Users/derickober/anaconda3/bin/python
import numpy as np 
import matplotlib.pyplot as plt
import sys
import derickEssentials as de

#takes in a file of 2 columns: first column is the energy cutoff value in eV, second column is the E0 value from the vasp.out file
#optionally, it can plot the energy delta between two simulations
#the delta is given in meV
#Delta is given by y2-y1, and the value of (y2-y1) is paired with the x2 value (x2 being the second encut value)

filename = sys.argv[1]
natoms = int(sys.argv[2])

data = np.loadtxt(filename)
data = de.columnSort(data, 0)

data[:,1] = 1000 * data[:,1]/natoms    #convert eV to meV/atom

delta = []

for i in list(range(len(data))):
    delta.append(data[i,1] - data[-1,1])

delta = np.array(delta)
print(delta)
fiveLine = -0.5*np.ones(len(data[:,0]))

if 'encut' in filename.split('_'):
    convergenceType = 'encut'
elif 'kdensity' in filename.split('_'):
    convergenceType = 'k'

if convergenceType == 'k':
    plt.scatter(data[:,0], delta, color='xkcd:crimson')
    plt.plot(data[:,0],fiveLine,color='k', linestyle='dashed')
    plt.plot(data[:,0],-1*fiveLine,color='k', linestyle='dashed')
    plt.ylabel('Delta meV/atom Relative to Highest kdenstiy Simulation', fontsize=15)
    plt.xlabel(r'R$_k$ parameter', fontsize=18)
    #plt.xticks(np.arange(min(data[:,0]), max(data[:,0])+1, 5))
    plt.title(filename.split('.')[0], fontsize=20)

elif convergenceType == 'encut':
    plt.scatter(data[:,0], delta, color='xkcd:crimson')
    plt.plot(data[:,0],fiveLine,color='k', linestyle='dashed')
    plt.ylabel('meV/atom', fontsize=18)
    plt.xlabel('Encut [eV]', fontsize=18)
    plt.xticks(np.arange(min(data[:,0]), max(data[:,0])+1, 50))
    plt.title(filename.split('.')[0], fontsize=20)

plt.show()
