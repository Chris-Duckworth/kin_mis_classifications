# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------
# pa_funcs
#
# This library contains the functions associated with estimating and cleaning the stellar 
# and halpha position angles.
#
# Chris J Duckworth cd201@st-andrews.ac.uk
# ---------------------------------------------------------------------------------------

import numpy as np 
from astropy.io import fits
from skimage import morphology
from fit_kinematic_pa import fit_kinematic_pa
from cap_display_pixels import display_pixels
import os
import matplotlib.pyplot as plt
from astropy.stats import sigma_clip

# ---------------------------------------------------------------------------------------
# func: pa_wrapper
#
# Given a file_path this will call on load_vfields, reg_remove, fit_kinematic_pa and 
# fudge_kinematic_pa to return a filtered vfield with pa fits.

def pa_wrapper(file_path, nsteps=361, plot=True):
    # Checking if file exists. Returning if not.
    if os.path.isfile(file_path) == False: 
        print(file_path + ' missing.')
        return np.nan, np.nan 
    
    hdu = fits.open(file_path)
    grid, stellar_vfield, halpha_vfield = load_vfields(hdu)
    
    # filtering small regions.
    stel_reg = reg_remove(stellar_vfield)
    halpha_reg = reg_remove(halpha_vfield)
    
    # sigma clipping super high velocity regions. this is mainly done so can actually 
    # eyeball the map.
    stel_clipped = sigma_clip(stellar_vfield[stel_reg]) 
    halpha_clipped = sigma_clip(halpha_vfield[halpha_reg])
    
    # defining masked vfields.
    SX, SY, SVEL = grid[0][stel_reg][~stel_clipped.mask], grid[1][stel_reg][~stel_clipped.mask], stel_clipped[~stel_clipped.mask]
    GX, GY, GVEL = grid[0][halpha_reg][~halpha_clipped.mask], grid[1][halpha_reg][~halpha_clipped.mask], halpha_clipped[~halpha_clipped.mask]

    # attempting pa fits. returning nan if fails.
    try:
        # stellar vfield
        stellar_pa,_,_ = fit_kinematic_pa(SX, SY, SVEL, nsteps=nsteps, plot=False, quiet=True)
        # finding fit_kinematic_pa with consistent axis of rotation. (Needed to find difference between 
        # gas and stellar velocity fields).
        stellar_axis = fudge_kinematic_pa(SX, SY, SVEL, stellar_pa)
        # finding fixed pa.
        stellar_pa = stellar_axis + 90 
        if stellar_pa > 360:
            stellar_pa -= 360

    except:
        stellar_pa = np.nan
        stellar_axis = np.nan
    
    try:
        # halpha vfield
        halpha_pa,_,_ = fit_kinematic_pa(GX, GY, GVEL, nsteps=nsteps, plot=False, quiet=True)
        # finding fit_kinematic_pa with consistent axis of rotation. (Needed to find difference between 
        # gas and stellar velocity fields).
        halpha_axis = fudge_kinematic_pa(GX, GY, GVEL, halpha_pa)
        # finding fixed pa.
        halpha_pa = halpha_axis + 90 
        if halpha_pa > 360:
            halpha_pa -= 360

    except:
        halpha_pa = np.nan
        halpha_axis = np.nan

    if plot == True:
        try:
            dual_plot(grid, SX, SY, SVEL, GX, GY, GVEL, stellar_pa, halpha_pa)
        except AssertionError:
            print('Plotting failed for '+gal_str)      

    return stellar_pa, halpha_pa 

# ---------------------------------------------------------------------------------------
# func: dual_plot
# 
# Plots the stellar and halpha velocity fields side by side with pa overlaid.

