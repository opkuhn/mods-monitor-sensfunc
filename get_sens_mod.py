#!/opt/anaconda/bin/python

import numpy as np
import matplotlib.pyplot as pl

import argparse
import scipy as sp
from scipy.interpolate import interp1d
import math
import matplotlib.pyplot as pl

parser = argparse.ArgumentParser(description='MODS Zero Points')
parser.add_argument('inlist', type=str, help = 'Output of sensfunc')
parser.add_argument('channel', type=str, help = 'b or r')
parser.add_argument('nskip', type=int, help = 'number of lines of log file to skip')
args = parser.parse_args()
  
infile = args.inlist
chan = args.channel
nskip = args.nskip

extinct = np.array([[3200,0.866],[3500,0.511],[4000,0.311],[4500,0.207],[5000,0.153],[5500,0.128],[6000,0.113],[6450,0.088],[6500,0.085],[7000,0.063],[7500,0.053],[8000,0.044],[8210,0.043],[8260,0.042],[8370,0.041],[8708,0.026],[10256,0.020],[10550,0.020]],float)

iextinct = sp.interpolate.interp1d(extinct[:,0],extinct[:,1],kind='linear')

r1=2.5
b1=2.1
r2=1.7
b2=2.0

sens = np.genfromtxt(infile,skip_header=nskip)

sw = np.zeros(len(sens))
sf  = np.zeros_like(sw) 

for i in range(len(sens)):
   if nskip > 0:
      sw[i] = sens[i,0]
      #sf[i] = sens[i,2] + iextinct(sens[i,0])   ---- to check on the effect of assuming output of sensfunc is sensitivity at airmass=1 (it is not)
      sf[i] = sens[i,2]
   elif nskip == 0:
      sw[i] = sens[i,0]
      #sf[i] = sens[i,1] + iextinct(sens[i,0])  ---- to check on the effect of assuming output of sensfunc is sensitivity at airmass=1 (it is not)
      sf[i] = sens[i,1]

isens = sp.interpolate.interp1d(sw,0.4*sf, kind='linear')
#isens = sp.interpolate.interp1d(sens[:,0],0.4*sens[:,2], kind='linear')

#pl.plot(sens[:,0],0.4*sens[:,2],color='k')
#pl.plot(sens[:,0],0.4*sens[:,2],color='red', marker='*', linestyle="")

#pl.axis([3000,11000,14,17])
#pl.xlabel("Wavelength[A]")
#pl.ylabel("Sensitivity")

if str.lower(chan) == "r":
   lam = [5000,5500,5650,6000,6500,7000,7500,8000,8500,9000,9500,10000]
if str.lower(chan) == "b":
   lam = [3200.00,3500,4000,4500,5000,5500,5800,6000,6450]

outfile = infile + ".out"

F = open(outfile,"w")

for wav in lam:
   print ("%f %.3f" % (wav,isens(wav)))
   line = ("%f %.3f\n" % (wav,isens(wav)))
   F.write(line)

F.close()
