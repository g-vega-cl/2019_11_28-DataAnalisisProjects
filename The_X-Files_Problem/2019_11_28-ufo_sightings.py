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
import random 
import matplotlib
#read data from folder, could be taken from database or any other method as well
os.chdir(r'C:\\Users\gvega\OneDrive\Documentos\Code\Intelimetrica_exam\The_X-Files_Problem\ufo_sightings')
ufo_sightings  = pd.read_csv('UFO_sightings.csv')

"""
This are helper fucntions to get some specific parts of data or change data types
"""
def buildArrayFromPandasDatabase(dataset,sectionIndexName): #Helper funciton to transform pandas into array
    array = []
    for i in range(len(dataset)):
        try:
            array.append(float(dataset.iloc[i][sectionIndexName]))
        except:
            print("error in array in index: " + str(i))
        
        if(i % 1000 == 0):
            print(i / len(dataset))
    
    return array

    
def saveArrayToCsv(array, name):
    arrayPandas = pd.DataFrame(array)
    arrayPandas.to_csv(name)

def buildHistogramFromArray(array):
    arrayCounted = Counter(array)
    pandasCountedArray = pd.DataFrame.from_dict(arrayCounted, orient = 'index')
    pandasCountedArray.plot(kind='bar')
"""
End of helper functions
"""

#Check latitude, longitude and time(seconds) data integrity
    #To do this we will just pass to float and see if they have any symbols that sould not be there.
def checkLatLongTimeIntegrity(dataset): #Report page 3
    latArray = []
    longArray = []
    secondsArray = []
    for i in range(len(dataset)):
        try:
            longArray.append(float(dataset.iloc[i]['longitude']))
        except:
            print("error in long array in index: " + str(i))
        try:
            latArray.append(float(dataset.iloc[i]['latitude']))
        except:
            print("error in lat array in index: " + str(i))
        try:
            secondsArray.append(float(dataset.iloc[i]['duration (seconds)']))
        except:
            print("error in seconds array in index: " + str(i))
        
        if(i % 1000 == 0):
            print(i / len(dataset))
    returnArray = [latArray, longArray, secondsArray]
    return returnArray

    

#Check consistency of country labels and coordinates
def buildMapFromPandasDatabaseWithText(database): #report page 4
    fig = plt.figure(figsize=(18, 16), edgecolor='w')
    m = Basemap(projection='moll', resolution=None,
                lat_0=0, lon_0=0)
    m.etopo()
    # Map (long, lat) to (x, y) for plotting
    randomRangeStart = random.randint(0, len(database) - 101)
    randomRangeEnd= randomRangeStart + 100
    for i in range(randomRangeStart, randomRangeEnd):    
        x, y = m(database.iloc[i]['longitude'], database.iloc[i]['latitude'])
        plt.plot(x, y, 'ok', markersize=3)
        plt.text(x, y,database.iloc[i]['country'] , fontsize=8);
        
        
#Hypotesis #1, the sightings are clustered in specific areas:

#This is used in other functions to draw the map
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
def buildDatabasesByTimeAndPlotMapsPerTimePeriod(ufo_sightings): #report page 5
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
            
#filtering results of a box and outside the box, this is to see if there is a difference between 
    #duration in and outside US, plus its nice to know the percentage of sightings in the US.
def filterResultsByGeographicalBox(bottomLeftLat,bottomLeftLong,topRightLat,topRightLong,array): #report page 6
    sightingsInBox = pd.DataFrame()
    restOfWorldSightings = pd.DataFrame()
    for i in range(int(len(array))):
        try:
            if int(float(array.iloc[i]['latitude'])) > bottomLeftLat and int(float(array.iloc[i]['longitude'])) > bottomLeftLong:
                if int(float(array.iloc[i]['latitude'])) < topRightLat and int(float(array.iloc[i]['longitude'])) < topRightLong:
                    sightingsInBox = sightingsInBox.append(array.iloc[i])
                else:
                    restOfWorldSightings = restOfWorldSightings.append(array.iloc[i])
            else:
                restOfWorldSightings = restOfWorldSightings.append(array.iloc[i])
        except:
            print("there was an exception")
            pass
        if i% 1000 == 0:
            print(i/(len(array)))
                
    sightingsArray = [sightingsInBox,restOfWorldSightings]
    return sightingsArray            
    
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
        if(i % int(len(ufo_sightings)/100)):
            print(i/len(ufo_sightings))
    return mergedArray


#This function has geographical data hardcoded, care when reusing
def buildingDictionariesAndBuildHistogramOfLocations(mergedArray): #report page 7,8
    mergedStringCounts = Counter(mergedArray) #counting every instance of a sighting in a zone
    filteredMergedCounts = {} #remove values under certain frequency, in this case under 1000
    for value in mergedStringCounts:
        if(mergedStringCounts[value] > 1000):
            filteredMergedCounts[value] = mergedStringCounts[value]
            
    #instead of the coordinate write the name of the place, this is not a reusable function      
    namedCountsForHistogram = {}
    namedCountsForHistogram['Fairfax Forest Reserve'] = filteredMergedCounts['-122 47'] 
    namedCountsForHistogram['Hillgrove'] = filteredMergedCounts['-118 34'] 
    namedCountsForHistogram['Toms River'] = filteredMergedCounts['-74 40'] 
    namedCountsForHistogram['Poway'] = filteredMergedCounts['-117 33'] 
    
    latLongMergedPandas = pd.DataFrame.from_dict(namedCountsForHistogram, orient='index')
    
    latLongMergedPandas.plot(kind='bar')

    #Hillgrove and Poway are very close to each other, so I will build a map with
        #the data to see if there is any cluster
    filteredMergedCountsForMap = {} #remove values under certain frequency, in this case under 800
    for value in mergedStringCounts:
        if(mergedStringCounts[value] > 800):
            filteredMergedCountsForMap[value] = mergedStringCounts[value]
    
    latArray = []
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
    
    

    
    
