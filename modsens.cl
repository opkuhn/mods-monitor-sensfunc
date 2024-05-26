 ##############################################################################
 #                                                                            #
 #  modsens.cl                                                                #
 #                                                                            #
 #  Given a list of trimmed, flat-fielded, bad-pixel corrected, OT subtracted #
 #   images, for each image in the list, this script:                         #
 #     extracts 1D std star spectrum (apall)                                  #
 #     extracts a corresponding spectrum from the complamp image (apall)      # 
 #     reidentifies the comp lamp spectrum                                    #
 #     references the comp lamp spectrum to its associated std star spectrum  #
 #     wavelength calibrates the std star spectrum (dispcor)                  #
 #     associates the std with a template standard star spectrum              #
 #     determines the sensitivity function and outputs that                   #
 #                                                                            #
 #  The results are, for each input spectrum:                                 # 
 #      a wavelength calibrated spectrum;                                     # 
 #      a standard star table output by "standard"; and                       #
 #      a sensitivity function                                                #
 #                                                                            #
 #  The sensitivity function requires care to fit, because of the dichroic    #
 #   wiggles. It is not used.                                                 #
 #                                                                            #
 #  The tables output by "standard" contain 4 columns:                        #
 #      (1) wavelength [angstroms]                                            #
 #      (2) flam[erg/s/cm2/angstrom] from the 10-Ang std star flux table      #
 #      (3) bin width (10 Angstroms)                                          #
 #      (4) counts in the mods spectrum over a 10-Ang bin                     #
 #  and a leading line which contains the name of the spectrum,               #
 #      information on the dimension of that image (1 5601, e.g.?)            #
 #      exptime                                                               #
 #      airmass                                                               #
 #      first and last wavelength in the image                                #
 #      image title                                                           #
 #                                                                            #
 #  To compute the zeropoints, the list of standard star tables is            #
 #      input to the python script, sensplist2_v1.0.py                        #
 #  The script computes the zeropoint, plots it as a function of wavelength   #
 #      and plots also the zeropoint at a particular wavelength as            #
 #      a function of time.                                                   #
 #                                                                            #
 #                                                                            #
 #  Olga Kuhn - LBT Observatory                                   IRAF v2.16  #
 #                                                        written: 23.Jun.16  #
 #                                                        update : 26.Sep.22  #
 #                                                                            #
 ##############################################################################

procedure modsens (imagelist,bcompim,bcompid,rcompim,rcompid,autoap,awidth)

 string imagelist {      "",prompt="List of images?"}
 string bcompim    {     "",prompt="Name of blue 2D comparison lamp spectrum"}
 string bcompid    {     "",prompt="Name of blue 1D identified comparison lamp spectrum"}
 string rcompim    {     "",prompt="Name of red 2D comparison lamp spectrum"}
 string rcompid    {     "",prompt="Name of red 1D identified comparison lamp spectrum"}
 bool   autoap    {     yes,prompt="Automatically set aperture limits?"}
 int    awidth    {     80,prompt="used if autoap = no, default: +/-40 pix"}
 bool   verbose   {     yes,prompt="Verbose output to screen?"}
 bool   interact  {     yes,prompt="Interactive?"}

 struct *flist

