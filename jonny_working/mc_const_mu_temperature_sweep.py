import numpy as np
import argparse
import os
import json 


#Parse input parameters
#format is: python path/to/script -monte_dir path/to/mc_runs/
parser = argparse.ArgumentParser()
parser.add_argument("--monte_dir", '-md', help="full path to your monte carlo directory. Preferrably path/to/casm_root/mc_runs/")
parser.add_argument('--run_monte', nargs='?', const=False, type=bool, default=False, help="If True, will execute the MC runs. If false, will only generate the settings files and folders")
args = parser.parse_args()
mc_runs_directory = args.monte_dir
run_monte_carlo = args.run_monte


#Path to vasp_scripts templates directory
mc_template_path = '/home/jonnyli/Desktop/vasp_scripts/templates/mc_fixed_mu_temperature_sweep_template.json'


#User defined inputs  
chem_potential = np.linspace(0.4,1.0,13)
temperature_low = 100
temperature_high = 1500
temperature_increment = 50.0

#Leave on false to format necessary directories and settings files. Change to True to run metropolis monte carlo
#run_monte_carlo = False       


#read in the template settings.json file
with open(mc_template_path) as f:
  settings_mc = json.load(f)

#iterate through the user-defined chemical potential values; perform monte carlo across a range of temperatures between temperature_low and temperature_high for each chemical potential value
for i, mu in enumerate(chem_potential):
    new_mc_run_name = 'mu_%.4f_T_%d_%d' % (mu, temperature_low, temperature_high)
    current_dir  = os.path.join(mc_runs_directory, new_mc_run_name)
    os.makedirs(current_dir, exist_ok=True)
    os.chdir(current_dir)

    #modify the settings.json template, found in vasp_scripts/templates
    settings_mc['driver']['initial_conditions']['param_chem_pot']['a'] = mu
    settings_mc['driver']['final_conditions']['param_chem_pot']['a'] = mu
    settings_mc['driver']['initial_conditions']['temperature'] = temperature_low
    settings_mc['driver']['final_conditions']['temperature'] = temperature_high
    settings_mc['driver']['incremental_conditions']['temperature'] = temperature_increment
    
    #if this is not the first chemical potential value, use the "final_state.json from the previous chemical potential"
    if i > 0:
      last_condition = 'conditions.%d' % int((temperature_high - temperature_low) / temperature_increment)
      last_output = os.path.join(mc_runs_directory, 'mu_%.4f_T_%d_%d' % (chem_potential[i-1], temperature_low, temperature_high), last_condition, 'final_state.json' )
      settings_mc['driver']['motif'].update({"configdof":last_output})

    #Write formatted setting.json file to the current monte carlo run directory
    with open(os.path.join(current_dir, 'mc_settings.json'), 'w') as settings_file:
        json.dump( settings_mc, settings_file, indent=4)
    settings_file.close()
    
    #Run monte carlo
    if run_monte_carlo:
      os.system('casm monte -s mc_settings.json > mc_results.out')

    os.chdir(mc_runs_directory)


