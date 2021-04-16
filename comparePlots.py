#!/Users/derickober/anaconda3/bin/python
import numpy as np 
import derickEssentials as de
import matplotlib.pyplot as plt
import sys


#Takes in 2 data files and compares them by plotting both plots on subplot1, and the difference between the two plots on subplot2.
#Arrays for data file 1 and 2 need to be the same length
#Assumes that data1 and data2 have identical first columns (identical input vector)

vaspData = True

file1 = sys.argv[1]
file2 = sys.argv[2]

name1 = file1.split('.')[0]
name2 = file2.split('.')[0]


if len(sys.argv) > 3:
    numberAtoms = int(sys.argv[3])

data1 = np.loadtxt(file1)
data2 = np.loadtxt(file2)

data1 = de.columnSort(data1,0)
data2 = de.columnSort(data2,0)


if vaspData:
    #convert absolute eV units to meV/atom
    data1[:,1] = data1[:,1] * 1000/numberAtoms
    data2[:,1] = data2[:,1] * 1000/numberAtoms


plt.title(name1 + ' & ' + name2, fontsize=20)

plt.subplot(2,1,1)
plt.scatter(data1[:,0], data1[:,1], color='xkcd:crimson')
plt.scatter(data2[:,0], data2[:,1], color='xkcd:blue')
plt.ylabel('meV/atom', fontsize=18)
plt.xlabel('Encut [eV]', fontsize=18)
plt.xticks(np.arange(min(data1[:,0]), max(data1[:,0])+1, 50))
plt.legend([name1, name2 ])

plt.subplot(2,1,2)
difference = data2[:,1] - data1[:,1]
plt.scatter(data1[:,0], difference, color='xkcd:crimson')
plt.ylabel(r'$Delta$ meV/atom', fontsize=18)
plt.xlabel('Encut [eV]', fontsize=18)
plt.legend(['%s - %s' % (name2, name1)])

plt.show()




