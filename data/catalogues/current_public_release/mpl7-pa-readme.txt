---------------------------------------------------------------------------------------
mpl7-pa-classifications
Chris Duckworth. cd201@st-andrews.ac.uk

17-4-19. v0.1 - still in vetting. if bugs or mis-classifications found please email

Disclaimer:
- The photometry field has not been eyeballed for all of the galaxies in the sample. Therefore the merger category is not a complete sample. The ones presented are those simply very obvious in the kinematics and then followed-up in photometry.
---------------------------------------------------------------------------------------

Global position angles for stellar and h-alpha fields for all MaNGA galaxies in MPL-8.
Complete kinematic classifications and usability flags for all PA fits and PA offset
between stellar and h-alpha rotation.

---------------------------------------------------------------------------------------

If you use this catalogue for science I would really appreciate it if you cite:
Duckworth et al. (The decoupling of star-gas co-rotation - I: the fundamental links to morphology and halo spin). 

(Paper will be up on arXiv ~ 20 October 2019)

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

pa_offset: numeric (0-180)
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

Additional column descriptions.
All other columns are taken from the drpall metadata file. The columns are descrived here:
(Note: order not preserved)

1) PLATE: The plateid
2) IFUDSGN: The ifu design id (e.g., 12701)
3) PLATEIFU: The plate+ifudesign name for this object (e.g., 7443-12703).
4) MANGAID: The mangaid for this object (e.g., 1-114145)
5) VERSDRP2: Version of DRP used for 2d reductions
6) VERSDRP3: Version of DRP used for 3d reductions
7) VERSCORE: Version of mangacore used for reductions
8) VERSUTIL: Version of idlutils used for reductions
9) VERSPRIM: Version of mangapreim used for reductions
10) PLATETYP: Plate type (MANGA, APOGEE-2&MANGA)
11) SRVYMODE: Survey mode (MANGA dither, MANGA stare, APOGEE lead)
12) OBJRA: Right ascension of the science object in J2000
13) OBJDEC: Declination of the science object in J2000
14) IFUGLON: Galactic longitude corresponding to IFURA/DEC
15) IFUGLAT: Galactic longitude corresponding to IFURA/DEC
16) IFURA: Right ascension of this IFU in J2000
17) IFUDEC: Declination of this IFU in J2000
18) EBVGAL: E(B-V) value from sdss dust routine for this IFUGLON, IFUGLAT
19) NEXP: Number of science exposures combined
20) EXPTIME: Total exposure time (seconds)
21) DRP3QUAL: Quality bitmask
22) BLUESN2: Total blue SN2 across all nexp exposures
23) REDSN2: Total red SN2 across all nexp exposures
24) HARNAME: IFU harness
25) FRLPLUG: frlplug hardware code
26) CARTID: Cartridge ID number
27) DESIGNID: Design ID number
28) CENRA: Plate center right ascension in J2000
29) CENDEC: Plate center declination in J2000
30) AIRMSMIN: Minimum airmass across all exposures
31) AIRMSMED: Median airmass across all exposures
32) AIRMSMAX: Maximum airmass across all exposures
33) SEEMIN: Best guider seeing
34) SEEMED: Median guider seeing
35) SEEMAX: Worse guider seeing
36) TRANSMIN: Worst transparency
37) TRANSMED: Median transparency
38) TRANSMAX: Best transparency
39) MJDMIN: Minimum MJD across all exposures
40) MJDMED: Median MJD across all exposures
41) MJDMAX: Maximum MJD across all exposures
42) GFWHM: Reconstructed FWHM in g-band (arcsec)
43) RFWHM: Reconstructed FWHM in r-band (arcsec)
44) IFWHM: Reconstructed FWHM in i-band (arcsec)
45) ZFWHM: Reconstructed FWHM in z-band (arcsec)
46) MNGTARG1: manga_target1 maskbit for galaxy target catalog
47) MNGTARG2: manga_target2 maskbit for non-galaxy target catalog
48) MNGTARG3: manga_target3 maskbit for ancillary target catalog
49) CATIDNUM: Primary target input catalog (leading digits of mangaid: see https://trac.sdss.org/browser/repo/manga/mangacore/trunk/platedesign/catalog_ids.dat)
50) PLTTARG: plateTarget reference file appropriate for this target
These next entries are taken from the relevant plateTargets file
51) manga_tileid: Tiling ID
52) nsa_iauname: The accepted IAU name
53) ifudesignsize: The size of the IFU assigned to the target.
54) ifutargetsize: The size of the IFU that was meant to be assigned. Same as ifudesignsize unless changed during the plate design process.
55) ifudesignwrongsize: 1 if the IFU assigned is of the wrong size (for instance, if it does not cover 1.5Reff).
56) z: The targeting redshift (identical to nsa_z for those targets in the NSA Catalog. For others, it is the redshift provided by the Ancillary programs)
57) zmin: Primary sample lower redshift limit
58) zmax: Primary sample upper redshift limit
59) szmin: Secondary sample lower redshift limit
60) szmax: Secondary sample upper redshift limit
61) ezmin: Primary+ sample lower redshift limit
62) ezmax: Primary+ sample upper redshift limit
63) probs: The probability that a Secondary sample galaxy is included after down-sampling. For galaxies not in the Secondary sample PROBS is set to the mean down-sampling probability
64) pweight: The volume weight for the Primary sample. Corrects the MaNGA selection to a volume limited sample.
65) psweight: The volume weight for the combined Primary and full Secondary samples. Corrects the MaNGA selection to a volume limited sample.
66) psrweight: The volume weight for the combined Primary and down-sampled Secondary samples. Corrects the MaNGA selection to a volume limited sample.
67) sweight: The volume weight for the full Secondary sample. Corrects the MaNGA selection to a volume limited sample.
68) srweight: The volume weight for the down-sampled Secondary sample. Corrects the MaNGA selection to a volume limited sample.
69) eweight: The volume weight for the Primary+ sample. Corrects the MaNGA selection to a volume limited sample.
70) esweight: The volume weight for the combined Primary+ and full Secondary samples. Corrects the MaNGA selection to a volume limited sample.
71) esrweight: The volume weight for the combined Primary+ and down-sampled Secondary samples. Corrects the MaNGA selection to a volume limited sample.
72) nsa_field: The SDSS field covering the target.
73) nsa_run: The SDSS run covering the target.
74) nsa_camcol: The SDSS camcol covering catalog position.
75) nsa_version: The version of the NSA catalogue used to select these targets.
76) nsa_nsaid: The NSAID field in the NSA catalogue v1.
77) nsa_nsaid_v1b: The NSAID of the target in the NSA_v1b_0_0_v2 catalogue (if applicable).
78) nsa_z: Heliocentric redshift.
79) nsa_zdist: Distance estimate using pecular velocity model of Willick et al. (1997); multiply by c/H0 for Mpc.
80) nsa_sersic_absmag[7]: Absolute magnitude estimates for FNugriz from K-corrections (Ωm=0.3, ΩΛ=0.7, h=1)
81) nsa_elpetro_absmag[7]: As nsa_sersic_absmag but from elliptical Petrosian apertures.
82) nsa_elpetro_amivar[7]
83) nsa_sersic_mass: Stellar mass from K-correction fit in h-2 solar masses to sersic magnitudes.
84) nsa_elpetro_mass[7] Stellar mass from K-correction fit in h-2 solar masses to elliptical petrosian magnitudes.
85) nsa_elpetro_ba Axis ratio b/a from elliptical petrosian fit.
86) nsa_elpetro_phi Angle (E of N, degrees) of major axis in elliptical petrosian fit
87) nsa_extinction[7]
88) nsa_elpetro_th50_r: Elliptical petrosian 50% light radius (derived from r band), in arcsec.
89) nsa_petro_th50: Petrosian 50% light radius (derived from r band), in arcsec
90) nsa_petro_flux[7]: Azimuthally-averaged SDSS-style Petrosian flux in FNugriz (GALEX-SDSS photometric systems). In nanomaggies.
91) nsa_petro_flux_ivar[7]: Inverse variance of petroflux in nanomaggies-2.
92) nsa_elpetro_flux[7]: Azimuthally-averaged SDSS-style Petrosian flux in FNugriz (GALEX-SDSS photometric systems). In nanomaggies.
93) nsa_elpetro_flux_ivar[7]: Inverse variance of petroflux in nanomaggies-2.
94) nsa_sersic_ba: Axis ratio b/a from 2D Sersic fit.
95) nsa_sersic_n: 2D Sersic index from fit.
96) nsa_sersic_phi: Angle (E of N, degrees) of major axis in 2D Sersic fit.
97) nsa_sersic_th50: 50% light radius (r-band) of 2D Sersic fit (along major axis), in arcsec.
98) nsa_sersic_flux[7]: 2D Sersic fit flux in FNugriz (GALEX-SDSS photometric systems) in nanommagies.
99) nsa_sersic_flux_ivar[7]: Inverse variance of sersicflux in nanomaggies-2.
