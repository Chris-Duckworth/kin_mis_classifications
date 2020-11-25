# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------
# pa_find
#
# This script finds the pa for the stellar and halpha velocity fields and returns the
# position angle difference between them in a table format. Various cleaning is performed
# to the velocity maps (e.g. removing bad pixels or other small objects in the ifu).
#
# Chris J Duckworth cd201@st-andrews.ac.uk
# ---------------------------------------------------------------------------------------

import numpy as np
import pa_funcs 
import pandas as pd
from multiprocessing import Pool
import matplotlib.pyplot as plt
import time
from mangadap.util.bitmask import BitMask
import os
from astropy.io import fits
import sys

# ---------------------------------------------------------------------------------------
# defining number of processes to use. since this is local, lets not go crazy.
processes = os.cpu_count()

# ---------------------------------------------------------------------------------------
# Setting up environment of loading in non-critical files.

drpall = fits.open('/Users/cd201/Data/MaNGA/MPL-8-DAP/find_maps/drpall-v2_5_3.fits')[1].data
gal = drpall[(((drpall.mngtarg1 != 0) | (drpall.mngtarg3 != 0)) & ((drpall.mngtarg3 & int(2)**int(19)+int(2)**int(20)) == 0) )]
sdssMaskbits = os.path.join(os.environ['IDLUTILS_DIR'], 'data', 'sdss', 'sdssMaskbits.par')
bm = BitMask.from_par_file(sdssMaskbits, 'MANGA_DRP3QUAL')
critical = bm.flagged(gal.drp3qual, flag='CRITICAL')
data_dir = '/Users/cd201/Data/MaNGA/MPL-8-DAP/VOR10-GAU-MILESHC/'

# ---------------------------------------------------------------------------------------
# Defining wrapper function for multiprocessing. 

def multiproc_wrapper(gal_str):
    file_name = 'manga-'+gal_str+'-MAPS-VOR10-MILESHC-MILESHC.fits.gz'
    file_path = os.path.join(data_dir, gal_str.split("-")[0], gal_str.split("-")[1],file_name)
    plt.close()
    stellar_pa, halpha_pa  = pa_funcs.pa_wrapper(file_path, plot=True)
    plt.savefig('/Users/cd201/mpl8-kin-mis/plots/pa_fits/'+gal_str+'-PA.pdf', format='pdf', bbox_inches='tight')
    return stellar_pa, halpha_pa

# ---------------------------------------------------------------------------------------
# Multiprocessing. For some reason, the plotting causes the processes to hang. There is 
# nothing wrong with the function. 

# start = time.time()
# if __name__ == '__main__':
#     p = Pool(processes)
#     output = p.map(multiproc_wrapper, gal[~critical]['plateifu'][0:100] )

# ending timing sequence.
# end = time.time()
# print(end - start)

# ---------------------------------------------------------------------------------------
# Fuck this, brute forcing this on a single process. :( 

input_plateifus = gal[~critical]['plateifu']
stellar_pa = np.zeros(input_plateifus.shape)
halpha_pa = np.zeros(input_plateifus.shape)

for i, gal_str in enumerate(input_plateifus):
    stellar_pa[i], halpha_pa[i] = multiproc_wrapper(gal_str)
    progress = str(100*i/input_plateifus.shape[0])+'%'
    sys.stdout.write('\r'+progress)
    sys.stdout.flush()

# ---------------------------------------------------------------------------------------
# Saving this to a dataframe.

tab = pd.DataFrame({'plateifu':input_plateifus, 'stellar_pa':stellar_pa, 'halpha_pa':halpha_pa},columns=['plateifu', 'stellar_pa', 'halpha_pa'])
tab.to_csv('/Users/cd201/mpl8-kin-mis/catalogues/MPL8-PA-FIT-RAW.csv',index=None)