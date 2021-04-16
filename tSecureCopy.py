#!/Users/derickober/anaconda3/bin/python

import sys
import subprocess

source = sys.argv[1]
destination = sys.argv[2]

destination = 'derick@73.63.184.227:' + destination

subprocess.run(['scp','-r','-P 2025', source, destination])
