# -*- coding: utf-8 -*-
"""
Created on Thu Nov 28 17:23:30 2019

@author: gvega
"""


import os
import numpy as np
import pandas as pd
import datetime
from matplotlib import pyplot as plt
from mpl_toolkits.basemap import Basemap

#read data from folder, could be taken from database or any other method as well
os.chdir(r'C:\\Users\gvega\OneDrive\Documentos\Code\Intelimetrica_exam\The_X-Files_Problem\ufo_sightings')
ufo_sightings  = pd.read_csv('UFO_sightings.csv')



#Hypotesis #1, the sightings are clustered in specific areas:
fig = plt.figure(figsize=(18, 16), edgecolor='w')
m = Basemap(projection='moll', resolution=None,
            lat_0=0, lon_0=0)
m.etopo()
# Map (long, lat) to (x, y) for plotting
for i in range(len(ufo_sightings)):    
    x, y = m(ufo_sightings.iloc[i]['longitude'], ufo_sightings.iloc[i]['latitude'])
    plt.plot(x, y, 'ok', markersize=5)
    latlong = ufo_sightings.iloc[i]['latitude'], ufo_sightings.iloc[i]['longitude']
#clearly most sightings are in north america (The US Specifically) and Europe

#Scince the question is basically all about location i will ignore comments, and shape
    
    
#I will start checking if there is a difference with distribution with time
#Will hardcode this things to make it faster. Check in the future how to do a df inside another one
DF1940to1960 = pd.DataFrame()
DF1960to1980 = pd.DataFrame()
DF1980to2000 = pd.DataFrame()
DF2000to2020 = pd.DataFrame()
for i in range(len(ufo_sightings)):
    #Day and month are not zero padded, make them padded
    timeString = ufo_sightings.iloc[i]['datetime']
    if(timeString[1] == "/" ): #pad month
        timeString = "0" + timeString
    
    if(timeString[4] == "/"): #pad day
        timeString = timeString[:3] + "0" + timeString[3:]
        
    if(timeString[11:] == "24:00"): #transform 24:00h  to 00:00h
        timeString = timeString[:10] + " 00:00"
    
    currentTime = datetime.datetime.strptime(timeString, '%m/%d/%Y %H:%M')
        
    if currentTime < datetime.datetime(1960,1,1):
        DF1940to1960 = DF1940to1960.append(ufo_sightings.iloc[i])
    elif currentTime < datetime.datetime(1980,1,1):
        DF1960to1980 = DF1960to1980.append(ufo_sightings.iloc[i])
    elif currentTime < datetime.datetime(2000,1,1):
        DF1980to2000 = DF1980to2000.append(ufo_sightings.iloc[i])
    elif currentTime < datetime.datetime(2020,1,1):
        DF2000to2020 = DF2000to2020.append(ufo_sightings.iloc[i])
        
    if(i % int(len(ufo_sightings)/500)):
        print(i/len(ufo_sightings))
#Could I have done a sort() and just find the indices where the condition is met?
    #would that be faster?        - thing is, to sort you need to convert to date anyways

"""
to save and continue working later
DF1940to1960.to_csv("DF1940to1960.csv")
DF1960to1980.to_csv("DF1960to1980.csv")
DF1980to2000.to_csv("DF1980to2000.csv")
DF2000to2020.to_csv("DF2000to2020.csv")
"""
"""
#IDEA BOX

build a histogram with country frequency (and maybe state)
    building on that idea we could clusters lat/longs and build an histogram for those too

note: sightings might have a time shift with distribution, I have to see if 
evey ¿decade? is there a shift in position of sightings

"""