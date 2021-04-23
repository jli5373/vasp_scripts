import numpy as np
import os
import sys


#Provide scel list file and casm root directory as 1st and second command line arguments
#ex: python spinpol  /path/to/scel_list.txt /path/to/rocksalt_ZrN_casm/training_data/
#scel list file is a lines in the form

#SCEL4_4_1_1_0_1_0/0
#SCEL4_4_1_1_0_1_0/1
#..etc 
scel_list_path = sys.argv[1]
casm_training_dir = sys.argv[2]

#Run-specific parameters
experiment_name = 'spinpol_ZrN_rocksalt_1'
encut = 525
kdensity = 45
ncore = 2
nedos = 301
processors = 4
lwave_on = False           #change to True to write wavecar after static run


#User parameters (for your system)
template_path = '/Users/derickober/vasp_scripts/templates/' #specifically for the incar and submit templates
experiments_path = '/Volumes/Derick_data/experiments'



#read in the scel list file 
scel_list = np.genfromtxt(scel_list_path, dtype=np.str)

#make main experiment directory
experiment_dir = os.path.join(experiments_path,experiment_name)
os.mkdir(experiment_dir)
os.chdir(experiment_dir)

#iterate through scel list
for i in range(len(scel_list)):
    #make scel dir
        os.makedirs(os.path.join(experiment_dir, scel_list[i]))
        #copy poscar, potcar, kpoint, format incar
        os.chdir(os.path.join(experiment_dir, scel_list[i]))
            
        copy_dir = os.path.join(casm_training_dir,scel_list[i] )

        for subdir, dirs, files in os.walk(copy_dir):
            if subdir.split('/')[-1] == 'run.final':
                os.system('cp %s %s' % ( os.path.join(subdir, 'POSCAR'), os.path.join(experiment_dir, scel_list[i])))
                os.system('cp %s %s' % ( os.path.join(subdir, 'POTCAR'), os.path.join(experiment_dir, scel_list[i])))
                os.system('cp %s %s' % ( os.path.join(subdir, 'KPOINTS'), os.path.join(experiment_dir, scel_list[i])))
        
        #format incar files
        with open(os.path.join(template_path, 'INCAR_relax_spinpolarized')) as f:
            template = f.read()
            s = template.format(simulationName=scel_list[i], encut=encut, ncore=ncore, nedos=nedos)
            f.close()
        with open(os.path.join(experiment_dir, scel_list[i], 'INCAR'), 'w') as incar:
            incar.write(s)
            incar.close() 

        #format and run submit

        with open(os.path.join(template_path, 'submit_spinpol_loop_template')) as f:
            template = f.read()
            lwave = ''
            if lwave_on :
                lwave = 'sed -i "s/LWAVE.*/LWAVE = .TRUE." INCAR'

            s = template.format(processors=processors, simulationName=scel_list[i], vaspFilesDir='../', lwave=lwave, experiment_dir=experiment_dir)
            f.close()
        with open(os.path.join(experiment_dir, scel_list[i], 'submit_spinpol_loop') , 'w') as submit:
            submit.write(s)
            submit.close()
        os.system('chmod +x submit_spinpol_loop')
        print('submitting %s ' % scel_list[i])
        #os.system('qsub ')