def dual_plot(grid, SX, SY, SVEL, GX, GY, GVEL, stellar_pa, halpha_pa):
    fig, ax = plt.subplots(1,2, figsize=(10,3))
    # display_pixels doesn't like obj-orientated matplotlib
    plt.sca(ax[0])
    display_pixels(SX, SY, SVEL, colorbar=True)
    ax[0].set_title('STAR-PA: '+str(stellar_pa))
    
    # Plotting 0 and 90 deg lines.
    rad = np.sqrt(np.max(grid[0]**2 + grid[1]**2))
    ang = [0, -np.pi] 
    ax[0].plot(rad*np.cos(ang), rad*np.sin(ang), linestyle='dashed', color='gray', linewidth=3, alpha=0.2)
    ax[1].plot(rad*np.cos(ang), rad*np.sin(ang), linestyle='dashed', color='gray', linewidth=3, alpha=0.2)
    
    ang =  [-np.pi/2, -np.pi*3/2]
    ax[0].plot(rad*np.cos(ang), rad*np.sin(ang), linestyle='dashed', color='gray', linewidth=3, alpha=0.2)
    ax[1].plot(rad*np.cos(ang), rad*np.sin(ang), linestyle='dashed', color='gray', linewidth=3, alpha=0.2)
    
    # Plotting pa lines.
    if stellar_pa != np.nan:
        rad = np.sqrt(np.max(grid[0]**2 + grid[1]**2))
        ang = [0,np.pi] + np.radians(stellar_pa)
        ax[0].plot(rad*np.cos(-ang), rad*np.sin(-ang), 'k--', linewidth=3) # Zero-velocity line
        ax[0].plot(-rad*np.sin(-ang), rad*np.cos(-ang), color="limegreen", linewidth=3) # Major axis PA
    
    # limits and labels.
    ax[0].set_xlim([np.min(grid[0]), np.max(grid[0])])
    ax[0].set_ylim([np.min(grid[1]), np.max(grid[1])])
    ax[0].set_xlabel('arcsec')
    ax[0].set_ylabel('arcsec')

    plt.sca(ax[1])
    display_pixels(GX, GY, GVEL, colorbar=True)
    ax[1].set_title('GAS-PA: '+str(halpha_pa))
    
    # Plotting pa lines.
    if halpha_pa != np.nan:
        rad = np.sqrt(np.max(grid[0]**2 + grid[1]**2))
        ang = [0,np.pi] + np.radians(halpha_pa)
        ax[1].plot(rad*np.cos(-ang), rad*np.sin(-ang), 'k--', linewidth=3) # Zero-velocity line
        ax[1].plot(-rad*np.sin(-ang), rad*np.cos(-ang), color="limegreen", linewidth=3) # Major axis PA
    
    # limits and labels.
    ax[1].set_xlim([np.min(grid[0]), np.max(grid[0])])
    ax[1].set_ylim([np.min(grid[1]), np.max(grid[1])])
    ax[1].set_xlabel('arcsec')
    ax[1].set_ylabel('arcsec')
    return

# ---------------------------------------------------------------------------------------
# func: vfield_reg_rem
#
# Given a velocity field (masked array), this function removes small regions (i.e. objects
# not connected to target galaxy, that may bias the fit). 
    
def reg_remove(vfield, thres=0.1):
    # Only mask required for region size identifier.
    # Selecting total number of pixels with observation, NOT, the total area.
    ms = thres * np.sum(~vfield.mask.flatten())
    reg_filter = morphology.remove_small_objects(~vfield.mask, min_size = ms)
    return reg_filter

# ---------------------------------------------------------------------------------------
# func: load_vfields 
#
# Given a maps file this returns the stellar and halpha velocity fields and coordinates.
# X (Y) coordinates accessed by grid[0] (1).

def load_vfields(hdu):
    emlc = channel_dictionary(hdu, 'EMLINE_GVEL')
    grid = hdu['SPX_SKYCOO'].data
    smask_ext = hdu['STELLAR_VEL'].header['QUALDATA']
    stellar_vfield = np.ma.MaskedArray(hdu['STELLAR_VEL'].data, mask=hdu[smask_ext].data > 0)
    gmask_ext = hdu['EMLINE_GVEL'].header['QUALDATA']
    halpha_vfield = np.ma.MaskedArray(hdu['EMLINE_GVEL'].data[emlc['Ha-6564'],:,:], mask=hdu[gmask_ext].data[emlc['Ha-6564'],:,:] > 0) 
    return grid, stellar_vfield, halpha_vfield

