#!/opt/anaconda/bin/python
#
# sensplist3.py: reads a list of std tables and creates 2 plots:
# 1 sensitivity vs wavelength 
# 2 sensitivity at lam0 vs time
#
# std tables are output by iraf standard and contain a first line like:
# filename i1 i2 exptime airmass w1 w2 starname
#
# Usage: sensplist3.py std.tab lam0 (usu lam0 = 4500.0 blue and 7000.0 red)
#
# Options: 
#	-v print verbose debugging info during execution
#	-V print version info and exit
#
# Description: 
#
# Author: 
#
# O. Kuhn, LBTO (based on the python scripts developed for MODS by R. Pogge)
#   okuhn@lbto.org
#
# Module Dependencies:
#   numpy as np
#   matplotlib.pyplot as pl
#
# Modification History
# 	2016 Aug 19 
# --------------------------------------------------------------------------------------

import os
from os import path
import argparse
import numpy as np
import scipy as sp
from scipy.interpolate import interp1d
import math
import matplotlib.pyplot as pl
from astropy.io import fits

# Version number and date

versNum = "1.0.0"
versDate = "2020-04-03"

Verbose = False  

#----------------------------------------------------------------

def stdplot(stdfile,lam0):
	ret = dict()
	f = open(stdfile,'r')
	fl = f.readline().split() 
	f.close()
	file=fl[0]
	exptime=float(fl[3])
	airmass=float(fl[4])
	star= ('_'.join(fl[7:])).strip('\n')
	
	ht=fits.getheader(fl[0].strip('[').strip(']'))
	dich = str.lower(ht['dichname'])
	inst = str.lower(ht['instrume'])
	mjd = float(ht['mjd-obs'])
	
	if (inst == "mods1r" or inst == "mods2r"):
		if (dich == "dual"):
			s0 = sdualredgrat
		if (dich == "red"):
			s0 = sredgrat
	if (inst == "mods1b" or inst == "mods2b"):
		if (dich == "dual"):
			s0 = sdualbluegrat
		if (dich == "blue"):
			s0 = sbluegrat
			
	sf = np.loadtxt(stdfile,skiprows=1,dtype='float')
	sensno= np.log10(sf[:,3]) - np.log10(sf[:,1]) - np.log10(exptime) -np.log10(sf[:,2]) 
	sens= np.log10(sf[:,3]) - np.log10(sf[:,1]) - np.log10(exptime) -np.log10(sf[:,2]) + 0.4*airmass*iextinct(sf[:,0])

	if lam0 == 0:
		s0l=0.0
		s0lno=0.0
	if lam0 !=0:
		# build table mjd S0_7000_ext S0_7000_raw instrume mode star
		il = [i for i in range(len(sf)) if sf[i,0]==lam0]
		s0l=sens[il]
		s0lno=sensno[il]

	#simply making x-axis buffers 
	buf=.1*(max(sf[:,0])-min(sf[:,0]))
	xlo=min(sf[:,0])-buf
	xhi=max(sf[:,0])+buf


	ax1.axis([xlo,xhi,14.25,16.75])
	#ax1.axis([xlo,xhi,ylo,yhi])
	ax1.plot(sf[:,0],sens,"*")
	ax1.plot(sf[:,0],sensno)
	ax1.plot(s0[:,0],s0[:,1],"r+")
	ax1.plot(s0[:,0],s0[:,1],"y")

	ret['airmass']=airmass
	ret['s0l']=s0l
	ret['s0lno']=s0lno
	ret['mjd']=mjd
	ret['inst']=inst
	ret['dich']=dich
	ret['star']=star

	#return {'s0l':s0l,'s0lno':s0lno,'mjd':mjd,'inst':inst,'dich':dich,'star':star}
	return ret
  
#def get_upper_env(a,niter):
#
	#for i in range(niter):
		#mean = np.mean(na)
		#sdev = np.stddev(na,ddof=1)
		#j = [j in range(len(na)) where a[j,1] > mean-3*sdev]
		#new = na[j]
#
	#return na
