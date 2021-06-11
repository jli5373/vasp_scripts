#!/Users/derickober/anaconda3/bin/python
import os 
import numpy as np 
import sys
import matplotlib.pyplot as plt
import csv

#User input 
fit_dir  = sys.argv[1]                      #path to the fit directory
hall_of_fame_index = sys.argv[2]           #individual number corresponding to hall of fame index 
full_formation_energy_file = 'full_formation_energies.txt'


title = fit_dir.split('/')[-3] + ' ' + fit_dir.split('/')[-1]
dft_scel_names = []
clex_scel_names = []
dft_hull_data = []
clex_hull_data = []


for subdir, dirs, files in os.walk(fit_dir):
    for f in files:

        if '_%s_dft_gs' % hall_of_fame_index in f:
            dft_hull_path = os.path.join(fit_dir, f)
            dft_hull_data = np.genfromtxt(dft_hull_path, skip_header=1, usecols=list(range(1,10))).astype(float)
            with open(dft_hull_path, 'r') as dft_dat_file:
                dft_scel_names = [row[0] for row in csv.reader(dft_dat_file,delimiter=' ')]
                dft_scel_names = dft_scel_names[1:]

            
        if '_%s_clex_gs' % hall_of_fame_index in f:
            clex_hull_path = os.path.join(fit_dir, f)
            clex_hull_data = np.genfromtxt(clex_hull_path, skip_header=1, usecols=list(range(1,10))).astype(float)
            with open(clex_hull_path, 'r') as clex_dat_file:
                clex_scel_names = [row[0] for row in csv.reader(clex_dat_file,delimiter=' ')]
                clex_scel_names = clex_scel_names[1:]


        if '_%s_below_hull' % hall_of_fame_index in f:
            below_hull_path = os.path.join(fit_dir, f)
            below_hull_data = np.genfromtxt(below_hull_path, skip_header=1, usecols=list(range(1,10))).astype(float)
            with open(below_hull_path, 'r') as below_hull_file:
                below_hull_scel_names = [row[0] for row in csv.reader(below_hull_file, delimiter=' ')]
                below_hull_scel_names = below_hull_scel_names[1:]



plt.title(title, fontsize=30)
plt.xlabel(r'Composition $\frac{N}{Zr}$', fontsize=20)
plt.ylabel(r'Energy $\frac{eV}{prim}$', fontsize=20)
plt.plot(dft_hull_data[:,1], dft_hull_data[:,4],marker='o', color='xkcd:crimson')
plt.plot(clex_hull_data[:,1], clex_hull_data[:,7],marker='o',linestyle='dashed' ,  color='b')
plt.scatter(dft_hull_data[:,1], dft_hull_data[:,7], color='k')
plt.scatter(below_hull_data[:,1], below_hull_data[:,7], marker='+', color='k')

labels = ['DFT Hull', 'Clex Hull', 'Clex Prediction of DFT Hull', 'Clex Below Clex Prediction of DFT Hull Configs']

if full_formation_energy_file:
#format:
#run casm query -k comp formation_energy hull_dist clex clex_hull_dist -o full_formation_energies.txt
#            configname    selected           comp(a)    formation_energy    hull_dist(MASTER,atom_frac)        clex()    clex_hull_dist(MASTER,atom_frac)
    datafile = full_formation_energy_file

    data = np.genfromtxt(datafile, skip_header=1, usecols=list(range(2,7))).astype(float)
    composition = data[:,0]
    dft_formation_energy = data[:,1]
    clex_formation_energy = data[:,3]

    plt.scatter(composition, dft_formation_energy)
    labels.append('DFT energies')
    
    plt.scatter(composition, clex_formation_energy)
    labels.append('ClEx energies')
    

plt.legend(labels, loc='upper left', fontsize=20)

fig = plt.gcf()
fig.set_size_inches(18.5, 10)
fig.savefig(os.path.join(fit_dir, fit_dir.split('/')[-1]), dpi=100)
plt.show()









