# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------
# tidy_fine_classifications
#
# Iteration-4: This combines and then tidies the classifications from the previous 
# iteration.
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
# Loading in separate classification files from iteration-3 to be combined.

dont_use = pd.read_csv('/Users/cd201/mpl8-kin-mis/classification/iteration-3/fine_classifications-dont-use.csv')
messy = pd.read_csv('/Users/cd201/mpl8-kin-mis/classification/iteration-3/fine_classifications-messy.csv')
clean = pd.read_csv('/Users/cd201/mpl8-kin-mis/classification/iteration-3/fine_classifications-clean.csv')
kdc = pd.read_csv('/Users/cd201/mpl8-kin-mis/classification/iteration-3/fine_classifications-kdc.csv')
warp = pd.read_csv('/Users/cd201/mpl8-kin-mis/classification/iteration-3/fine_classifications-warp.csv')
funky = pd.read_csv('/Users/cd201/mpl8-kin-mis/classification/iteration-3/fine_classifications-funky.csv')
incoh_gas = pd.read_csv('/Users/cd201/mpl8-kin-mis/classification/iteration-3/fine_classifications-incoh-gas.csv')

# ---------------------------------------------------------------------------------------
# Viewing pdfs of vfields in adobe due to strange error with preview access permissions.

file_dir = '/Users/cd201/mpl8-kin-mis/plots/pa_fits/'
adobe = '/Applications/Adobe Acrobat Reader DC.app/Contents/MacOS/AdobeReader'
outpath = '/Users/cd201/mpl8-kin-mis/classification/iteration-4/'

# ---------------------------------------------------------------------------------------
# Combining dataframe into one. 

frames = [dont_use, messy, clean, kdc, warp, funky, incoh_gas]
combined_tab = pd.concat(frames)

# ---------------------------------------------------------------------------------------
# Defining function which can redefine a given galaxy. ( for the misclassified).
#
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

# ---------------------------------------------------------------------------------------
# Reclassifying the wrongly categorised.

# misclassified = np.array(['8081-6104', '8145-3702', '8595-3703', '9086-6101', '10215-6101',
#                           '10509-12705', '7991-3701', '8135-3702', '8137-6102', '8153-3702',
#                           '8245-6103', '8252-3704', '8256-3704', '8438-3704', '8438-6102',
#                           '8438-6103', '8553-6101', '8611-1902', '8623-6104', '8623-9101',
#                           '8624-12702', '8711-9102', '8715-12705', '8720-9102', '8721-12703',
#                           '8721-3702', '8722-6104', '8938-6103', '8940-9102', '8944-6102', 
#                           '8947-3704', '8980-6104', '8980-9101', '8992-12705', '9091-3701',
#                           '9193-6101', '9196-3702', '9511-6101', '9885-6102'])

# accidentally misclassified again. 
misclassified = np.array(['8137-6102', '8938-6103'])

# Updating.
for pifu in misclassified:
    mask = combined_tab.plateifu.values == pifu
    combined_tab['STEL_QUAL'][mask], combined_tab['GAS_QUAL'][mask], combined_tab['STEL_FEATURE'][mask], combined_tab['GAS_FEATURE'][mask], combined_tab['GAS_NOTES'][mask] = fine_classify(pifu, file_dir, adobe)

combined_tab.to_csv(outpath+'fine-classifications-iter4.csv', index=None)
# ---------------------------------------------------------------------------------------