#----------------------------------------------------------------
#
# Main Program starts here...
#
#
# Sensitivities for grating (not prism) spectroscopy in dual/blue/red modes
#
sbluegrat = np.array([[3200,15.721],[3500,15.934],[4000,16.226],[4500,16.270],[5000,16.239],[5500,16.167],[5800,16.109],[6000,16.603],[6450,15.940]],float)
sdualbluegrat = np.array([[3200,15.597],[3500,15.865],[4000,16.179],[4500,16.257],[5000,16.237],[5500,16.162],[5800,14.811]],float)
sredgrat = np.array([[5000,15.978],[5500,16.381],[6000,16.465],[6500,16.487],[7000,16.488],[7500,16.456],[8000,16.391],[8500,16.310],[9000,16.229],[9500,15.963],[10000,15.802]],float)
sdualredgrat = np.array([[5500,14.922],[6000,16.453],[6500,16.473],[7000,16.462],[7500,16.433],[8000,16.341],[8500,16.242],[9000,16.151],[9500,15.893],[10000,15.396]],float)

ibluegrat = sp.interpolate.interp1d(sbluegrat[:,0],sbluegrat[:,1],kind='linear')
idualbluegrat = sp.interpolate.interp1d(sdualbluegrat[:,0],sdualbluegrat[:,1],kind='linear')
iredgrat = sp.interpolate.interp1d(sredgrat[:,0],sredgrat[:,1],kind='linear')
idualredgrat = sp.interpolate.interp1d(sdualredgrat[:,0],sdualredgrat[:,1],kind='linear')
#
# Extinction Curve
#
#extinct = np.array([[3200,0.866],[3500,0.511],[4000,0.311],[4500,0.207],[5000,0.153],[5500,0.128],[6000,0.113],[6450,0.088],[6500,0.085],[7000,0.063],[7500,0.053],[8000,0.044],[8210,0.043],[8260,0.042],[8370,0.041],[8708,0.026],[10256,0.020]],float)
# below I made up the point at 10550 (0.02), like ctio curve, flat into near-IR
extinct = np.array([[3200,0.866],[3500,0.511],[4000,0.311],[4500,0.207],[5000,0.153],[5500,0.128],[6000,0.113],[6450,0.088],[6500,0.085],[7000,0.063],[7500,0.053],[8000,0.044],[8210,0.043],[8260,0.042],[8370,0.041],[8708,0.026],[10256,0.020],[10550,0.020]],float)

iextinct = sp.interpolate.interp1d(extinct[:,0],extinct[:,1],kind='linear')

# Runtime flags

# Parse the command-line arguments using argparse

parser = argparse.ArgumentParser(description='MODS Zero Point Trends')
parser.add_argument('stdlist', type=str, help = 'List of tables output by IRAF task, standard')
parser.add_argument('lam0', type=float, help = 'reference wavelength for plotting trends')
parser.add_argument('ylo', type=float, help = 'lower limit for y (15.5 or 16)')
parser.add_argument('yhi', type=float, help = 'lower limit for y (16.5 or 17)')

args = parser.parse_args()
  
stdlist = args.stdlist
lam0 = args.lam0
slam0 = str(lam0)
ylo = args.ylo
yhi = args.yhi

dir = os.path.dirname(stdlist)

if lam0 != 0.0:
	# create output file name from input filename
	outlist = [stdlist,slam0,'out']
	outlistsrt = [stdlist,slam0,'sort']
	outfile = "_".join(outlist)
	outfilesrt = "_".join(outlistsrt)

pngFile1 = stdlist + "_zps.png"
pngFile2 = stdlist + "_trend.png"

fig1,ax1 = pl.subplots()
dpi = 600
fig1.set_dpi(dpi)

fig2,ax2 = pl.subplots()
dpi = 600
fig2.set_dpi(dpi)


# figure 1 begin 
if lam0 != 0:
	m=[]
	am=[]
	i=[]
	d=[]
	s=[]
	sl=[]
	slno=[]
cnt=0


