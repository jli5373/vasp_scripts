#!/Users/derickober/anaconda3/bin/python
import sys

from pymatgen.io.vasp.inputs import Kpoints
from pymatgen.core import Structure
from pymatgen.symmetry.bandstructure import HighSymmKpath

struct = Structure.from_file(sys.argv[1])
kpath = HighSymmKpath(struct)
kpts = Kpoints.automatic_linemode(divisions=40,ibz=kpath)
kpts.write_file("KPOINTS_nsc")
