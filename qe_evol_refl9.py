import numpy as np
import matplotlib.pyplot as pl


#From commissioning of M1 (2011) an M2 (2015). I have put these
#all in the M2 comm directory.

m1_bdual = np.genfromtxt("2011/sensx_m1_bdual_qe.out")
m1_blue = np.genfromtxt("2011/sens_m1_blueonly_qe.out")
m1_rdual = np.genfromtxt("2011/sens_m1_rdual_qe.out")
m1_red = np.genfromtxt("2011/sens_m1_redonly_qe.out")
m2_bdual = np.genfromtxt("2015MODS2/sensx_m2_bdual_qe.out")
m2_blue = np.genfromtxt("2015MODS2/sensx_m2_blueonly_qe.out")
m2_rdual = np.genfromtxt("2015MODS2/sensx_m2_rdual_qe.out")
m2_red = np.genfromtxt("2015MODS2/sensx_m2_redonly_qe.out")

#Now - Sep2022. M2red has increased from what it was at comm. 
# M1 has fallen dramatically.
m1_bdual_sep22 = np.genfromtxt("2022/2022Sep/log_dual_m1b_sep22_qe.out")
m1_rdual_sep22 = np.genfromtxt("2022/2022Sep/log_dual_m1r_sep22_qe.out")
m2_rdual_sep22 = np.genfromtxt("2022/2022Sep/log_dual_m2r_sep22_qe.out")
m2_bdual_sep22 = np.genfromtxt("2022/2022Sep/log_dual_m2b_sep22_qe.out")
m2_blue_sep22 = np.genfromtxt("2022/2022Sep/log_blue_m2b_sep22_qe.out")
m1_blue_sep22 = np.genfromtxt("2022/2022Sep/log_blue_m1b_sep22_qe.out")
m1_red_sep22 = np.genfromtxt("2022/2022Sep/log_red_m1r_sep22_qe.out")
m2_red_sep22 = np.genfromtxt("2022/2022Sep/log_red_m2r_sep22_qe.out")


fig,ax = pl.subplots(1,1)

plotHeight = 3000 # plot width and height in pixels
plotWidth = 4000
hDisp = plotHeight
wDisp = plotWidth
dpi = 300 # dpi = 300 gives finer resolution and nicer plots.
fig.set_dpi(dpi)
wInches = float(wDisp)/float(dpi)
hInches = float(hDisp)/float(dpi)
fig.set_size_inches(wInches,hInches,forward=True)




ax.plot(m1_blue_sep22[:,0],m1_blue_sep22[:,1],color="grey",label="MODS1B direct Sep2022")
ax.plot(m1_bdual_sep22[:,0],m1_bdual_sep22[:,1],color="grey",linestyle="dotted",label="MODS1B dual Sep2022")
ax.plot(m2_red_sep22[:,0],m2_red_sep22[:,1],color="black",label="MODS2R direct Sep2022")
ax.plot(m2_rdual_sep22[:,0],m2_rdual_sep22[:,1],color="black",linestyle="dotted",label="MODS2R dual Sep2022")
ax.plot(m2_blue_sep22[:,0],m2_blue_sep22[:,1],color="black",label="MODS2B direct Sep2022")
ax.plot(m2_bdual_sep22[:,0],m2_bdual_sep22[:,1],color="black",linestyle="dotted",label="MODS2B dual Sep2022")
ax.plot(m1_red_sep22[:,0],m1_red_sep22[:,1],color="grey",label="MODS1R direct Sep2022")
ax.plot(m1_rdual_sep22[:,0],m1_rdual_sep22[:,1],color="grey",linestyle="dotted",label="MODS1R dual Sep2022")

#m1_bdual_dec22 = np.genfromtxt("2022/2022Dec/log_dual_m1b_dec22_qe.out")
#m1_rdual_dec22 = np.genfromtxt("2022/2022Dec/log_dual_m1r_dec22_qe.out")
#m2_rdual_dec22 = np.genfromtxt("2022/2022Dec/log_dual_m2r_dec22_qe.out")
#m2_bdual_dec22 = np.genfromtxt("2022/2022Dec/log_dual_m2b_dec22_qe.out")
#m2_blue_dec22 = np.genfromtxt("2022/2022Dec/log_blue_m2b_dec22_qe.out")
#m1_blue_dec22 = np.genfromtxt("2022/2022Dec/log_blue_m1b_dec22_qe.out")
#m1_red_dec22 = np.genfromtxt("2022/2022Dec/log_red_m1r_dec22_qe.out")
#m2_red_dec22 = np.genfromtxt("2022/2022Dec/log_red_m2r_dec22_qe.out")

#ax.plot(m1_blue_dec22[:,0],m1_blue_dec22[:,1],color="grey",label="MODS1B direct Dec2022")
#ax.plot(m1_bdual_dec22[:,0],m1_bdual_dec22[:,1],color="grey",linestyle="dotted",label="MODS1B dual Dec2022")
#ax.plot(m2_red_dec22[:,0],m2_red_dec22[:,1],color="black",label="MODS2R direct Dec2022")
#ax.plot(m2_rdual_dec22[:,0],m2_rdual_dec22[:,1],color="black",linestyle="dotted",label="MODS2R dual Dec2022")
#ax.plot(m2_blue_dec22[:,0],m2_blue_dec22[:,1],color="black",label="MODS2B direct Dec2022")
#ax.plot(m2_bdual_dec22[:,0],m2_bdual_dec22[:,1],color="black",linestyle="dotted",label="MODS2B dual Dec2022")
#ax.plot(m1_red_dec22[:,0],m1_red_dec22[:,1],color="grey",label="MODS1R direct Dec2022")
#ax.plot(m1_rdual_dec22[:,0],m1_rdual_dec22[:,1],color="grey",linestyle="dotted",label="MODS1R dual Dec2022")

ax.plot(m1_blue[:,0],m1_blue[:,1],color="blue",linewidth =1,label="MODS1B direct Dec2011")
ax.plot(m1_bdual[:,0],m1_bdual[:,1],color="blue",linewidth =1,linestyle="dotted",label="MODS1B dual Dec2011")
ax.plot(m1_red[:,0],m1_red[:,1],color="red",linewidth =1,label="MODS1R direct Dec2011")
ax.plot(m1_rdual[:,0],m1_rdual[:,1],color="red",linewidth =1,linestyle="dotted",label="MODS1R Dec2011")
ax.plot(m2_blue[:,0],m2_blue[:,1],color="skyblue",linewidth =1,label="MODS2B direct May2015")
ax.plot(m2_bdual[:,0],m2_bdual[:,1],color="skyblue",linewidth =1,linestyle="dotted",label="MODS2B dual May2015")
ax.plot(m2_red[:,0],m2_red[:,1],color="lightcoral",linewidth =1,label="MODS2R direct May2015")
ax.plot(m2_rdual[:,0],m2_rdual[:,1],color="lightcoral",linewidth =1,linestyle="dotted",label="MODS2R dual May2015")


ax.set_xlabel("Wavelength [Angstroms], fontsize=14")
ax.set_ylabel("Efficiency MODS +telescope (reflectivity=90%), airmass=0", fontsize=14)

ax.legend()

pl.savefig("MODS1_MODS2_qe_evol.png")
