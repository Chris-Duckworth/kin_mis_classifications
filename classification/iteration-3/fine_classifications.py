# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------
# fine_classifications
#
# Iteration-3: This script will sort the initial coarse classifications into finer
# categories, allowing for finer selection.
#
# Classification format:
# 
# STEL_QUAL
# 0 - DON'T USE
# 1 - MESSY
# 2 - CLEAN
# 
# GAS_QUAL
# 0 - DON'T USE
# 1 - MESSY
# 2 - CLEAN
# 
# STEL_FEATURE
# 0 - NONE
# 1 - KDC
# 2 - WARP
# 3 - MERGER
# 
# GAS_FEATURE
# 0 - NONE
# 1 - KDC
# 2 - WARP
# 3 - MERGER
# 
# GAS_NOTES (ONLY DEFINED FOR STEL_QUAL == 1 OR 2 AND GAS_QUAL == 0)
# 0 - NONE
# 1 - DEPLETION
# 2 - NO CLEAR ROTATION 
# 3 - ROTATION BUT BIASED
# 
# Chris J Duckworth cd201@st-andrews.ac.uk
# ---------------------------------------------------------------------------------------

import os 
import numpy as np
import pandas as pd
import subprocess
import time

# ---------------------------------------------------------------------------------------
# Loading in csv of classifications from iteration 2.
tab = pd.read_csv('/Users/cd201/mpl8-kin-mis/classification/iteration-2/raw_classifications-iter2-c.csv')

# ---------------------------------------------------------------------------------------
# Viewing pdfs of vfields in adobe due to strange error with preview access permissions.

file_dir = '/Users/cd201/mpl8-kin-mis/plots/pa_fits/'
adobe = '/Applications/Adobe Acrobat Reader DC.app/Contents/MacOS/AdobeReader'
outpath = '/Users/cd201/mpl8-kin-mis/classification/iteration-3/'

# ---------------------------------------------------------------------------------------
# Since the finer classification categories only apply for certain coarse classifications, 
# we break down these into individual dataframes to be combined later.

# ---------------------------------------------------------------------------------------
# Firstly lets consider the 'DON'T USE'

dont_use_mask = tab.classification.values == 0
dont_use_tab = tab[dont_use_mask]
dont_use_tab = dont_use_tab.reset_index(drop=True)

# defining new classifications.
dont_use_tab['STEL_QUAL'] = np.zeros(dont_use_tab.shape[0]).astype(int)
dont_use_tab['GAS_QUAL'] = np.zeros(dont_use_tab.shape[0]).astype(int)
dont_use_tab['STEL_FEATURE'] = np.zeros(dont_use_tab.shape[0]).astype(int)
dont_use_tab['GAS_FEATURE'] = np.zeros(dont_use_tab.shape[0]).astype(int)
dont_use_tab['GAS_NOTES'] = np.zeros(dont_use_tab.shape[0]).astype(int)

# Saving individual DF.
dont_use_tab.to_csv(outpath+'fine_classifications-dont-use.csv', index=None)

# ---------------------------------------------------------------------------------------
# Secondly lets consider the 'MESSY BUT USABLE'

messy_mask = tab.classification.values == 1
messy_tab = tab[messy_mask]
messy_tab = messy_tab.reset_index(drop=True)

# defining new classifications.
messy_tab['STEL_QUAL'] = np.ones(messy_tab.shape[0]).astype(int)
messy_tab['GAS_QUAL'] = np.ones(messy_tab.shape[0]).astype(int)
messy_tab['STEL_FEATURE'] = np.zeros(messy_tab.shape[0]).astype(int)
messy_tab['GAS_FEATURE'] = np.zeros(messy_tab.shape[0]).astype(int)
messy_tab['GAS_NOTES'] = np.zeros(messy_tab.shape[0]).astype(int)

# Saving individual DF.
messy_tab.to_csv(outpath+'fine_classifications-messy.csv', index=None)

# ---------------------------------------------------------------------------------------
# Thirdly the 'CLEAN' sample

clean_mask = tab.classification.values == 3
clean_tab = tab[clean_mask]
clean_tab = clean_tab.reset_index(drop=True)

# defining new classifications.
clean_tab['STEL_QUAL'] = np.full(clean_tab.shape[0], 2).astype(int)
clean_tab['GAS_QUAL'] = np.full(clean_tab.shape[0], 2).astype(int)
clean_tab['STEL_FEATURE'] = np.zeros(clean_tab.shape[0]).astype(int)
clean_tab['GAS_FEATURE'] = np.zeros(clean_tab.shape[0]).astype(int)
clean_tab['GAS_NOTES'] = np.zeros(clean_tab.shape[0]).astype(int)

# Saving individual DF.
clean_tab.to_csv(outpath+'fine_classifications-clean.csv', index=None)

