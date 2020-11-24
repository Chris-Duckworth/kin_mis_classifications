# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------
# classify_access 
#
# This script returns a dataframe and merged pdf of galaxies of a certain type. 
# 
# Chris J Duckworth cd201@st-andrews.ac.uk
# ---------------------------------------------------------------------------------------

import os 
import numpy as np
import pandas as pd
from PyPDF2 import PdfFileMerger

file_dir = '/Users/cd201/mpl8-kin-mis/plots/pa_fits/'

# ---------------------------------------------------------------------------------------
# Provided a dataframe, this will return the merged pdf of all galaxies selected.

def subsamp_pdf(tab, file_dir, filename):
    pifus = tab.plateifu.values
    
    # merged pdf.
    merger = PdfFileMerger()

    for pifu in pifus:
        merger.append(open(file_dir + str(pifu) + '-PA.pdf', 'rb'))

    with open(str(filename)+'.pdf', 'wb') as fout:
        merger.write(fout)

    merger.close()
    return

# ---------------------------------------------------------------------------------------
# Creating a few example pdfs.

tab = pd.read_csv('/Users/cd201/mpl8-kin-mis/classification/iteration-4/fine-classifications-iter4.csv')

# KDCs of some kind.
mask = (tab.STEL_FEATURE == 1) | (tab.GAS_FEATURE == 1)
kdcs = tab[mask]
subsamp_pdf(kdcs, file_dir, 'KDCs')

# Warps in the gas velocity field only.
mask = (tab.STEL_FEATURE == 0) & (tab.GAS_FEATURE == 2)
gas_warp = tab[mask]
subsamp_pdf(gas_warp, file_dir, 'gas_warps')

# Mergers
mask = (tab.STEL_FEATURE == 3) | (tab.GAS_FEATURE == 3)
merger = tab[mask]
subsamp_pdf(merger, file_dir, 'mergers')

# ---------------------------------------------------------------------------------------


