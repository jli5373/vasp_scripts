import os
import sys

casm_root = sys.argv[1]
searchdir = os.path.join(casm_root, 'training_data')


with open(os.path.join(casm_root, 'structure_file_path_batch.txt'), 'w') as batchfile:
        
    for subdir, dirs, files in os.walk(searchdir):
        for f in files:
            if f == 'POS':
                batchfile.write(os.path.join(subdir, 'POS')+'\n')
                #print(os.path.join(subdir, 'POS'))
    batchfile.close()

