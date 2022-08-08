#!/Users/jonnyli/anaconda3/bin/python
import os 
import numpy as np 
import sys
import matplotlib.pyplot as plt
import csv

#User input 
fit_dir  = sys.argv[1]                      #path to the fit directory
fit_name = 'lasso_fit.0'                          #optional parameter
hall_of_fame_index = sys.argv[2]           #individual number corresponding to hall of fame index
casm_environment = 'casm'                   #name of casm environment in conda
pymatgen_environment = 'my_pymatgen'        #name of environment with matplotlib

#generate energies
#os.system('conda activate %s' % ( casm_environment ) )
os.system('/home/jonnyli/Desktop/vasp_scripts/jonny_working/get_all_clex_energies.sh %s ./' % ( hall_of_fame_index ) )
#os.system('conda activate %s' % ( pymatgen_environment ) )

#title = fit_dir.split('/')[-1] + ' ' + hall_of_fame_index
title = fit_name + ' ' + hall_of_fame_index
dft_scel_names = []
clex_scel_names = []
dft_hull_data = []
clex_hull_data = []
all_energies_data = []
below_hull_data = []

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

        if '_%s_all' % hall_of_fame_index in f:
            all_energies_path = os.path.join(fit_dir, f)
            all_energies_data = np.genfromtxt(all_energies_path, skip_header=13, skip_footer=2, usecols=list(range(1,5))).astype(float)
#            with open(all_energies_path, 'r') as all_energies_file:
#                all_energies_scel_names = [row[0] for row in csv.reader(all_energies_file, delimiter=' ', skipinitialspace = True)]
#                all_energies_scel_names = all_energies_scel_names[1:]
    
print(below_hull_data)
print(all_energies_data)

plt.title(title, fontsize=30)
plt.plot(dft_hull_data[:,1], dft_hull_data[:,4],marker='o', color='xkcd:crimson') #DFT hull
plt.plot(clex_hull_data[:,1], clex_hull_data[:,7],marker='o',linestyle='dashed' ,  color='b') #CLEX hull
plt.scatter(all_energies_data[:,1], all_energies_data[:,3], marker='*', color='salmon') #all DFT energies
plt.scatter(all_energies_data[:,1], all_energies_data[:,2], marker='*', color='skyblue') #all clex energies
plt.scatter(dft_hull_data[:,1], dft_hull_data[:,7], color='k') #DFT clex prediction
plt.scatter(below_hull_data[:,1], below_hull_data[:,7], marker='+', color='k') #clex energies below DFT ground states (in clex)
plt.legend(['DFT Hull', 'Clex Hull', 'DFT energies', 'Clex energies', 'Clex Prediction of DFT Hull', 'Clex Below Clex Prediction of DFT Hull Configs'], fontsize=8)
plt.show()