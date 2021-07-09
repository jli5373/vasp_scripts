import numpy as np
import os 
import argparse 
import json
import matplotlib.pyplot as plt


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
                 

plt.show()