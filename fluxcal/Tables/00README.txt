MODS Spectrophotometric Calibration Tables
2014 May 28 [rwp/osu]

This directory contains the flux tables for the MODS primary 
spectrophotometric standard stars.  The stars were selected
from the HST CALSPEC database, and have good spectrophotometry
from the UV through near-IR.  

All files are in ASCII 3-column format

   Wavelength ABmag  Band

where:
   Wavelength is in Angstroms
   ABmag is the average AB magnitude; m_AB = -2.5 log(f_nu) - 48.60
   Band is the band width in Angstroms.

This is the same ASCII format used by IRAF (e.g., as in the flux tables
used by the standard command in the NOAO onedspec package).

Flux tables are provided with 10A and 50A sampling from 3200-10500A
ensure good fluxes for grating and prism modes, with sufficient
sampling to capture low-level structure in the instrumental response
(e.g., wiggles in the dichroic transmission, etc.).  The 10A flux
tables were created by John Moustakas for is IDL/iSPEC package and
modified for use with MODS spectra.

All of the flux tables have been edited to censor the strong telluric
absorption features and strong stellar absorption lines that might
cause problems with IRAF sensfunc.

The original flux spectra for the primary standards can be retrieved
from the HST CALSPEC database

  www.stsci.edu/hst/observatory/cdbs/calspec.html

for example, to use the primary standards for generating telluric
corrections.  

Note that the full CALSPEC versions of the primary standard stars
are included as part of the modsIDL spectral reduction pipeline
distribution and do not need to be separately downloaded if using
modsIDL for your spectra (which we strong recommend you do).

Important Note:

As of May 2014, we have removed the four "secondary" standard stars
from previous releases (these are GD140, Hiltner 600, PG0823, and 
Wolf 1346).  We have found on reviewing available MODS spectra and
flux tables that these stars were not good calibrators for MODS.


Approximate LBT Extinction Curve
--------------------------------

The file 

   lbtextinct.dat

is an approximate extinction curve for the LBT site on Mt. Graham.  It
is based on the KPNO and Paranal extinction curves, scaled to the
3220m elevation of LBT assuming an atmospheric scale height of 7km.
This approximate is valid for molecular components of atmospheric
absorption and scattering, but will be less good for components due to
Mie scattering from high-altitude aerosols (e.g., volcanic dust) that
do not scale exponentially.


------------------------------
R. Pogge, OSU Astronomy Dept.
pogge@astronomy.ohio-state.edu
