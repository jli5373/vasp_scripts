import numpy as np 
import os 
import sys 
from PIL import Image



#script to combine cluster fit plots into one pdf document

ce_fits_dir = sys.argv[1]          #the directory of cluster expansion fits. Currently, we use casm_root/ce_fits
print(ce_fits_dir)
os.chdir(ce_fits_dir)

imagelist = []
combined_hull_pdf_name = ce_fits_dir.split('/')[-2] + '_combined_hull_plots.pdf'
for subdir, dirs, files in os.walk(ce_fits_dir):

    

    for f in files:
        if (f.split('.')[-1] == 'png') and (len(f.split(' '))==1):
            print(f)

            image = Image.open(os.path.join(ce_fits_dir,subdir, f))
            im = image.convert('RGB')
            imagelist.append(im)
            im.save(os.path.join(ce_fits_dir,combined_hull_pdf_name), save_all=True, append_images=imagelist)