with open(stdlist,'r') as l:
   for line in l:
        if not line.startswith('#'):
           stdfile = line.strip('\n')
        # stdplot adds to figure 1: S0 vs wavelength for all standards in list
        #s0l,s0lno,mjd,inst,dich,star = stdplot(stdfile,lam0)
           t = stdplot(stdfile,lam0)
           if lam0 != 0:
                m.append(t['mjd'])
                am.append(t['airmass'])
                i.append(t['inst'])
                d.append(t['dich'])
                s.append(t['star'])
                sl.append(t['s0l'])
                slno.append(t['s0lno'])
                cnt=cnt+1

ax1.set_title(stdlist)
fig1.savefig(pngFile1)
# figure 1 end

amcolors = {0:'c',1:'b',2:'m',3:'g',4:'y',5:'r',6:'brown'}

if lam0 != 0:
	#create array to hold resulting table
	tf = open(outfile,'w')
	for j in range(cnt):
		tline =  "%f %f %f %.3f %s %s %f %s\n" % (m[j],sl[j],slno[j],am[j],i[j],d[j],lam0,s[j])
		tf.write(tline)
	tf.close()
	# sort the array by MJD
	ta = np.genfromtxt(outfile,dtype=str)
	tsrt=ta[np.argsort(ta[:,0].astype(float))]

	np.savetxt(outfilesrt,tsrt,fmt='%s %s %s %s %s %s %s %s')

	# figure 2 (mjd vs S0_7000) and table output
	# mjd S0_7000 mode star
	# pt colors by airmass

	c0 = [i for i in range(len(tsrt)) if (tsrt[i,3].astype(float)-1.) < 0.1]
	c1 = [i for i in range(len(tsrt)) if (tsrt[i,3].astype(float)-1.) >= 0.1 and (tsrt[i,3].astype(float)-1.) < 0.2] 
	c2 = [i for i in range(len(tsrt)) if (tsrt[i,3].astype(float)-1.) >= 0.2 and (tsrt[i,3].astype(float)-1.) < 0.3] 
	c3 = [i for i in range(len(tsrt)) if (tsrt[i,3].astype(float)-1.) >= 0.3 and (tsrt[i,3].astype(float)-1.) < 0.4] 
	c4 = [i for i in range(len(tsrt)) if (tsrt[i,3].astype(float)-1.) >= 0.4 and (tsrt[i,3].astype(float)-1.) < 0.5] 
	c5 = [i for i in range(len(tsrt)) if (tsrt[i,3].astype(float)-1.) >= 0.5 and (tsrt[i,3].astype(float)-1.) < 0.6] 
	c6 = [i for i in range(len(tsrt)) if (tsrt[i,3].astype(float)-1.) >= 0.6] 

	ax2.axis([np.min(tsrt[:,0]),np.max(tsrt[:,0]),ylo,yhi])
	#ax2.plot(tsrt[:,0].astype(float),tsrt[:,1].astype(float),color=amcolors[cind],marker='.')
	ax2.plot(tsrt[c0,0].astype(float),tsrt[c0,1].astype(float),color=amcolors[0],marker='o',ms="12",ls="")
	ax2.plot(tsrt[c1,0].astype(float),tsrt[c1,1].astype(float),color=amcolors[1],marker='o',ms="12",ls="")
	ax2.plot(tsrt[c2,0].astype(float),tsrt[c2,1].astype(float),color=amcolors[2],marker='o',ms="12",ls="")
	ax2.plot(tsrt[c3,0].astype(float),tsrt[c3,1].astype(float),color=amcolors[3],marker='o',ms="12",ls="")
	ax2.plot(tsrt[c4,0].astype(float),tsrt[c4,1].astype(float),color=amcolors[4],marker='o',ms="12",ls="")
	ax2.plot(tsrt[c5,0].astype(float),tsrt[c5,1].astype(float),color=amcolors[5],marker='o',ms="12",ls="")
	ax2.plot(tsrt[c6,0].astype(float),tsrt[c6,1].astype(float),color=amcolors[6],marker='o',ms="12",ls="")

	ax2.plot(tsrt[:,0].astype(float),tsrt[:,1].astype(float),'k:')

	ax2.set_title(stdlist)
	fig2.savefig(pngFile2)
	

pl.show()

l.close()
