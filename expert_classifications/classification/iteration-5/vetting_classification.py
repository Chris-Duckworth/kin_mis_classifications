# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------
# vetting_classifications
#
# Iteration-5: The classifications are now complete. Now on to vetting. This script checks 
# the clean sample.
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

# ---------------------------------------------------------------------------------------

file_dir = '/Users/cd201/mpl8-kin-mis/plots/pa_fits/'
adobe = '/Applications/Adobe Acrobat Reader DC.app/Contents/MacOS/AdobeReader'
outpath = '/Users/cd201/mpl8-kin-mis/classification/iteration-5/'

# ---------------------------------------------------------------------------------------
# Writing vetting function.
# i.e. easy to skip to the next file but can input when required.

def vetting(tab, pifu, file_dir, adobe):
    # Finding file.
    path = file_dir + str(pifu) + '-PA.pdf'
    
    # Checking if file exists.
    if os.path.isfile(path) == True:
        # If it does, opening in adobe reader.
        p = subprocess.Popen([adobe, path], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        
        # Vetting. 
        reclassify = input('Does this galaxy need reclassifying? (y/n) \n')
        
        while (reclassify != 'y') & (reclassify != 'n'):
            reclassify = input('y or n \n')
         
        if reclassify == 'n':
            # Returning original classifications.
            SQ = tab.STEL_QUAL.values[tab.plateifu.values == pifu][0]
            GQ = tab.GAS_QUAL.values[tab.plateifu.values == pifu][0]
            SF = tab.STEL_FEATURE.values[tab.plateifu.values == pifu][0]
            GF = tab.GAS_FEATURE.values[tab.plateifu.values == pifu][0]
            GN = tab.GAS_NOTES.values[tab.plateifu.values == pifu][0]
            p.kill()
            return SQ, GQ, SF, GF, GN
        
        # if yes, then is reclassified.
        
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

# ---------------------------------------------------------------------------------------
# Testing out with a random subsample.
# 
# tab = pd.read_csv('/Users/cd201/mpl8-kin-mis/classification/iteration-4/fine-classifications-iter4.csv')
# test = tab[0:10]
# test.to_csv('test_before.csv', index=None)
# 
# for pifu in test.plateifu.values:
#     mask = test.plateifu.values == pifu
#     test['STEL_QUAL'][mask], test['GAS_QUAL'][mask], test['STEL_FEATURE'][mask], test['GAS_FEATURE'][mask], test['GAS_NOTES'][mask] = vetting(test, pifu, file_dir, adobe)
# 
# test.to_csv('test_after.csv',index=None)

# ---------------------------------------------------------------------------------------
# Vetting the clean subsample.

tab = pd.read_csv('/Users/cd201/mpl8-kin-mis/classification/iteration-4/fine-classifications-iter4.csv')
clean = tab[tab.classification.values == 3]

for pifu in clean.plateifu.values:
    mask = clean.plateifu.values == pifu
    clean['STEL_QUAL'][mask], clean['GAS_QUAL'][mask], clean['STEL_FEATURE'][mask], clean['GAS_FEATURE'][mask], clean['GAS_NOTES'][mask] = vetting(clean, pifu, file_dir, adobe)

clean.to_csv(outpath+'classifications-vetted.csv',index=None)
# ---------------------------------------------------------------------------------------
