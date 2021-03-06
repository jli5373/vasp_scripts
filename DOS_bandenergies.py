#!/Users/derickober/anaconda3/bin/python

"""
Created on Thu Jan 19 15:39:59 2017

@author: Julija

Plot band energies from VASP
"""

import os
import matplotlib.pyplot as plt
import numpy as np
import sys

#file_path = '/home/harsha/braid_bkp/Ti_Al_O/bulk_Ti_calcs/dos_calcs_rotated/calcs/unrelaxed/bulk_Ti_AlO_def_pos10'
#file_path = '../POSCAR.14_DOS/5.calc_dos'
file_path = sys.argv[1]
spin_pol = False
shift_fermi = True


EIGENVAL_path = os.path.join(file_path, 'EIGENVAL')
DOSCAR_path = os.path.join(file_path, 'DOSCAR')
print(DOSCAR_path)

font = {'color':  'black',
        'size': 8,
        }

#pts=30000

with open(DOSCAR_path) as d:
    line1 = d.readline()
    line2 = d.readline()
    line3 = d.readline()
    line4 = d.readline()
    line5 = d.readline()
    info = d.readline().split()
    efermi = float(info[3])
    pts = int(info[2])
    total_DOS_en = np.zeros((pts, 1))
    total_DOS_up = np.zeros((pts, 1))
    if spin_pol:
        total_DOS_dn = np.zeros((pts, 1))
    for ii in range(pts):
        sline = d.readline().split()
        if len(sline) > 0:
            print(len(sline))
            print(len(total_DOS_en))
            print(ii)
            print('\n')
            total_DOS_en[ii] = float(sline[0])
            total_DOS_up[ii] = float(sline[1])
            if spin_pol:
                total_DOS_dn[ii] = float(sline[2])
    d.close()

fig = plt.figure()

if spin_pol == True:
    with open(EIGENVAL_path) as f:
        line1 = f.readline()
        line2 = f.readline()
        line3 = f.readline()
        line4 = f.readline()
        comment = f.readline()
        unknown, npoints, nbands = [int(x) for x in f.readline().split()]
    
        blankline = f.readline()
    
        band_energies_1 = [[] for i in range(nbands)]
        band_energies_2 = [[] for i in range(nbands)]
    
        for i in range(npoints):
            x, y, z, weight = [float(x) for x in f.readline().split()]
    
            for j in range(nbands):
                fields = f.readline().split()
                id1, energy_1, energy_2 = int(float(fields[0])), float(fields[1]), float(fields[2])
                band_energies_1[id1-1].append(energy_1)
                band_energies_2[id1-1].append(energy_2)
            blankline = f.readline()
        f.close()
    
    rescale_up = npoints*0.5/np.amax(total_DOS_up)
    rescale_dn = npoints*0.5/np.amax(total_DOS_dn)
    rescale = max(rescale_up, rescale_dn)
    band_energies_1 = np.array(band_energies_1)
    band_energies_2 = np.array(band_energies_2)
    if shift_fermi:
        efermi_shift = efermi
    else:
        efermi_shift = 0
        
    band_energies_1 = band_energies_1 - efermi_shift
    band_energies_2 = band_energies_2 - efermi_shift
    efermi = efermi - efermi_shift
    total_DOS_en = total_DOS_en - efermi_shift
    for i in range(nbands):
        plt.subplot(122)
        plt.plot(range(npoints), np.array(band_energies_1[i]))
        plt.text(npoints-1, np.mean(np.array(band_energies_1[i])), i+1, fontdict=font) # up
        plt.plot(range(npoints), np.ones(len(range(npoints)))*efermi, '-', color = 'black', linewidth = 1.5)
        plt.text(npoints-1, efermi, 'E Fermi', fontdict=font)
        plt.plot(total_DOS_up*rescale, total_DOS_en, '-', color = 'black', linewidth = 1.5)
        ax = plt.gca()
        ax.set_xticks([])  # no tick marks
        plt.xlabel('k-vector')
        plt.ylabel('Energy (eV)')
        plt.title('spin up')
        
        plt.subplot(121)
        plt.plot(-1*np.array(range(npoints)), np.array(band_energies_2[i]))
        plt.text(-npoints+1, np.mean(np.array(band_energies_2[i])), i+1.5, fontdict=font) # down
        plt.plot(-1*np.array(range(npoints)), np.ones(len(range(npoints)))*efermi, '-', color = 'black', linewidth = 1.5)
        plt.text(-npoints+1, efermi, 'E Fermi', fontdict=font)
        plt.plot(-total_DOS_dn*rescale, total_DOS_en, '-', color = 'black', linewidth = 1.5)
        ax = plt.gca()
        ax.set_xticks([])  # no tick marks
        plt.xlabel('k-vector')
        plt.title('spin down')
        
    ax = plt.gca()
    plt.suptitle(file_path)
        
elif spin_pol == False:
    with open(EIGENVAL_path) as f:
        line1 = f.readline()
        line2 = f.readline()
        line3 = f.readline()
        line4 = f.readline()
        comment = f.readline()
        unknown, npoints, nbands = [int(x) for x in f.readline().split()]
    
        blankline = f.readline()
    
        band_energies_1 = [[] for i in range(nbands)]
    
        for i in range(npoints):
            x, y, z, weight = [float(x) for x in f.readline().split()]
    
            for j in range(nbands):
                fields = f.readline().split()
                id1, energy_1 = int(float(fields[0])), float(fields[1])
                band_energies_1[id1-1].append(energy_1)
            blankline = f.readline()
        f.close()
    
    band_energies_1 = np.array(band_energies_1)
    if shift_fermi:
        efermi_shift = efermi
    else:
        efermi_shift = 0
    
    rescale = npoints/np.amax(total_DOS_up)
    
    if shift_fermi:
        band_energies_1 = band_energies_1 - efermi_shift
        efermi = efermi - efermi_shift
        total_DOS_en = total_DOS_en - efermi_shift
    ax1 = plt.subplot(111)
    for i in range(nbands):
        plt.plot(range(npoints), np.array(band_energies_1[i]))
        plt.text(npoints-1, np.mean(np.array(band_energies_1[i])), i+1, fontdict=font) # up
        plt.plot(total_DOS_up*rescale, total_DOS_en, '-', color = 'black', linewidth = 1.5)
    
    plt.plot(range(npoints), np.ones(len(range(npoints)))*efermi, '-', color = 'black', linewidth = 2)
    plt.text(npoints, efermi, 'E Fermi', fontdict=font)
    plt.xlabel('k-vector')
    plt.ylabel('Energy (eV)')
    plt.title(file_path)
    
plt.show()
