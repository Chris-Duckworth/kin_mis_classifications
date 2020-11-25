# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------
# classify_vfield
#
# Given that we have tabledata of the raw pa classifications and velocity fields with 
# the fits overlaid; this script aids in eyeballing the sample to check if the 
# classifications have worked.
#
# Chris J Duckworth cd201@st-andrews.ac.uk
# ---------------------------------------------------------------------------------------

import os 
import numpy as np
import pandas as pd
import subprocess
import time

# ---------------------------------------------------------------------------------------
# Loading in csv containing all of the galaxies.
tab_raw = pd.read_csv('/Users/cd201/mpl8-kin-mis/catalogues/MPL8-PA-FIT-RAW.csv')

# ---------------------------------------------------------------------------------------
# Viewing pdfs of vfields in adobe due to strange error with preview access permissions.

file_dir = '/Users/cd201/mpl8-kin-mis/plots/pa_fits/'
adobe = '/Applications/Adobe Acrobat Reader DC.app/Contents/MacOS/AdobeReader'
outpath = '/Users/cd201/mpl8-kin-mis/classification/iteration-1/raw_classifications-'

# ---------------------------------------------------------------------------------------
# Main calling sequence.

plateifus = tab_raw.plateifu
classifications = np.full(plateifus.shape, -99)

for i, pifu in enumerate(plateifus):
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
                    response = input('0-5 please. \n')
        
        classifications[i] = response
        p.kill()
        
    # If file doesn't exist, the classification is void. 
    else:
        classifications[i] = -99
        print(str(pifu)+' not found.')
    
    # Saving every 50 classifications.
    if i % 50 == 0:
        print(str(i)+' down. Backing up classifications.')
        tab_raw['classification'] = classifications
        tab_raw.to_csv(outpath+str(i)+'.csv', index=None)

# Final update.
tab_raw['classification'] = classifications
# Saving complete classifications.
tab_raw.to_csv(outpath+'all.csv', index=None)

# ---------------------------------------------------------------------------------------