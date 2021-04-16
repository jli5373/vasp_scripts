#!/Users/derickober/anaconda3/bin/python
from pymatgen import Structure
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer
import numpy as np
import sys


#get the conventional standard primitive cell from the poscar
structure = Structure.from_file(sys.argv[1])
spg_analy =SpacegroupAnalyzer(structure)
primitive_standard_structure=spg_analy.get_primitive_standard_structure(international_monoclinic=False)
primitive_standard_structure.to(fmt="poscar", filename=sys.argv[1].split('.')[0] + '_standard_primitive.vasp')