begin

   ############################################################################
   ## Declare all variables used in this task:
   string  imlist,bcomp1,bcompimage,rcomp1,rcompimage,comp1,compimage   
   bool    quiet,log,inter,aap

   ### Image variables (headers, filenames):
   string  image, eximage, cimage
   string  wavimage,swavimage,snfunc,senslog
   string  kwdlis1,objnam,object,obj_name
   string  inst,airmass,datetime,mjd,stdtables,extfile,linelists,clist
   string  tsam,bsam,star
   string  getcmd,dum
   real    lam1,lam2,awid,aplo,aphi
   real    line4000, nsum50
   int     k

   ############################################################################
   ### Pass parameters to internal variables:
   imlist     = imagelist
   bcomp1      = bcompid
   bcompimage  = bcompim
   rcomp1      = rcompid
   rcompimage  = rcompim
   quiet      = !verbose 
   inter      = interact
   aap        = autoap
   awid       = awidth/2.0  # half width to input to apall

   aplo = -1*awid
   aphi = awid

   #linelists = "/scratch/MODS/CalTables/linelists/"
   #stdtables = "/scratch/MODS/CalTables/fluxcal/Tables/"
   #extfile = "/scratch/MODS/CalTables/fluxcal/lbtextinct.dat"

   linelists = "/home/olga/Dropbox/MODS/CalTables/linelists/"
   stdtables = "/home/olga/Dropbox/MODS/CalTables/fluxcal/Tables/"
   extfile = "/home/olga/Dropbox/MODS/CalTables/fluxcal/lbtextinct.dat"

   #linelists = "/Users/olga/MODS/Calib/modsSpecPhot/Tables/"
   #stdtables = "/Users/olga/MODS/Calib/modsSpecPhot/Tables/"
   #extfile = "/Users/olga/MODS/Calib/modsSpecPhot/Tables/lbtextinct.dat"

   ############################################################################
   ### Loop through images in list
   flist = imlist

   while (fscan (flist, image) != EOF) {

      k = strlen(image)
      printf ("image = %s \n",image)
      printf ("substr(image,1,k-5) = %s \n",substr(image,1,k-5))
      if (substr(image,k-4,k) == ".fits") { 
         image = substr(image,1,k-5)
         }
      printf ("image = %s \n",image)

      eximage = image//".ms.fits"
      cimage = image//".cp.fits"
      wavimage = "w"//eximage
      swavimage = "std_"//image//".tab"
      senslog = "sens_"//image//".log"
      snfunc = "sn"//eximage
      if (access(eximage)) { dele(eximage)}
      if (access(cimage)) { dele(cimage)}
      if (access(wavimage)) { dele(wavimage)}
      if (access(swavimage)) { dele(swavimage)}
      if (access(snfunc)) { dele(snfunc)}

      kwdlis1 = "instrume,airmass,date-obs,mjd-obs"
      hselect (image, kwdlis1, yes) | scan (inst,airmass,datetime,mjd)
      #getcmd =  "!gethead -b "//image//".fits object"
      getcmd =  "!gethead -b "//image//".fits objname"
      print ( getcmd ) | cl () | scanf("%20s",obj_name)
      printf ("image = %s \n",image)
      objnam = substr(obj_name,1,8)
      printf ("image = %s obj_name = %s \n",image,obj_name)
      if (objnam == "BD+28d42" || objnam == "BD+28_42" || objnam == "BD28+421") {star="bd28d4211_10a"}
      else if (objnam == "BD+33d26" || objnam == "BD+33_26") {star="bd33d2642_10a"}
      else if (objnam == "Feige_11") {star="feige110_10a"}
      else if (objnam == "Feige_34") {star="feige34_10a"}
      else if (objnam == "Feige_66") {star="feige66_10a"}
      else if (objnam == "Feige_67") {star="feige67_10a"}
      else if (objnam == "G191-B2B" || objnam == "G191B2B") {star="g191b2b_10a"}
      else if (objnam == "GD_71" || objnam == "GD71") {star="gd71_10a"}
      else if (objnam == "GD_140" || objnam == "GD140") {star="gd140_10a"}
      else if (objnam == "GD_153" || objnam == "GD153") {star="gd153_10a"}
      else if (objnam == "Hiltner_") {star="hilt600_10a"}
      else if (objnam == "Hz44" || objnam == "Hz_44") {star="hz44_10a"}
      else if (objnam == "Hz43" || objnam == "Hz_43") {star="hz43_10a"}
      else if (objnam == "PG0823+5") {star="pg0823_10a"}
      else if (objnam == "Wolf_134") {star="wolf1346_10a"}
      else {
	print "There is no star for OBJNAM %s \n", objnam)
	print "File %s cannot be analyzed. \n", eximage)
	goto next_file
	}
      printf ("image = %s objnam = %s \n",image,objnam)

	if (inst == "MODS2R") {
		tsam = "*"
		bsam = "-300:-200,110:160"
		comp1 = rcomp1
		compimage = rcompimage
		#clist = "/Users/olga/MODS/linelists/all_red.wav"
		clist = linelists//"dualred.wav"
		lam1 = 4900
		#lam1 = 5500
		lam2 = 11000
		}
	if (inst == "MODS2B") {
		tsam = "1500:8192"
		bsam = "-250:-200,110:160"
		comp1 = bcomp1
		compimage = bcompimage
		#clist = "/Users/olga/MODS/linelists/all_blue.wav"
		clist = linelists//"dualblue.wav"
		lam1 = 3190
		#lam2 = 6000
		lam2 = 6500
		}
	if (inst == "MODS1R") {
		#tsam = "*"
		tsam = "1:7490"
		bsam = "-300:-200,110:145"
		comp1 = rcomp1
		compimage = rcompimage
		#clist = "/Users/olga/MODS/linelists/all_red.wav"
		clist = linelists//"dualred.wav"
		lam1 = 4900
		#lam1 = 5500
		lam2 = 11000
		}
	if (inst == "MODS1B") {
		tsam = "1500:8192"
		bsam = "-300:-200,110:145"
		comp1 = bcomp1
		compimage = bcompimage
		#clist = "/Users/olga/MODS/linelists/all_blue.wav"
		clist = linelists//"dualblue.wav"
		lam1 = 3190
		#lam2 = 6000
		lam2 = 6500
		}

   
    ### Extract std star spectrum

line4000=4000
nsum50 = 50

