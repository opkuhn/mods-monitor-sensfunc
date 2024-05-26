#!/opt/anaconda/bin/python 

import numpy as np
import matplotlib.pyplot as pl

m23_m1bb  = np.genfromtxt("2022/2023_M2Rigid/m1b_blue0526_qe_tel0.out")
m23_m1bd = np.genfromtxt("2022/2023_M2Rigid/m1b_dual0526_qe_tel0.out")
m23_m1rd = np.genfromtxt("2022/2023_M2Rigid/m1r_dual0526_qe_tel0.out")
m23_m1rr = np.genfromtxt("2022/2023_M2Rigid/m1r_red0526_qe_tel0.out")
m23_m2bb = np.genfromtxt("2022/2023_M2Rigid/m2b_blue0526_qe_tel0.out")
m23_m2bd = np.genfromtxt("2022/2023_M2Rigid/m2b_dual0526_qe_tel0.out")
m23_m2rd = np.genfromtxt("2022/2023_M2Rigid/m2r_dual0526_qe_tel0.out")
m23_m2rr = np.genfromtxt("2022/2023_M2Rigid/m2r_red0526_qe_tel0.out")

s22_m1bb = np.genfromtxt("2022/2022Sep/log_blue_m1b_sep22_qe_tel0.out")
s22_m1bd = np.genfromtxt("2022/2022Sep/log_dual_m1b_sep22_qe_tel0.out")
s22_m1rd = np.genfromtxt("2022/2022Sep/log_dual_m1r_sep22_qe_tel0.out")
s22_m1rr = np.genfromtxt("2022/2022Sep/log_red_m1r_sep22_qe_tel0.out")
s22_m2bb = np.genfromtxt("2022/2022Sep/log_blue_m2b_sep22_qe_tel0.out")
s22_m2bd = np.genfromtxt("2022/2022Sep/log_dual_m2b_sep22_qe_tel0.out")
s22_m2rd = np.genfromtxt("2022/2022Sep/log_dual_m2r_sep22_qe_tel0.out")
s22_m2rr = np.genfromtxt("2022/2022Sep/log_red_m2r_sep22_qe_tel0.out")

f23_m1bb = np.genfromtxt("2022/2023_Feb/sens_m1b_blue_qe_tel0.out")
f23_m1bd = np.genfromtxt("2022/2023_Feb/sens_m1b_dual_qe_tel0.out")
f23_m1rd = np.genfromtxt("2022/2023_Feb/sens_m1r_dual_qe_tel0.out")
f23_m1rr = np.genfromtxt("2022/2023_Feb/sens_m1r_red_qe_tel0.out")
f23_m2bb = np.genfromtxt("2022/2023_Feb/sens_m2b_blue_qe_tel0.out")
f23_m2bd = np.genfromtxt("2022/2023_Feb/sens_m2b_dual_qe_tel0.out")
f23_m2rd = np.genfromtxt("2022/2023_Feb/sens_m2r_dual_qe_tel0.out")
f23_m2rr = np.genfromtxt("2022/2023_Feb/sens_m2r_red_qe_tel0.out")

c_m1bd = np.genfromtxt("2011/sensx_m1_bdual_qe_tel0.out")
c_m1bb = np.genfromtxt("2011/sensx_m1_blue_qe_tel0.out")
c_m1rd = np.genfromtxt("2011/sensx_m1_rdual_qe_tel0.out")
c_m1rr = np.genfromtxt("2011/sensx_m1_red_qe_tel0.out")

c_m2bd = np.genfromtxt("2015MODS2/sensx_m2_bdual_qe_tel0.out")
c_m2bb = np.genfromtxt("2015MODS2/sensx_m2_blueonly_qe_tel0.out")
c_m2rd = np.genfromtxt("2015MODS2/sensx_m2_rdual_qe_tel0.out")
c_m2rr = np.genfromtxt("2015MODS2/sensx_m2_redonly_qe_tel0.out")

fig,ax = pl.subplots(2,2)

ax0 = ax[0,0]
ax1 = ax[0,1]
ax2 = ax[1,0]
ax3 = ax[1,1]

plotHeight = 3000 # plot width and height in pixels
plotWidth = 4000
hDisp = plotHeight
wDisp = plotWidth
dpi = 300 # dpi = 300 gives finer resolution and nicer plots.
fig.set_dpi(dpi)
wInches = float(wDisp)/float(dpi)
hInches = float(hDisp)/float(dpi)
fig.set_size_inches(wInches,hInches,forward=True)



ax0.plot(c_m1bb[:,0],c_m1bb[:,1],color="blue",linestyle="solid",lw=3,label="MODS1B direct Comm")
ax0.plot(c_m1rr[:,0],c_m1rr[:,1],color="red",linestyle="solid",lw=3,label="MODS1R direct Comm")
ax0.plot(c_m1bd[:,0],c_m1bd[:,1],color="blue",linestyle=":",lw=3,label="MODS1B dual Comm")
ax0.plot(c_m1rd[:,0],c_m1rd[:,1],color="red",linestyle=":",lw=3,label="MODS1R dual Comm")
ax0.plot(c_m2bb[:,0],c_m2bb[:,1],color="lightblue",linestyle="solid",lw=3,label="MODS2B direct Comm")
ax0.plot(c_m2rr[:,0],c_m2rr[:,1],color="lightcoral",linestyle="solid",lw=3,label="MODS2R direct Comm")
ax0.plot(c_m2bd[:,0],c_m2bd[:,1],color="lightblue",linestyle="-.",lw=3,label="MODS2B dual Comm")
ax0.plot(c_m2rd[:,0],c_m2rd[:,1],color="lightcoral",linestyle="-.",lw=3,label="MODS2R dual Comm")

