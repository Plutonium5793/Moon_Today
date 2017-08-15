#!/usr/bin/python3
"""----------------------------------------------------------------------
Name:        Moon Today
Purpose:     To display  lunar information for current time; converted from 
Solar system today

Author:      John Duchek
Copyright:   In the public domain
Created:     June 6, 2009,
Updated:     Aug 15, 2017

Version       0.20 
display rearrangement of data
Note:  Be sure to replace my data in the 'choose site' section with your data
----------------------------------------------------------------------  """
version = "0.2.0"

#import numpy
import tkinter as tk
from tkinter import ttk

from PIL import Image, ImageTk
from ephem import *
from string import *
from math import *
john=Observer()
file_name=("Day0.jpg","Day1.jpg","Day2.jpg","Day3.jpg","Day4.jpg","Day5.jpg"
,"Day6.jpg","Day7.jpg","Day8.jpg","Day9.jpg","Day10.jpg"
,"Day11.jpg","Day12.jpg","Day13.jpg","Day14.jpg","Day15.jpg"
,"Day16.jpg","Day17.jpg","Day18.jpg","Day19.jpg","Day20.jpg"
,"Day21.jpg","Day22.jpg","Day23.jpg","Day24.jpg","Day25.jpg"
,"Day26.jpg","Day27.jpg","Day28.jpg","Day29.jpg")
daze=0
john=Observer()
# --------------   Choose Site    ------------------------
john_timezone=-5 #Central Daylight Time
site="Karamar, MO" #name of site
john.long,john.lat,john.elev='-90.379025','38.47362',147.9  #longitude, latitude, elevation in meters
#-------------------- Site 2 ------------------------------
#john_timezone=-6  #mountain Daylight time
#site="Carrizozo, NM"
#john.long,john.lat,john.elev='-105.77175','33.60763',1849
# --------------------------------------------------------
john.temp=15 #deg C
john.pressure=1010 #mB
john.date=now()
sun,moon=Sun(),Moon()

local = localtime(john.date)
day_start = local.replace(hour=0, minute=0, second=0, microsecond=0)

moon=Moon()
horizon=""
phase_type=""
illumination=""
john.date=now()
moon.compute(john)

#---------------------make a window-------------------------
win=tk.Tk()
win.title("Moon Today"+" at "+site)
#win.resizable(False, False)
#---------------------makegrid frames---------------------
MainFrame = ttk.LabelFrame(win, text='Moon Today')
MainFrame.grid(row = 0, column = 0,padx=5,pady=5) 

Picture_frame=ttk.LabelFrame(MainFrame,text="Picture")
Picture_frame.grid(column=0,row=0,sticky='W')

site_frame=ttk.LabelFrame(MainFrame,text='Site Information')
site_frame.grid(column=1,row=0,sticky='W')  

rise_frame=ttk.LabelFrame(MainFrame,text='Time')
rise_frame.grid(column=1,row=0,sticky='NWE') 

phase_frame=ttk.LabelFrame(MainFrame,text='Phases')
phase_frame.grid(column=1,row=0,sticky='E') 

current_frame=ttk.LabelFrame(MainFrame,text='Current Info')
current_frame.grid(column=1,row=0,sticky='SW') 

#--------------------------Current Information calculate-----------------------------------
john.date=now()
moon.compute(john)  
if moon.alt <0:
        horizon="Below Horizon"
else:
        horizon="Above Horizon"
            
if  next_new_moon(now()) >next_full_moon(now()):
            phase_type="Waxing"
            daze=0+int((moon.moon_phase*14))
else:
            phase_type=", Waning"
            daze=15+int((1-moon.moon_phase)*14)

current_info = (horizon+"\nDay "+str(daze)+ " and "+phase_type+" in "+str(constellation(
    moon)[1])+"\nSize : "+str(moon.size/60)[0:6]+" (arc-mins)"+"\nIlluminated : "+str(
    moon.moon_phase*100)[0:5]+"%"+"\nMag : "+str(moon.mag)[0:5]+"\nAlt : "+str(
    moon.alt)+"   Az : "+str(moon.az)+"\nRA : "+str(moon.a_ra)+"  Dec : "+str(
    moon.a_dec)+"\nLibration (Lat,  Long):    "+ str(moon.libration_lat)+",     "+str(moon.libration_long))


#--------------------place the picture ----------------------

image = Image.open(file_name[daze])
image1=image.resize((340,340))
photo = ImageTk.PhotoImage(image1)
ttk.Label(Picture_frame,image=photo).grid(column=0,row=0,sticky=tk.NW,padx=5,pady=2)

label = ttk.Label(image=photo)
label.image = photo # keep a reference!


#---------------------site information----------------------
john.date=now()
moon.compute(john)  
lat_long_elev = site+"\nLatitude: "+str(john.lat)+"\nLongitude: "+str(
    john.lon)+"\nElevation: "+str(john.elev)+ " M"
ttk.Label(site_frame,text=lat_long_elev).grid(column=1,row=2,sticky=tk.NW,padx=5,pady=2)


#------------------------------(time) rise, transit, set ------------------------------
rise_transit_set=("Moonrise : "+ str(localtime(john.next_rising(
    moon)))[5:19]+ "\nTransit : "+ str(localtime(john.next_transit(
    moon)))[5:19]+"\nMoonset : " + str(localtime(john.next_setting(moon)))[5:19])

ttk.Label(rise_frame,text=rise_transit_set).grid(column=1,row=1,sticky=tk.W,padx=5,pady=2)

date_local_univ_sidereal="Date : "+str(localtime(
    john.date))[0:10]+"\n"+"Local Time :  "+str(localtime(john.date)).split(
    )[1][:10]+"\nUniversal Time :  "+str(john.date).split(
    )[1][:10]+"\nSidereal Time :  "+(str(john.sidereal_time()))
ttk.Label(rise_frame,text=date_local_univ_sidereal).grid(column=1,row=2,sticky=tk.W,padx=5,pady=2)


#-----------------Moon Phase-------------------------------------------------
john.date=now()
moon.compute(john)


phases = ("New : " + str(localtime(next_new_moon(now(
    ))))[5:19]+"\n1st Q : " + str(localtime(next_first_quarter_moon(now(
    ))))[5:19]+"\nFull : " + str(localtime(next_full_moon(now(
    ))))[5:19]+"\n3rd Q : " + str(localtime(next_last_quarter_moon(now())))[5:19])
ttk.Label(phase_frame,text=phases).grid(column=2,row=1,sticky=tk.W,padx=0,pady=2)

#------------------------current info print-----------------------------

ttk.Label(current_frame,text=current_info).grid(column=3,row=1,padx=5,pady=5)







win.mainloop()  