# ---------------------------------------------------------------------------------------
# func: channel_dictionary
# 
# Taken from TRM example functions. Used to create a dictionary for the columns in the
# multi-channel extensions.

def channel_dictionary(hdu, ext):
    channel_dict = {}
    for k, v in hdu[ext].header.items():
        if k[0] == 'C':
            try:
                i = int(k[1:])-1
            except ValueError:
                continue
            channel_dict[v] = i
    return channel_dict

# ---------------------------------------------------------------------------------------
# func: pa_absolute_offset
#
# Returns the absolute offset between the stellar and gas PAs. (Note: this need to be 
# corrected to run between 0-360. This deals with the periodicity.

def pa_absolute_offset(stelPA, gasPA):
    off_cw = np.abs(stelPA - gasPA)
    off_ccw = 360 - np.abs(stelPA - gasPA)
    pa_offset = np.minimum(off_cw, off_ccw)
    return pa_offset

# ---------------------------------------------------------------------------------------
# func: fudge_kinematic_pa
# 
# Provides a global kinematic position angle between 0 and 360 degs from the positive 
# horizontal (y-)axis. The angle provided is the axis of rotation clockwise of the 
# blue-shifted side of the rotating galaxy. This routine is dependent on Michele 
# Cappellari's routine fit_kinematic_pa which provides the angle of maximum velocity but 
# is indiscriminate in direction. 
# 
# Note: angle returned is the axis of rotation NOT the angle of maximum velocity.

def fudge_kinematic_pa(XX, YY, vel, pa):
    assert XX.size == YY.size == vel.size, 'X, Y and VEL must be same length'
    
    # Flatten arrays
    XX, YY, vel = XX.flatten(), YY.flatten(), vel.flatten()

    # Transforming pa into angle from positive y-axis.
    pa_azi = 360 - pa
    
    # Creating comparison line across velocity map on rotational axis. 
    rot_angs = [0,np.pi] + np.radians(pa_azi-90)
    radius = np.sqrt(np.max((XX)**2+(YY)**2)) # radius of all points from centre. 
    x_s, y_s = radius*np.sin(rot_angs),radius*np.cos(rot_angs)
    m = (y_s[1] - y_s[0])/(x_s[1] - x_s[0])

    # Comparing average velocity above and below dividing line to find axis of rotation.
    # Depending on which quadrant the PA falls in, applying conversion. Finding all pixels
    # in the defined half and applying rotation direction.
    
    if (pa < 45) or (pa > 135):
        y_intrp = y_s[1] + m*(XX - x_s[1])
        half_1 = np.median(vel[YY > y_intrp])
        half_2 = np.median(vel[YY < y_intrp])
        if half_1 == half_2:
            half_1 = np.mean(vel[YY > y_intrp])
            half_2 = np.mean(vel[YY < y_intrp])
            
        if (0 <= pa < 45):
            if half_2 < half_1:
                axis = pa_azi - 90 
            elif half_1 < half_2:
                axis = pa_azi + 90

        elif (135 < pa <= 180):
            if half_2 < half_1:
                axis = pa_azi + 90 
            elif half_1 < half_2:
                axis = pa_azi - 90
    else:
        x_intrp = x_s[1] + 1/m*(YY - y_s[1])
        half_1 = np.median(vel[XX > x_intrp])
        half_2 = np.median(vel[XX < x_intrp])
        if half_1 == half_2:
            half_1 = np.mean(vel[XX > x_intrp])
            half_2 = np.mean(vel[XX < x_intrp])

        if half_2 < half_1:
            axis = pa_azi + 90 
        elif half_1 < half_2:
            axis = pa_azi - 90
    
    # Re-centring so value always between 0 and 360.
    if axis > 360:
        axis = axis - 360

    return axis

# ---------------------------------------------------------------------------------------