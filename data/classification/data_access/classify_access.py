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
from mangadap.util.bitmask import BitMask

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
# mask = (tab.STEL_FEATURE == 1) | (tab.GAS_FEATURE == 1)
# kdcs = tab[mask]
# kdcs.plateifu[46]
# subsamp_pdf(kdcs, file_dir, 'KDCs')
# 
# Warps in the gas velocity field only.
mask = (tab.STEL_FEATURE == 0) & (tab.GAS_FEATURE == 2)
gas_warp = tab[mask]
subsamp_pdf(gas_warp, file_dir, 'gas_warps')

# # Mergers
# mask = (tab.STEL_FEATURE == 3) | (tab.GAS_FEATURE == 3)
# merger = tab[mask]
# subsamp_pdf(merger, file_dir, 'mergers')

# ---------------------------------------------------------------------------------------
# Creating ETG aligned and misaligned samples.
# ---------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------
# func: mpl8_main_sample
#
# This function returns a dataframe containing the main MPL-8 sample (Primary, Secondary and
# Colour-Enhanced) with all repeat observations removed.
# 
# Input: location of file as a str. File must be csv.

def mpl8_main_sample(file):
    mpl8 = pd.read_csv(file, comment='#')
    tab = mpl8[(((mpl8.mngtarg1 != 0) | (mpl8.mngtarg3 != 0)) & ((mpl8.mngtarg3 & int(2)**int(19)+int(2)**int(20)) == 0) )]
    sdssMaskbits = os.path.join(os.environ['IDLUTILS_DIR'], 'data', 'sdss', 'sdssMaskbits.par')
    bm = BitMask.from_par_file(sdssMaskbits, 'MANGA_TARGET1')
    main_sample = bm.flagged(tab.mngtarg1, flag=['PRIMARY_v1_2_0','SECONDARY_v1_2_0','COLOR_ENHANCED_v1_2_0'])
    # Removing ancillary progs and repeat obs.
    mpl8_main = tab[main_sample]
    mpl8_main = mpl8_main.iloc[np.unique(mpl8_main.mangaid.values, return_index=True)[1]]
    return mpl8_main

# ---------------------------------------------------------------------------------------
# func: mpl8_pa_sample 
#
# This function returns a pa defined sample when given the output from mpl8_main_sample.
# This checks there are no repeats in-case main sample comes from another source.

def mpl8_pa_sample(mpl8_main):
    mpl8_pa = mpl8_main[(mpl8_main.stel_feature == 0) & (mpl8_main.halpha_feature == 0) & ((mpl8_main.stel_qual == 1) | (mpl8_main.stel_qual == 2)) & ((mpl8_main.halpha_qual == 1) | (mpl8_main.halpha_qual == 2))]
    mpl8_pa = mpl8_pa.iloc[np.unique(mpl8_pa.mangaid.values, return_index=True)[1]]
    return mpl8_pa

# ---------------------------------------------------------------------------------------
# func: GZ_match
#
# This function loads in the galaxyZoo tabledata (VAC for MaNGA) and matches to a given
# dataframe on MANGAID. 

def GZ_match(GZfile, match):
    gz_info = pd.read_csv(GZfile)
    return pd.merge(gz_info, match, left_on='MANGAID', right_on='mangaid')

# ---------------------------------------------------------------------------------------
# func: morph_breakdown
#
# This function splits an MPL8 dataframe (matched to GZ) into 3 separate dataframes:
# ETG, S0/Sa and Sb/Sd. LTGs are split based on the linear T-type mapping (at 3) in the
# GZ2 paper. Use with care but should be fine for define 'lateness' of LTGs.

