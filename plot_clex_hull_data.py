#!/Users/derickober/anaconda3/bin/python
import os 
import numpy as np 
import sys
import matplotlib.pyplot as plt
import csv

#User input 
fit_dir  = sys.argv[1]                      #path to the fit directory
hall_of_fame_index = sys.argv[2]           #individual number corresponding to hall of fame index 


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


plt.plot(dft_hull_data[:,1], dft_hull_data[:,4],marker='o', color='xkcd:crimson')
plt.plot(clex_hull_data[:,1], clex_hull_data[:,7],marker='o',linestyle='dashed' ,  color='b')
plt.scatter(dft_hull_data[:,1], dft_hull_data[:,7], color='k')
plt.scatter(below_hull_data[:,1], below_hull_data[:,7], marker='+', color='k')
plt.legend(['DFT Hull', 'Clex Hull', 'Clex Prediction of DFT Hull', 'Clex Below Clex Prediction of DFT Hull Configs'], fontsize=20)
plt.show()









