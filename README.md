# mods-monitor-sensfunc
Scripts to monitor the MODS spectroscopic zeropoints


modsens.cl -- an IRAF task that takes as input a list of preprocessed 2D
spectra of spectrophotometric standards and blue/red wavelength solutions 
and, for each, outputs: 
(1) a log file which contains the composite, extinction-corrected
sensitivity as a function of wavelength (this file is to be used in preference to the
fitted sensitivity function, sf*fits, since there are too many gaps and wiggles to 
permit a good automatic fit); and
(2) a table of observed counts within each of the wavelength bins of the standard
star tabulated flux.

The tabulated flux tables and line lists are included here.

fluxcal:
linelists:
lbtextinct.dat

The procedure is documented here ().


The python scripts plot the output:

sensplist3.py takes the list of std*tab files containing the observed counts in each wavelength
bin and overplots all of these. 

get_sens_mod.py takes the log file and outputs the zeropoints at a discrete set of wavelengths.

m1_vs_m2_eff.py - compares the MODS1 vs MODS2 efficiencies.

Efficiency:
efficiency_comm_vs_may23.py
efficiency_evol.py
qe4.py
qe4_v1.py
qe_evol.py
qe_evol_refl9.py