def morph_breakdown(main, vote_frac = 0.7, Tsplit = 3):
    ETGs = main[main.t01_smooth_or_features_a01_smooth_debiased >= vote_frac]
    LTGs = main[main.t01_smooth_or_features_a02_features_or_disk_debiased >= vote_frac]
    # defining T-type. Based entirely on bulge prominence.
    Ttype = 4.63 + 4.17 * LTGs.t05_bulge_prominence_a10_no_bulge_debiased - 2.27 * LTGs.t05_bulge_prominence_a12_obvious_debiased - 8.38 * LTGs.t05_bulge_prominence_a13_dominant_debiased
    # dividing on T-type.
    S0_Sa = LTGs[Ttype <= Tsplit]
    Sb_Sd = LTGs[Ttype > Tsplit]
    return ETGs, S0_Sa, Sb_Sd

# ---------------------------------------------------------------------------------------

# Loading in matched Lim catalogue.
lim_main = mpl8_main_sample('/Users/cd201/mpl8-kin-mis/catalogues/lim_match/mpl8-pa-classifications-drp-lim-skymatch-1arc.csv')
# Selecting PA sub-sample.
lim_pa = mpl8_pa_sample(lim_main)
# Finding no gas rotation sample.
lim_ngr = lim_main[((lim_main.halpha_notes == 1) | (lim_main.halpha_notes == 2) )]

GZ_lim_pa = GZ_match('/Users/cd201/morphology_misalignment/catalogues/MaNGA_gz-v1_0_1.csv', lim_pa)
ETGs_lim_pa, S0_Sa_lim_pa, Sb_Sd_lim_pa = morph_breakdown(GZ_lim_pa, vote_frac = 0.7, Tsplit = 3)
GZ_lim_ngr = GZ_match('/Users/cd201/morphology_misalignment/catalogues/MaNGA_gz-v1_0_1.csv', lim_ngr)
ETGs_lim_ngr, S0_Sa_lim_ngr, Sb_Sd_lim_ngr = morph_breakdown(GZ_lim_ngr, vote_frac = 0.7, Tsplit = 3)

ETG_centrals_lim = ETGs_lim_pa[(ETGs_lim_pa.galaxyID.values == ETGs_lim_pa.cenID.values)]
ETG_satellites_lim = ETGs_lim_pa[(ETGs_lim_pa.galaxyID.values != ETGs_lim_pa.cenID.values)]
ETG_centrals_lim_ngr = ETGs_lim_ngr[(ETGs_lim_ngr.galaxyID.values == ETGs_lim_ngr.cenID.values)]
ETG_satellites_lim_ngr = ETGs_lim_ngr[(ETGs_lim_ngr.galaxyID.values != ETGs_lim_ngr.cenID.values)]


subsamp_pdf(ETG_centrals_lim[ETG_centrals_lim.pa_offset.values < 30], file_dir, '/Users/cd201/morphology_misalignment/plots/mpl8/ETG_ifus/ETG_centrals_aligned_lim')
subsamp_pdf(ETG_centrals_lim[ETG_centrals_lim.pa_offset.values >= 30], file_dir, '/Users/cd201/morphology_misalignment/plots/mpl8/ETG_ifus/ETG_centrals_misaligned_lim')

subsamp_pdf(ETG_satellites_lim[ETG_satellites_lim.pa_offset.values < 30], file_dir, '/Users/cd201/morphology_misalignment/plots/mpl8/ETG_ifus/ETG_satellites_aligned_lim')
subsamp_pdf(ETG_satellites_lim[ETG_satellites_lim.pa_offset.values >= 30], file_dir, '/Users/cd201/morphology_misalignment/plots/mpl8/ETG_ifus/ETG_satellites_misaligned_lim')

subsamp_pdf(ETG_centrals_lim_ngr, file_dir, '/Users/cd201/morphology_misalignment/plots/mpl8/ETG_ifus/ETG_centrals_lim_ngr')
subsamp_pdf(ETG_satellites_lim_ngr, file_dir, '/Users/cd201/morphology_misalignment/plots/mpl8/ETG_ifus/ETG_satellites_lim_ngr')