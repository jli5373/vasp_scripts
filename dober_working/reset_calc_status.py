import os 
import sys
import argparse
import json
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument("--training_dir", '-td', help="full path to your casm training_data directory. Preferrably path/to/casm_root/training_data/")
parser.add_argument('--config_selection', '-cs', help="json file containing the configuration paths (eg:SCEL2_1_2_1_1_0_0/0/ of the configs that you wish to recalculate with vasp")
args = parser.parse_args()
training_dir = args.training_dir
config_selection_file = args.config_selection

newstatus = {"status":"not_submitted"}

print(config_selection_file)

with open(config_selection_file ) as f:
  config_selection = json.load(f)
  f.close()

for entry in config_selection:
    #print('resetting config: ', end='')
    #print(entry['configname'])
    status_path = os.path.join(training_dir,entry['configname'],'calctype.default','status.json')
    print('resetting %s' % status_path)

    with open(status_path) as f
        json.dump(new_status, f)
        f.close()