ax1.plot(s22_m1bb[:,0],s22_m1bb[:,1],color="blue",linestyle="solid",lw=3,label="MODS1B direct 09/22")
ax1.plot(s22_m1rr[:,0],s22_m1rr[:,1],color="red",linestyle="solid",lw=3,label="MODS1R direct 09/22")
ax1.plot(s22_m1bd[:,0],s22_m1bd[:,1],color="blue",linestyle=":",lw=3,label="MODS1B dual 09/22")
ax1.plot(s22_m1rd[:,0],s22_m1rd[:,1],color="red",linestyle=":",lw=3,label="MODS1R dual 09/22")
ax1.plot(s22_m2bb[:,0],s22_m2bb[:,1],color="lightblue",linestyle="solid",lw=3,label="MODS2B direct 09/22")
ax1.plot(s22_m2rr[:,0],s22_m2rr[:,1],color="lightcoral",linestyle="solid",lw=3,label="MODS2R direct 09/22")
ax1.plot(s22_m2bd[:,0],s22_m2bd[:,1],color="lightblue",linestyle="-.",lw=3,label="MODS2B dual 09/22")
ax1.plot(s22_m2rd[:,0],s22_m2rd[:,1],color="lightcoral",linestyle="-.",lw=3,label="MODS2R dual 09/22")

ax2.plot(f23_m1bb[:,0],f23_m1bb[:,1],color="blue",linestyle="solid",lw=3,label="MODS1B direct 02/23")
ax2.plot(f23_m1rr[:,0],f23_m1rr[:,1],color="red",linestyle="solid",lw=3,label="MODS1R direct 02/23")
ax2.plot(f23_m1bd[:,0],f23_m1bd[:,1],color="blue",linestyle=":",lw=3,label="MODS1B dual 02/23")
ax2.plot(f23_m1rd[:,0],f23_m1rd[:,1],color="red",linestyle=":",lw=3,label="MODS1R dual 02/23")
ax2.plot(f23_m2bb[:,0],f23_m2bb[:,1],color="lightblue",linestyle="solid",lw=3,label="MODS2B direct 02/23")
ax2.plot(f23_m2rr[:,0],f23_m2rr[:,1],color="lightcoral",linestyle="solid",lw=3,label="MODS2R direct 02/23")
ax2.plot(f23_m2bd[:,0],f23_m2bd[:,1],color="lightblue",linestyle="-.",lw=3,label="MODS2B dual 02/23")
ax2.plot(f23_m2rd[:,0],f23_m2rd[:,1],color="lightcoral",linestyle="-.",lw=3,label="MODS2R dual 02/23")

ax3.plot(m23_m1bb[:,0],m23_m1bb[:,1],color="blue",linestyle="solid",lw=3,label="MODS1B direct 05/23")
ax3.plot(m23_m1rr[:,0],m23_m1rr[:,1],color="red",linestyle="solid",lw=3,label="MODS1R direct 05/23")
ax3.plot(m23_m1bd[:,0],m23_m1bd[:,1],color="blue",linestyle=":",lw=3,label="MODS1B dual 05/23")
ax3.plot(m23_m1rd[:,0],m23_m1rd[:,1],color="red",linestyle=":",lw=3,label="MODS1R dual 05/23")
ax3.plot(m23_m2bb[:,0],m23_m2bb[:,1],color="lightblue",linestyle="solid",lw=3,label="MODS2B direct 05/23")
ax3.plot(m23_m2rr[:,0],m23_m2rr[:,1],color="lightcoral",linestyle="solid",lw=3,label="MODS2R direct 05/23")
ax3.plot(m23_m2bd[:,0],m23_m2bd[:,1],color="lightblue",linestyle="-.",lw=3,label="MODS2B dual 05/23")
ax3.plot(m23_m2rd[:,0],m23_m2rd[:,1],color="lightcoral",linestyle="-.",lw=3,label="MODS2R dual 05/23")

ax0.set_xlim(left=3200,right=10000)
ax0.set_ylim(bottom=0,top=0.4)
ax1.set_xlim(left=3200,right=10000)
ax1.set_ylim(bottom=0,top=0.4)
ax2.set_xlim(left=3200,right=10000)
ax2.set_ylim(bottom=0,top=0.4)
ax3.set_xlim(left=3200,right=10000)
ax3.set_ylim(bottom=0,top=0.4)
ax0.grid()
ax1.grid()
ax2.grid()
ax3.grid()
ax0.legend(fontsize='small')
ax1.legend(fontsize='small')
ax2.legend(fontsize='small')
ax3.legend(fontsize='small')

ax2.set_xlabel ("Wavelength [angstroms]",fontsize=12)
ax3.set_xlabel ("Wavelength [angstroms]",fontsize=12)
ax2.set_ylabel("MODS+telescope efficiency",fontsize=12)
ax0.set_ylabel("MODS+telescope efficiency",fontsize=12)

pl.gcf().set_size_inches(wInches,hInches)
pl.savefig("efficiency_evol.png",dpi=100)

pl.show()
