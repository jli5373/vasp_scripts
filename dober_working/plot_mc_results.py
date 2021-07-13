import numpy as np
import os 
import argparse 
import json
import matplotlib.pyplot as plt



#Provide a directory within a casm project to store monte carlo runs via command line. 

#Parse input parameters
parser = argparse.ArgumentParser()
parser.add_argument("-md", '--monte_dir', help="full path to your monte carlo directory (fixed mu, temperature sweep)")
args = parser.parse_args()
mc_runs_directory = args.monte_dir



labels = []

for subdir, dirs, files in os.walk(mc_runs_directory):
    for filename in files:
        if filename == 'results.json':
            datafile = os.path.join(subdir,'results.json')
            with open(datafile) as f:
                data = json.load(f)
                f.close()
                current_mc = subdir.split('/')[-1]
                labels.append(current_mc)
                composition = data['<comp(a)>']
                temperature = data['T']
                plt.scatter(composition, temperature)

plt.legend(labels)
title = 'Chemical Potential and Temperature Sweep Rain Plot'
plt.title('Chemical Potential and Temperature Sweep Rain Plot', fontsize=30)
fig = plt.gcf()
fig.set_size_inches(18.5, 10)
fig.savefig(os.path.join(mc_runs_directory, title + '.png'), dpi=100)
plt.show()