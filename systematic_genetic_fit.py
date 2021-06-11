import numpy as np 
import os 
import sys 

#Runs a sweep across genetic algorithm fitting parameters A,B,kT. 
#more parameters can be added: just modify the template string to acccept the new parameters.
#make sure that the casm conda environment is active before you run this script

ce_fits_dir = sys.argv[1]           #the directory of cluster expansion fits. Currently, we use casm_root/ce_fits
os.chdir(ce_fits_dir)

run_fits = False                    #Change to True if you would like to do new fits. Leave False if you only want to generate new plots

#fit parameters
A = np.linspace(.1,2,3)
B = np.linspace(0,2,3)
kt = np.linspace(.01,.1,3)



for i in range(len(A)):
    for j in range(len(B)):
        for k in range(len(kt)):
            fitname = 'A-%s_B-%s_kt-%s' %(str(A[i]), str(B[j]), str(kt[k]))
            os.makedirs(fitname, exist_ok=True)
            os.system('cp training_set.txt %s' % fitname)

            template = '''
                            {
                            "problem_specs": {
                                "data": {
                                "filename": "training_set.txt",
                                "type": "selection",
                                "X": "corr",
                                "y": "formation_energy",
                                "kwargs": null
                                },
                                "weight": {
                                "method": "wHullDist",
                                "kwargs": {
                                    "A": %s,
                                    "B": %s,
                                    "kT": %s
                                }
                                },
                                "cv": {
                                "method": "KFold",
                                "kwargs": {
                                    "n_splits": 10,
                                    "shuffle": true
                                },
                                "penalty": 0.0
                                }
                            },
                            "estimator": {
                                "method": "LinearRegression"
                            },
                            "feature_selection": {
                                "method": "GeneticAlgorithm",
                                "kwargs": {
                                "constraints_kwargs": {
                                    "n_features_max": 20,
                                    "n_features_min": 3,
                                    "fix_off": [],
                                    "fix_on": [0,1,2]
                                },
                                "selTournamentSize": 3,
                                "mutFlipBitProb": 0.01,
                                "evolve_params_kwargs": {
                                    "n_generation": 20,
                                    "n_repetition": 20,
                                    "n_features_init": 3,
                                    "n_population": 5,
                                    "n_halloffame": 10
                                },
                                "cxUniformProb": 0.5
                                }
                            },
                            "n_halloffame": 10,

                            "checkhull" : {
                                "selection": "ALL",
                                "write_results": true,
                                "primitive_only": true,
                                "uncalculated_range": 1e-8,
                                "ranged_rms": [0.001, 0.005, 0.01, 0.05, 0.1, 0.5],
                                "composition": "atom_frac",
                                "hull_tol": 1e-8,
                                "dim_tol": 1e-8,
                                "bottom_tol": 1e-8
                                }
                            }
                        ''' % (str(A[i]), str(B[j]), str(kt[k]))

            with open(fitname+'/genetic_alg_settings.json', 'w') as settings_file:
                settings_file.write(template)
                settings_file.close()
            
            os.chdir(fitname)

            if run_fits:
                os.system('rm check.0; rm checkhull_genetic_alg_settings_0_*; rm genetic_alg_settings_*')
                os.system('casm-learn -s genetic_alg_settings.json > fit.out')
                os.system('casm-learn -s genetic_alg_settings.json --checkhull --indiv 0 > check.0')
            
            #collects full DFT and CLEX data, and generates plots for all fits
            os.system('casm-learn -s genetic_alg_settings.json --select 0')
            os.system('casm query -k comp formation_energy hull_dist clex clex_hull_dist -o full_formation_energies.txt')
            os.system('plot_clex_hull_data.py `pwd` 0')
            os.chdir('../')
            


