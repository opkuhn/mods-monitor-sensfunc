#!/opt/anaconda/bin/python
#
# qe  
# 
#  Takes as input the sensitivity function (lambda, sens) and instrument
# and telescope parameters: gain, collecting area, reflectivity.
#  
#  Outputs QE of instrument+telescope as a function of lambda
#
# Usage: qe sensfunc instrument 
# 
# Where:
#   sensfun = sensitivity function: lambda(angstroms) sensfunc(log10(x))
#   instrument = m1r, m1b, m2r or m2b 
# 
# Options:
#   -v      print verbose debugging info during execution
#   -V      print version info and exit

# Example: qe sensx_red.list m2r
#
# Description:
#
# Author:
#   O. Kuhn, LBTO (based on the python scripts developed for MODS by R. Pogge)
#   okuhn@lbto.org
#
# Module Dependencies:
#   numpy as np
#   matplotlib.pyplot as pl
#
# Modification History
#   2019 Mar 5 
#   2022 Nov 3 --- updated I/O, including making it run on log output of sensfunc 
#                  which has wavelength & avg sensfunc in columns 0 & 2, respectively.
#              --- nkskip is in the number of lines to skip before the data. If nskip=0,
#                  assume a table with wavelength & sensfunc in columns 0 & 1
#
#-----------------------------------------------------------------------------
#
import os 
from sys import argv, exit
import getopt
import numpy as np 
import matplotlib.pyplot as pl
import scipy as sp
from scipy.interpolate import interp1d

import argparse

# Version number and date

versNum = "0.0.0"
#versDate = "2019-04-05"
versDate = "2022-11-03"

# Global Defaults

# Runtime flags

Verbose = False      # Verbose debugging output on/off

#----------------------------------------------------------------
#
# Main Program starts here...
#

# Interpolate over "LBT Model Extinction Curve"
# The output of sensfunc is already for airmass=0; the curve is included 
# here for testing purposes (what effect does it have)?

extinct = np.array([[3200,0.866],[3500,0.511],[4000,0.311],[4500,0.207],[5000,0.153],[5500,0.128],[6000,0.113],[6450,0.088],[6500,0.085],[7000,0.063],[7500,0.053],[8000,0.044],[8210,0.043],[8260,0.042],[8370,0.041],[8708,0.026],[10256,0.020],[10550,0.020]],float)

iextinct = sp.interpolate.interp1d(extinct[:,0],extinct[:,1],kind='linear')


# Inputs are: 
# (1) the output of sensfunc (I set sensfunc.log = "mods??_mode.log" 
#   to write out a table of wavelength vs average sensitivity. This allows 
#   interpolation through the datapoints and avoids the limitations and 
#   problems with fitting a polynomial or even cubic spline through the gaps, 
#   dichroic wiggles and at the end points."
# (2,3 and 5) are purely for plotting purposes
# (2) channel: is this for mods1/mods2 red/blue?
# (3) mode:    dual or direct mode?
# (4) nskip:   number of lines to skip before data in input file.
# (5) plot color 
#
#
# Output is a table of wavelength vs efficiency 
# (efficiency with telescope but outside of atmosphere, i.e. @ airmass=0)
# Note that the output of sensfunc is already for airmass=0

parser = argparse.ArgumentParser(description = 'get QE from sensitivity function')

parser.add_argument('sensfunc', type=str, help = 'input file containing sensitivity function')
parser.add_argument('instrument', type=str, help = 'instrument, as one of "m1r","m1b","m2r","m2b"')
parser.add_argument('mode', type=str, help = '"dual" or "direct"')
parser.add_argument('nskip', type=int, help = 'number of lines to skip before data')
parser.add_argument('plotcol', type=str, help = 'plot color')

args = parser.parse_args()

inFile = args.sensfunc 
instrument  = args.instrument
mode = args.mode
nskip = args.nskip
pc = args.plotcol

outFile = str.split(inFile,".")[0] + "_qe_tel0.out"

gain_m1b = 2.1 
gain_m1r = 2.5 
gain_m2b = 2.0 
gain_m2r = 1.7 

d1 = 8.2 #w adsec
dobs = 0.889
#dobs = 0.0
#refl = 0.9
refl = 1
nmirr = 2

h = 6.626e-27
c = 2.9979e18

# Verify files exist, abort if input file not found.

if not os.path.isfile(inFile):
  print ("** ERROR: Input sensitivity function %s not found" % (inFile))
  print ("          qe aborting.")
  exit(1)

if Verbose:
  print ("reading %s..." % (inFile))
sf = np.genfromtxt(inFile,skip_header=nskip) 

l = sf[:,0]

#kext = iextinct(l)

if nskip > 0:
   s = sf[:,2]
   #s = sf[:,2] + kext
elif nskip == 0:
   s = sf[:,1]
   #s = sf[:,1] + kext

# gain 
if instrument == "m1r":
 	gain = gain_m1r
if instrument == "m1b":
 	gain = gain_m1b
if instrument == "m2r":
 	gain = gain_m2r
if instrument == "m2b":
 	gain = gain_m2b

area = np.pi*1.e4*(d1**2 - dobs**2)/4.
aeff = area*(refl**nmirr)
k = h * c * gain / (l * aeff) 

if np.max(s)>30:
	qe =  k * 10**(0.4*s) 
	flag = 1
if np.max(s)<30:
	qe =  k * 10**(s) 
	flag = 0

#
ltab = np.zeros((len(sf),2)) 
ltab[:,0] = l
ltab[:,1] = qe
#
#
if flag:
	if instrument[0:3] == "m1r": 
                if mode == "dual":
                   ri = [i for i in range(len(l)) if l[i]>5500.]
                   pl.plot(l[ri],qe[ri],color=pc,linestyle="dotted") 
                elif mode == "direct":
                   pl.plot(l,qe,color=pc,linestyle="solid") 
	elif instrument[0:3] == "m2r": 
                if mode == "dual":
                   ri = [i for i in range(len(l)) if l[i]>5500.]
                   pl.plot(l[ri],qe[ri],color=pc,linestyle="dotted") 
                elif mode == "direct":
                   pl.plot(l,qe,color=pc,linestyle="solid") 
	if instrument[0:3] == "m1b": 
                if mode == "dual":
                   bi = [i for i in range(len(l)) if l[i]<5800.]
                   pl.plot(l[bi],qe[bi],color=pc,linestyle="dotted") 
                elif mode == "direct":
                   pl.plot(l,qe,color=pc,linestyle="solid") 
	elif instrument[0:3] == "m2b": 
                if mode == "dual":
                   bi = [i for i in range(len(l)) if l[i]<5800.]
                   pl.plot(l[bi],qe[bi],color=pc,linestyle="dotted") 
                elif mode == "direct":
                   pl.plot(l,qe,color=pc,linestyle="solid") 
if not flag:
	if instrument[0:2] == "m1": 
		pl.plot(l, qe, "x") 
		pl.plot(l, qe,"c:") 
	elif instrument[0:2] == "m2": 
		pl.plot(l, qe, "x") 
		pl.plot(l, qe, "b:") 
#
np.savetxt(outFile,ltab,fmt='%.4f %.4e')
#
if Verbose:
  print ("qe Done, exit plot window to return to prompt")
#
pl.show()

