import numpy as np
import argparse
import os
import json 



parser = argparse.ArgumentParser()
parser.add_argument("-monte_dir", help="full path to your monte carlo directory. Preferrably path/to/casm_root/mc_runs/")
args = parser.parse_args()



mc_template_path = '/home/derick/vasp_scripts/templates/mc_fixed_mu_temperature_sweep_template.json'
mc_runs_directory = args.monte_dir

chem_potential = np.linspace(-1.75, -1, 4)

temperature_low = 100
temperature_high = 1000
temperature_increment = 10.0

with open(mc_template_path) as f:
  settings_mc = json.load(f)


for i, mu in enumerate(chem_potential):

    new_mc_run_name = 'mu_%.4f_T_%d_%d' % (mu, temperature_low, temperature_high)
    current_dir  = os.path.join(mc_runs_directory, new_mc_run_name)
    os.makedirs(current_dir, exist_ok=True)
    os.chdir(current_dir)

    settings_mc['driver']['initial_conditions']['param_chem_pot']['a'] = mu
    settings_mc['driver']['final_conditions']['param_chem_pot']['a'] = mu

    settings_mc['driver']['initial_conditions']['temperature'] = temperature_low
    settings_mc['driver']['final_conditions']['temperature'] = temperature_high
    settings_mc['driver']['incremental_conditions']['temperature'] = temperature_increment


    
    with open(os.path.join(current_dir, 'mc_settings.json'), 'w') as settings_file:
        json.dump( settings_mc, settings_file, indent=4)
        #settings_file.write(writeable_settings)
    settings_file.close()
    

    os.system('casm monte -s mc_settings.json > mc_results.out')

    os.chdir(mc_runs_directory)