# ---------------------------------------------------------------------------------------
# Now it gets more complex and we have to do more classifications.
# Lets define a few functions to do this.

# This function will be used for fine_classifications that require input for all
# of the fine categories.

def fine_classify(pifu, file_dir, adobe):
    # Finding file.
    path = file_dir + str(pifu) + '-PA.pdf'
    
    # Checking if file exists.
    if os.path.isfile(path) == True:
        # If it does, opening in adobe reader.
        p = subprocess.Popen([adobe, path], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        
        # STEL_QUAL
        SQ = input(str(pifu)+'\nSTELLAR_QUAL; 0 - Dont use, 1 - Messy, 2 - Clean \n') 
                
        try:
            SQ = int(SQ)          
        except ValueError:  
            while type(SQ) == str:
                try:
                    SQ = int(SQ)   
                except ValueError:
                    SQ = input('Needs to be numeric \n')
        
        # GAS_QUAL
        GQ = input('GAS_QUAL; 0 - Dont use, 1 - Messy, 2 - Clean \n') 
                
        try:
            GQ = int(GQ)          
        except ValueError:  
            while type(GQ) == str:
                try:
                    GQ = int(GQ)   
                except ValueError:
                    GQ = input('Needs to be numeric \n')
        
        # STEL_FEATURE
        SF = input('STELLAR_FEATURE; 0 - None, 1 - KDC, 2 - Warp, 3 - Merger \n') 
                
        try:
            SF = int(SF)          
        except ValueError:  
            while type(SF) == str:
                try:
                    SF = int(SF)   
                except ValueError:
                    SF = input('Needs to be numeric \n')
        
        # GAS_FEATURE
        GF = input('GAS_FEATURE; 0 - None, 1 - KDC, 2 - Warp, 3 - Merger \n') 
                
        try:
            GF = int(GF)          
        except ValueError:  
            while type(GF) == str:
                try:
                    GF = int(GF)   
                except ValueError:
                    GF = input('Needs to be numeric \n')
        
        # GAS_NOTES
        GN = input('GAS_NOTES; 0 - NA, 1 - Central Depletion, 2 - Dispersion Dominated \n') 
                
        try:
            GN = int(GN)          
        except ValueError:  
            while type(GN) == str:
                try:
                    GN = int(GN)   
                except ValueError:
                    GN = input('Needs to be numeric \n')
        
        p.kill()
        
    # If file doesn't exist, the classification is void. 
    else:
        SQ, GQ, SF, GF, GN = -99, -99, -99, -99, -99
        print(str(pifu)+' not found.')

    return SQ, GQ, SF, GF, GN
    
# Also defining a similar function which only requires classifications of SQ and GN.

def SQ_GN_classify(pifu, file_dir, adobe):
    # Finding file.
    path = file_dir + str(pifu) + '-PA.pdf'
    
    # Checking if file exists.
    if os.path.isfile(path) == True:
        # If it does, opening in adobe reader.
        p = subprocess.Popen([adobe, path], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        
        # STEL_QUAL
        SQ = input(str(pifu)+'\nSTELLAR_QUAL; 0 - Dont use, 1 - Messy, 2 - Clean \n') 
                
        try:
            SQ = int(SQ)          
        except ValueError:  
            while type(SQ) == str:
                try:
                    SQ = int(SQ)   
                except ValueError:
                    SQ = input('Needs to be numeric \n')
        
        # GAS_NOTES
        GN = input('GAS_NOTES; 0 - NA, 1 - Central Depletion, 2 - Dispersion Dominated \n') 
                
        try:
            GN = int(GN)          
        except ValueError:  
            while type(GN) == str:
                try:
                    GN = int(GN)   
                except ValueError:
                    GN = input('Needs to be numeric \n')
        
        p.kill()
        
    # If file doesn't exist, the classification is void. 
    else:
        print(str(pifu)+' not found.')
        return -99, -99, -99, -99, -99
        
    return SQ, 0, 0, 0, GN

# ---------------------------------------------------------------------------------------
# Now lets consider the 'KDCs'

# These require flags across the board.
kdc_mask = tab.classification.values == 4
kdc_tab = tab[kdc_mask]
kdc_tab = kdc_tab.reset_index(drop=True)

# defining empty classifications.
kdc_tab['STEL_QUAL'] = np.full(kdc_tab.shape[0], -99).astype(int)
kdc_tab['GAS_QUAL'] = np.full(kdc_tab.shape[0], -99).astype(int)
kdc_tab['STEL_FEATURE'] = np.full(kdc_tab.shape[0], -99).astype(int)
kdc_tab['GAS_FEATURE'] = np.full(kdc_tab.shape[0], -99).astype(int)
kdc_tab['GAS_NOTES'] = np.full(kdc_tab.shape[0], -99).astype(int)

# Since classification function works on a singular basis, running through a loop.
for i, pifu in enumerate(kdc_tab.plateifu.values):
    kdc_tab['STEL_QUAL'][i], kdc_tab['GAS_QUAL'][i], kdc_tab['STEL_FEATURE'][i], kdc_tab['GAS_FEATURE'][i], kdc_tab['GAS_NOTES'][i] = fine_classify( pifu, file_dir, adobe)

# Saving individual DF.
kdc_tab.to_csv(outpath+'fine_classifications-kdc.csv', index=None)

# ---------------------------------------------------------------------------------------
# Lets now consider the 'warps'

# These require flags across the board.
warp_mask = tab.classification.values == 5
warp_tab = tab[warp_mask]
warp_tab = warp_tab.reset_index(drop=True)

# defining empty classifications.
warp_tab['STEL_QUAL'] = np.full(warp_tab.shape[0], -99).astype(int)
warp_tab['GAS_QUAL'] = np.full(warp_tab.shape[0], -99).astype(int)
warp_tab['STEL_FEATURE'] = np.full(warp_tab.shape[0], -99).astype(int)
warp_tab['GAS_FEATURE'] = np.full(warp_tab.shape[0], -99).astype(int)
warp_tab['GAS_NOTES'] = np.full(warp_tab.shape[0], -99).astype(int)

# Since classification function works on a singular basis, running through a loop.
for i, pifu in enumerate(warp_tab.plateifu.values):
    warp_tab['STEL_QUAL'][i], warp_tab['GAS_QUAL'][i], warp_tab['STEL_FEATURE'][i], warp_tab['GAS_FEATURE'][i], warp_tab['GAS_NOTES'][i] = fine_classify( pifu, file_dir, adobe)

# Saving individual DF.
warp_tab.to_csv(outpath+'fine_classifications-warp.csv', index=None)

# ---------------------------------------------------------------------------------------
# On to the 'funky'

# These require flags across the board.
funky_mask = tab.classification.values == 6
funky_tab = tab[funky_mask]
funky_tab = funky_tab.reset_index(drop=True)

# defining empty classifications.
funky_tab['STEL_QUAL'] = np.full(funky_tab.shape[0], -99).astype(int)
funky_tab['GAS_QUAL'] = np.full(funky_tab.shape[0], -99).astype(int)
funky_tab['STEL_FEATURE'] = np.full(funky_tab.shape[0], -99).astype(int)
funky_tab['GAS_FEATURE'] = np.full(funky_tab.shape[0], -99).astype(int)
funky_tab['GAS_NOTES'] = np.full(funky_tab.shape[0], -99).astype(int)

# Since classification function works on a singular basis, running through a loop.
for i, pifu in enumerate(funky_tab.plateifu.values):
    funky_tab['STEL_QUAL'][i], funky_tab['GAS_QUAL'][i], funky_tab['STEL_FEATURE'][i], funky_tab['GAS_FEATURE'][i], funky_tab['GAS_NOTES'][i] = fine_classify( pifu, file_dir, adobe)

# Saving individual DF.
funky_tab.to_csv(outpath+'fine_classifications-funky.csv', index=None)

# ---------------------------------------------------------------------------------------
# Finally lets consider the incoherent gas and usable stellar maps.
# 
# These require two classifications.

incoh_gas_mask = tab.classification.values == 2
incoh_gas_tab = tab[incoh_gas_mask]
incoh_gas_tab = incoh_gas_tab.reset_index(drop=True)

# defining empty classifications.
incoh_gas_tab['STEL_QUAL'] = np.full(incoh_gas_tab.shape[0], -99).astype(int)
incoh_gas_tab['GAS_QUAL'] = np.full(incoh_gas_tab.shape[0], -99).astype(int)
incoh_gas_tab['STEL_FEATURE'] = np.full(incoh_gas_tab.shape[0], -99).astype(int)
incoh_gas_tab['GAS_FEATURE'] = np.full(incoh_gas_tab.shape[0], -99).astype(int)
incoh_gas_tab['GAS_NOTES'] = np.full(incoh_gas_tab.shape[0], -99).astype(int)

# Since classification function works on a singular basis, running through a loop.
for i, pifu in enumerate(incoh_gas_tab.plateifu.values):
    incoh_gas_tab['STEL_QUAL'][i], incoh_gas_tab['GAS_QUAL'][i], incoh_gas_tab['STEL_FEATURE'][i], incoh_gas_tab['GAS_FEATURE'][i], incoh_gas_tab['GAS_NOTES'][i] = SQ_GN_classify( pifu, file_dir, adobe)

# Saving individual DF.
incoh_gas_tab.to_csv(outpath+'fine_classifications-incoh-gas.csv', index=None)

# ---------------------------------------------------------------------------------------
