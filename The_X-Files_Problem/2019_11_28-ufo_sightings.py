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
from collections import Counter

#read data from folder, could be taken from database or any other method as well
os.chdir(r'C:\\Users\gvega\OneDrive\Documentos\Code\Intelimetrica_exam\The_X-Files_Problem\ufo_sightings')
ufo_sightings  = pd.read_csv('UFO_sightings.csv')



#Hypotesis #1, the sightings are clustered in specific areas:
def buildMapFromPandasDatabase(database):
    fig = plt.figure(figsize=(18, 16), edgecolor='w')
    m = Basemap(projection='moll', resolution=None,
                lat_0=0, lon_0=0)
    m.etopo()
    # Map (long, lat) to (x, y) for plotting
    for i in range(len(database)):    
        x, y = m(database.iloc[i]['longitude'], database.iloc[i]['latitude'])
        plt.plot(x, y, 'ok', markersize=3)
#clearly most sightings are in north america (The US Specifically) and Europe

#Scince the question is basically all about location i will ignore comments, and shape
    
    
#I will start checking if there is a difference with distribution with time
#Will hardcode this things to make it faster. Check in the future how to do a df inside another one
def buildDatabasesByTimeAndPlotMapsPerTimePeriod(ufo_sightings):
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
    building the maps according to time
    buildMapFromPandasDatabase(DF1940to1960)
    buildMapFromPandasDatabase(DF1960to1980)
    buildMapFromPandasDatabase(DF1980to2000)
    buildMapFromPandasDatabase(DF2000to2020)
    
    basically the more time passes the more sightings there are
    but the US is still the main place.
    this will be useful to present, but to answer the question of where
    should the guy go, I will cluster some lats,longs and build an histogram
    """
    
def clusterDataByLatLong(ufo_sightings):
    #To cluster I will do it by degree of longitude/latitude
    # -40.2,80 will be clustered with -40.8, 80.7
    #this is because one degree = 69 miles (approx) and its not practical to travel more than that
    #I will consider every sighting to have the same importance
    latArray = []
    longArray = []
    mergedArray = []
    exceptionIndexArray = []
    for i in range(len(ufo_sightings)): #basically build an array for latitude, for longitude and both
        try:
            latArray.append(int(float(ufo_sightings.iloc[i]['latitude'])))
            longArray.append(int(float(ufo_sightings.iloc[i]['longitude'])))
            mergedArray.append((str(int(float(ufo_sightings.iloc[i]['longitude']))) + " " + str(int(float(ufo_sightings.iloc[i]['latitude'])))))
        except:
            exceptionIndexArray.append(i)
            #literally one number had a 'b' in the longitude, i just ignored it
            #probably thats why I get an error when building the maps.
            #might delete later
        
    
    """
    if you wanted to build an histogram of the latitude and longitude separately 
    you use this, but its the combination what matters
    latLongPandas = pd.DataFrame()
    latLongPandas['Longitude'] = latArray
    latLongPandas['Latitude'] = longArray
    latLongPandas['Longitude'].plot.hist()
    latLongPandas['Latitude'].plot.hist()
    """
def buildingDictionariesAndBuildHistogramOfLocations(mergedArray):
    mergedStringCounts = Counter(mergedArray) #counting every instance of a sighting in a zone
    filteredMergedCounts = {} #remove values under certain frequency, in this case under 1000
    for value in mergedStringCounts:
        if(mergedStringCounts[value] > 1000):
            filteredMergedCounts[value] = mergedStringCounts[value]
            
    #instead of the coordinate write the name of the place        
    namedCountsForHistogram = {}
    namedCountsForHistogram['Fairfax Forest Reserve'] = filteredMergedCounts['-122 47'] 
    namedCountsForHistogram['Hillgrove'] = filteredMergedCounts['-118 34'] 
    namedCountsForHistogram['Toms River'] = filteredMergedCounts['-74 40'] 
    namedCountsForHistogram['Poway'] = filteredMergedCounts['-117 33'] 
    
    latLongMergedPandas = pd.DataFrame.from_dict(namedCountsForHistogram, orient='index')
    
    latLongMergedPandas.plot(kind='bar')

    #Hillgrove and Poway are very close to each other, so I will build a map with
        #the data to see if there is any cluster
    filteredMergedCountsForMap = {} #remove values under certain frequency, in this case under 500
    for value in mergedStringCounts:
        if(mergedStringCounts[value] > 800):
            filteredMergedCountsForMap[value] = mergedStringCounts[value]
    
    latArray = [] #I am repeating this variables, I could transform them into methods and we avoid any trouble
    longArray = []
    
    for value in filteredMergedCountsForMap: #Building the array in a format understandable for mapping
        longArray.append(value[:value.find(" ")])
        latArray.append(value[value.find(" ")+1:])
    
    filteredMergedCountsForMapPandas = pd.DataFrame()
    filteredMergedCountsForMapPandas['longitude'] = longArray
    filteredMergedCountsForMapPandas['latitude'] = latArray
    
    buildMapFromPandasDatabase(filteredMergedCountsForMapPandas)

#I can safely reccomend that Mr.TinFoil should go to Calidornia,
#specifically San Diego, California, -117.5, 33.5


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
    building on that idea we could clusters lat/longs and build an histogram for those too -DONE

note: sightings might have a time shift with distribution, I have to see if 
evey ¿decade? is there a shift in position of sightings - DONE

"""

"""
pending box:
    
exceptionIndexArray.append(i)
#literally one number had a 'b' in the longitude, i just ignored it
#probably thats why I get an error when building the maps.
#might delete later
"""