if (aap) {

apall (image, 1, output=eximage, apertures="", format="multispec", references=" ", profiles=" ", interactive=inter, find=yes, recenter=yes, resize=yes, edit=yes, trace=yes, fittrace=yes, extract=yes, extras=yes, review=yes, line=line4000, nsum=nsum50, lower=-5., upper=5., apidtable="", b_function="chebyshev", b_order=3, b_sample=bsam, b_naverage=-3, b_niterate=5, b_low_reject=3., b_high_rejec=3., b_grow=0., width=10., radius=10., threshold=0., minsep=5., maxsep=100000., order="increasing", aprecenter="", npeaks=INDEF, shift=yes, llimit=INDEF, ulimit=INDEF, ylevel=9.9999997473788E-5, peak=yes, bkg=yes, r_grow=0., avglimits=no, t_nsum=50, t_step=50, t_nlost=3, t_function="chebyshev", t_order=5, t_sample=tsam, t_naverage=1, t_niterate=10, t_low_reject=3., t_high_rejec=3., t_grow=0., background="fit", skybox=1, weights="variance", pfit="fit1d", clean=no, saturation=65000., readnoise="2.5", gain="2.5", lsigma=3., usigma=3., nsubaps=1) 
   }

else if (!aap) {

apall (image, 1, output=eximage, apertures="", format="multispec", references="", profiles="", interactive=inter, find=yes, recenter=yes, resize=yes, edit=yes, trace=yes, fittrace=yes, extract=yes, extras=yes, review=yes, line=line4000, nsum=nsum50, lower=-5., upper=5., apidtable="", b_function="chebyshev", b_order=3, b_sample=bsam, b_naverage=-3, b_niterate=5, b_low_reject=3., b_high_rejec=3., b_grow=0., width=10., radius=10., threshold=0., minsep=5., maxsep=100000., order="increasing", aprecenter="", npeaks=INDEF, shift=yes, llimit=aplo, ulimit=aphi, ylevel=INDEF, peak=yes, bkg=yes, r_grow=0., avglimits=no, t_nsum=50, t_step=50, t_nlost=3, t_function="chebyshev", t_order=5, t_sample=tsam, t_naverage=1, t_niterate=10, t_low_reject=3., t_high_rejec=3., t_grow=0., background="fit", skybox=1, weights="variance", pfit="fit1d", clean=yes, saturation=65000, readnoise="2.5", gain="2.5", lsigma=3., usigma=3., nsubaps=1)

}

    ### Extract comp lamp spectrum corresponding to std star (only set referen=image)
   #apall (compimage, 1, output=cimage, apertures="", format="multispec", referen=image, profile=image, interactive=no, find=no, recenter=no, resize=no, edit=no, trace=no, fittrace=no, extract=yes, extras=yes, review=no, line=INDEF, nsum=10, lower=-5., upper=5., apidtable="", b_function="chebyshev", b_order=3, b_sample="-200:-80,80:150", b_naverage=-3, b_niterate=5, b_low_reject=3., b_high_rejec=3., b_grow=0., width=10., radius=10., threshold=0., minsep=5., maxsep=100000., order="increasing", aprecenter="", npeaks=INDEF, shift=yes, llimit=INDEF, ulimit=INDEF, ylevel=9.9999997473788E-5, peak=yes, bkg=yes, r_grow=0., avglimits=no, t_nsum=50, t_step=50, t_nlost=3, t_function="chebyshev", t_order=5, t_sample=tsam, t_naverage=1, t_niterate=0, t_low_reject=3., t_high_rejec=3., t_grow=0., background="none", skybox=1, weights="variance", pfit="fit1d", clean=no, saturation=65000., readnoise="2.5", gain="2.5", lsigma=3., usigma=3., nsubaps=1)
   apall (compimage, 1, output=cimage, apertures="", format="multispec", referen=image, profile="", interactive=no, find=no, recenter=no, resize=no, edit=no, trace=no, fittrace=no, extract=yes, extras=yes, review=no, line=INDEF, nsum=10, lower=-5., upper=5., apidtable="", b_function="chebyshev", b_order=3, b_sample="-200:-80,80:150", b_naverage=-3, b_niterate=5, b_low_reject=3., b_high_rejec=3., b_grow=0., width=10., radius=10., threshold=0., minsep=5., maxsep=100000., order="increasing", aprecenter="", npeaks=INDEF, shift=yes, llimit=INDEF, ulimit=INDEF, ylevel=9.9999997473788E-5, peak=yes, bkg=yes, r_grow=0., avglimits=no, t_nsum=50, t_step=50, t_nlost=3, t_function="chebyshev", t_order=5, t_sample=tsam, t_naverage=1, t_niterate=0, t_low_reject=3., t_high_rejec=3., t_grow=0., background="none", skybox=1, weights="variance", pfit="fit1d", clean=no, saturation=65000., readnoise="2.5", gain="2.5", lsigma=3., usigma=3., nsubaps=1)

    ### Identify this comp lamp spectrum, using the 1D reference spectrum input: bcompref, rcompref
    reidentify(reference = comp1, images = cimage, answer = "yes", interactive = inter, section = "middle line", newaps = yes, override = yes, refit = yes, trace = no, step = "10", nsum = "10", shift = "0.", search = 0., nlost = 0, cradius = 5., threshold = 0., addfeatures = no, coordlist = clist, match = -3., maxfeatures = 50, minsep = 2., database = "database", logfiles = "logfile", plotfile = "", verbose = no, graphics = "stdgraph", cursor = "", aidpars = "")

    ### Reference comp to its associated standard star spectrum
    refspec(input = eximage,answer = "YES", references = cimage, apertures = "", refaps = "", ignoreaps = yes, select = "interp", sort = "", group = "", time = no, timewrap = 17., override = yes, confirm = yes, assign = yes, logfiles = "logfile", verbose = no) 


    ### Wavelength calibrate
    dispcor (eximage, wavimage, linearize=yes, database="database", table="", w1=lam1, w2=lam2, dw=0.5, nw=INDEF, log=no, flux=yes, blank=0., samedisp=no, global=no, ignoreaps=no, confirm=no, listonly=no, verbose=yes, logfile="logfile")
	#save3
	#plain wrong = save5
    #dispcor (eximage, wavimage, linearize=yes, database="database", table="", w1=lam1, w2=lam2, dw=0.5, nw=INDEF, log=yes, flux=yes, blank=0., samedisp=no, global=no, ignoreaps=no, confirm=no, listonly=no, verbose=yes, logfile="logfile")
	#save0
    #dispcor (eximage, wavimage, linearize=yes, database="database", table="", w1=lam1, w2=lam2, dw=0.5, nw=INDEF, log=no, flux=no, blank=0., samedisp=no, global=no, ignoreaps=no, confirm=no, listonly=no, verbose=yes, logfile="logfile")
	#save1
    #dispcor (eximage, wavimage, linearize=yes, database="database", table="", w1=INDEF, w2=INDEF, dw=INDEF, nw=INDEF, log=no, flux=yes, blank=0., samedisp=no, global=no, ignoreaps=no, confirm=no, listonly=no, verbose=yes, logfile="logfile")
	#save2
    #dispcor (eximage, wavimage, linearize=yes, database="database", table="", w1=lam1, w2=lam2, dw=0.5, nw=INDEF, log=no, flux=yes, blank=0., samedisp=no, global=no, ignoreaps=no, confirm=no, listonly=no, verbose=yes, logfile="logfile")
	#save3
    #dispcor (eximage, wavimage, linearize=no, database="database", table="", w1=INDEF, w2=INDEF, dw=INDEF, nw=INDEF, log=no, flux=no, blank=0., samedisp=no, global=no, ignoreaps=no, confirm=no, listonly=no, verbose=yes, logfile="logfile")
	#save4
    #dispcor (eximage, wavimage, linearize=no, database="database", table="", w1=INDEF, w2=INDEF, dw=INDEF, nw=INDEF, log=no, flux=yes, blank=0., samedisp=no, global=no, ignoreaps=no, confirm=no, listonly=no, verbose=yes, logfile="logfile")


    ### Associate instrumental magnitude/flux with tabulated values (interpolated to fill gaps)
    printf("going to standard: wavimage=%s swavimage=%s star=%s\n",wavimage,swavimage,star)
    standard (input = wavimage, output = swavimage, star_name = star, answer = "no", samestar = yes, beam_switch = no, apertures = "", bandwidth = INDEF, bandsep = INDEF, fnuzero = 3.6800000000000E-20, extinction = extfile, caldir = stdtables, interact = inter,graphics = "stdgraph")

    ### Create sensitivity function
    printf("going to sensfunc\n")
    sensfunc (swavimage, snfunc, "yes", apertures="", ignoreaps=yes, logfile=senslog, extinction=extfile, newextinctio="rev.dat", observatory=")_.observatory", function="spline3", order=64, interactive=inter, graphs="sr", marks="plus cross box", colors="2 1 3 4", cursor="", device="stdgraph")

    ### Add time stamp to header of sensitivity function
    #hedit (snfunc, "date-obs", datetime, add=yes, addonly=yes, delete=no, verify=no, show=yes, update=yes)
    #hedit (snfunc, "mjd-obs", mjd , add=yes, addonly=yes, delete=no, verify=no, show=yes, update=yes)


   next_file:
   } # End of loop through imglist

   ############################################################################
   ## Graceful exit, cleanup, and write final messages:
   exit_task:

   if (!quiet) { beep } 

end
