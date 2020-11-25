# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------
# tidy_classify_vfield
#
# Iteration-2: This script will tidy up the classifications from iteration 1.
#
# Chris J Duckworth cd201@st-andrews.ac.uk
# ---------------------------------------------------------------------------------------

import os 
import numpy as np
import pandas as pd
import subprocess
import time

# ---------------------------------------------------------------------------------------
# Loading in csv of classifications from iteration 1.
tab_raw = pd.read_csv('/Users/cd201/mpl8-kin-mis/classification/iteration-1/raw_classifications-all.csv')

# ---------------------------------------------------------------------------------------
# Viewing pdfs of vfields in adobe due to strange error with preview access permissions.

file_dir = '/Users/cd201/mpl8-kin-mis/plots/pa_fits/'
adobe = '/Applications/Adobe Acrobat Reader DC.app/Contents/MacOS/AdobeReader'
outpath = '/Users/cd201/mpl8-kin-mis/classification/iteration-2/'

# ---------------------------------------------------------------------------------------
# func: classify_pifu
#
# Given a plateifu; will return the vfields and ask for a classification which will be returned.

def classify_pifu(pifu, file_dir):
    # Finding file.
    path = file_dir + str(pifu) + '-PA.pdf'
    
    # Checking if file exists.
    if os.path.isfile(path) == True:
        # If it does, opening in adobe reader.
        p = subprocess.Popen([adobe, path], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        
        # Asking for classification.
        response = input('Please classify this galaxy. ID:'+str(pifu)+'. Type wut for more info on classifications. \n') 
        
        while response == 'wut':
            print('\n0: Dont use \n1: Messy \n2: Incoherent Gas rot but clean stellar \n3: Clean! \n4: KDC \n5: Warp \n6: Dont use but looks funky')
            time.sleep(0.5)
            response = input('So whats it going to be? \n')
        
        try:
            response = int(response)          
        except ValueError:  
            while type(response) == str:
                try:
                    response = int(response)   
                except ValueError:
                    response = input('0-6 please. \n')
        
        p.kill()

    else:
        repsonse = -99
        print(str(pifu)+' not found.')

    return response

# ---------------------------------------------------------------------------------------
# Defining function which given a subsample of classifications, asks for updated 
# classifications and return the updated dataframe.

def redef_subsamp(tab_raw, mask, file_dir):
    for i in np.where(mask)[0]:
        tab_raw.classification.values[i]  = classify_pifu(tab_raw.plateifu.values[i], file_dir)
    return tab_raw

# ---------------------------------------------------------------------------------------
# Selecting redefinitions.

# Firstly selecting all of those that are left unclassified.

unclass_mask = tab_raw.classification.values == -99
tab_raw = redef_subsamp(tab_raw, unclass_mask, file_dir)
# backing-up
tab_raw.to_csv(outpath+'raw_classifications-iter2-a.csv', index=None)

# ---------------------------------------------------------------------------------------
# Redefining all of those with noted misclassifications.

misclassified = np.array(['8337-6102', '8555-6101', '8597-6101', '8719-12705', '8934-12702',
                          '8934-6102', '8947-1901', '8947-3702', '8950-12705', '8985-6104', 
                          '8990-3702', '9026-9101', '9033-6103', '9034-3703', '9050-3703',
                          '9089-3702', '9182-6103', '9186-9101', '9196-3703', '9500-9109',
                          '9502-6103', '9511-6102', '9514-1902', '9879-12702', '9890-9101',
                          '9893-1901'])

# defining mask
mis_mask = np.in1d(tab_raw.plateifu.values, misclassified)
tab_raw = redef_subsamp(tab_raw, mis_mask, file_dir)
# backing-up
tab_raw.to_csv(outpath+'raw_classifications-iter2-b.csv', index=None)

# ---------------------------------------------------------------------------------------
# Checking all classifications fall within 0-6.

typo_mask = tab_raw.classification.values > 6
tab_raw = redef_subsamp(tab_raw, typo_mask, file_dir)
tab_raw.to_csv(outpath+'raw_classifications-iter2-c.csv', index=None)

# ---------------------------------------------------------------------------------------
