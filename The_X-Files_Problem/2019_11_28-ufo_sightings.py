# -*- coding: utf-8 -*-
"""
Created on Thu Nov 28 17:23:30 2019

@author: gvega
"""


import os
import numpy as np
import pandas as pd
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

"""
#IDEA BOX

build a histogram with country frequency (and maybe state)
    building on that idea we could clusters lat/longs and build an histogram for those too


"""