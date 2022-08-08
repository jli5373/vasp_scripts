#!/home/jonnyli/anaconda3/envs/casm/bin/python
import os 
import numpy as np 
import sys
import matplotlib.pyplot as plt
import csv

#User input 
casm_dir  = sys.argv[1]                      #path to root directory of CASM project
x_axis_param = sys.argv[2]           #always give x axis parameter first after directory (ex. comp)
y_axis_params = ""
params_file = 'plotting_params.txt'
#todo: add parameters for decorating plot formatting and axes
for argument in sys.argv[3:-1]:
    y_axis_params += argument
    y_axis_params += " "



print("\nBegin Plotting data:\n______________________")

os.chdir(casm_dir)
os.system('casm query -k "%s %s" -o %s'% (x_axis_param, y_axis_params, params_file))
#os.system('casm query -k comp formation_energy hull_dist clex clex_hull_dist -o full_formation_energies.txt')
#full_formation_energy_file = 'full_formation_energies.txt'


#title = casm_dir.split('/')[-3] + '_' + casm_dir.split('/')[-1] 
title = casm_dir.split('/')[-1]
cv = None
rms = None
wrms = None
below_hull_exists = False

parameters_data = np.genfromtxt(os.path.join(casm_dir,params_file), skip_header=1, usecols=list(range(2,len(sys.argv)+1)))

#debug
print(parameters_data)

fig = plt.figure()
#ax = fig.add_subplot()
#ax.text(0.80, 0.80*min(dft_hull_data[:,4]), 'CV:      %.10f\nRMS:    %.10f\nWRMS: %.10f' %(cv, rms, wrms), fontsize=15)

labels = []


plt.title(title, fontsize=30)
#plt.xlabel(r'Composition $\frac{N}{Hf}$', fontsize=20)
#plt.ylabel(r'Energy $\frac{eV}{prim}$', fontsize=20)
for i in range(len(parameters_data)-1):
    plt.scatter(parameters_data[:,0], parameters_data[:,i],marker='o',linestyle='dashed' ,  color='b')
#labels.append('Clex Prediction of DFT Hull')
#plt.show()
    

#fig = plt.gcf()
#fig.set_size_inches(18.5, 10)
#fig.savefig(os.path.join(casm_dir, title + '.png'), dpi=100)
#plt.show()

print("\nFinished plotting data.\n_____________________")

