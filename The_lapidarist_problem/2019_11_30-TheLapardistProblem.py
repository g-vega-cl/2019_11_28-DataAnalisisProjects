# -*- coding: utf-8 -*-
"""
Created on Sat Nov 30 10:04:09 2019

@author: gvega
"""
import os
import numpy as np
import pandas as pd
import datetime
from matplotlib import pyplot as plt
import seaborn as sns
from collections import Counter
import random 
import matplotlib

#read data from folder, could be taken from database or any other method as well
os.chdir(r'C:\\Users\gvega\OneDrive\Documentos\Code\Intelimetrica_exam\The_lapidarist_problem\diamonds')
diamonds_data  = pd.read_csv('diamonds_data_removedOutliersAndImpossibilities.csv')



#Checking data integrity
def checkDataIntegrity(dataset):
    print(dataset.describe())
    print(dataset.isnull().sum())
    matplotlib.pyplot.boxplot(diamonds_data['carat'])
    
def descriptiveAndSummaryAnalysis(dataset):
    dataset.hist(figsize = (20,20),bins=20)
    
    sns.set(context="notebook", palette="Spectral", style = 'darkgrid' ,font_scale = 1.5, color_codes=True)
    plt.figure(figsize=(20,20))
    sns.heatmap(dataset.corr(), cmap='RdYlGn',annot=True, square = True)
    plt.show()
