---------------------------------------------------------------------------------------
mpl8-pa-classifications
Chris Duckworth. cd201@st-andrews.ac.uk

17-4-19. v0.1 - still in vetting. if bugs or mis-classifications found please email

Disclaimer:
- The field has not been eyeballed for all of the galaxies in the sample. Therefore the
merger category is not a complete sample. The ones presented are those simply very obvious 
in the kinematics and then followed-up in photometry. 
---------------------------------------------------------------------------------------

Global position angles for stellar and h-alpha fields for all MaNGA galaxies in MPL-8.
Complete kinematic classifications and usability flags for all PA fits and PA offset
between stellar and h-alpha rotation.
---------------------------------------------------------------------------------------

Columns:

plateifu: str
unique observation identifier. note repeat observations are not removed here.

stellar_pa: numeric (0-360)
kinematic position angle of the stellar velocity field (angle along which velocity change is greatest). 
Defined by the angle to the redshifted side clockwise from the north axis.

halpha_pa: numeric (0-360)
kinematic position angle of the halpha velocity field (angle along which velocity change is greatest). 
Defined by the angle to the redshifted side clockwise from the north axis.

pa_offset: numeric (0-360)
difference in position angle between stellar_pa and halpha_pa.

stel_qual: int
stellar velocity field quality flag. 
0 - Do not use
1 - Messy (potentially usable but maps are typically messy and global PAs will have higher errors)
2 - Clean (global PAs are well behaved and well defined)

stel_feature: int
classification of kinematic features in the stellar velocity field. 
0 - None 
1 - Kinematically decoupled core.
2 - Warp (velocity field of central region is warped with respect to outskirts)
3 - Merger (ongoing merger or neighbour within IFU, majority are marked with do not use)

halpha_qual: int
halpha velocity field quality flag.
0 - Do not use
1 - Messy (potentially usable but maps are typically messy and global PAs will have higher errors)
2 - Clean (global PAs are well behaved and well defined)

halpha_feature: int
classification of kinematic features in the halpha velocity field. 
0 - None 
1 - Kinematically decoupled core.
2 - Warp (velocity field of central region is warped with respect to outskirts)
3 - Merger (ongoing merger or neighbour within IFU, majority are marked with do not use)

halpha_notes: int
additional classification of stellar velocity field in the instance of usable stellar field
(stel_qual == 1 or 2) and unusable halpha velocity field (halpha_qual == 0)
0 - None
1 - Depletion (clear instance of gas depletion, usually central)
2 - No clear rotation (map has no clear rotation or is noise dominated. note there is a clear 
overlap in classifications between this and depletion, so use with caution for pop. analysis.)
3 - Rotation but biased (part of the map has clear rotation, however is biased by gas either 
accreted in different direction or dispersion dominated)

---------------------------------------------------------------------------------------

IMPORTANT:
1) Missing velocity fields will have missing values for kinematic PAs and be set to -99 for 
the flags.

2) Kinematically misaligned galaxies are far more likely to appear with messy velocity 
than well behaved ones. This is a natural result of their creation (from mergers/accretion).
To select a population for misalignment population statistics, it is most likely best to use
the messy and clean together.

---------------------------------------------------------------------------------------

Usage examples:

I want to define a clean sample of stellar position angles.
-> (stel_qual == 2) & (stel_feature == 0)

I want as many galaxies as possible to define PA offsets for.
-> (stel_qual == 1 or 2) & (halpha == 1 or 2) & (stel_feature == 0) & (halpha_feature == 0)

I want a sample of KDCs. (defined in either stellar or halpha vel fields) 
-> (stel_feature == 1) or (halpha_feature == 1)

I want to find all of the galaxies with a rotating stellar component but with depleted gas.
-> (stel_qual == 1 or 2) & (halpha_notes == 1) 

---------------------------------------------------------------------------------------