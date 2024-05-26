
modsens.cl - IRAF task to reduced pre-processed 2D data and output a sensitivity function. IRAF.longslit.sensfunc also outputs a log file of wavelength vs extinction-corrected, shifted, composite sensitivity function
which is what is read by get_sens_mod.py and plotted by the efficiency*py and m1_vs_m2*py scripts (also 
the qe.py?).

modsens uses the linelists and standard star flux tables in the linelists and fluxcal directories.

sensplist3.py - takes a list of std*tab files output by IRAF.longslit.standard, calculates the sensitivity
function from each and overplots them all.  

get_sens_mod.py - takes the log file output by modsens.cl and interpolates to get the sensitivities at a set
of fixed wavelengths.

efficiency_comm_vs_may23.py
efficiency_evol.py
m1_vs_m2_eff.py

qe4.py
qe4_v1.py
qe_evol.py
qe_evol_refl9.py

fluxcal:
lbtextinct.dat
std_10and50ang_fluxtables_plot.png
Tables

linelists:
