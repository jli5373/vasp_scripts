#!/Users/derickober/anaconda3/bin/python

import numpy as np 
import sys
import os
from pymatgen import Structure
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer
from pymatgen.io.vasp.inputs import Kpoints
from pymatgen.core import Structure
from pymatgen.symmetry.bandstructure import HighSymmKpath

'''
Prepares conventional standard primitive cells and k point paths for band structure calculations
'''


searchDir = sys.argv[1]

#walk through directories
for subdir, dirs, files in os.walk(searchDir):
    for file in files:
        if file=='casm_poscar.vasp':
            
            casmPoscarPath = os.path.join(subdir, file)

            #get the conventional standard primitive cell from the poscar
            structure = Structure.from_file(casmPoscarPath)
            spg_analy =SpacegroupAnalyzer(structure)
            primitive_standard_structure=spg_analy.get_primitive_standard_structure(international_monoclinic=False)
            primitive_standard_structure.to(fmt="poscar", filename=os.path.join(subdir, 'POSCAR'))

            #write the kpoint path based on the conventional standard primitive cell 
            struct = Structure.from_file(os.path.join(subdir, 'POSCAR'))
            kpath = HighSymmKpath(struct)
            kpts = Kpoints.automatic_linemode(divisions=45,ibz=kpath)
            kpts.write_file(os.path.join(subdir, 'Kpath'))
            


            #print(subdir)
        #print(os.path.join(subdir, file))