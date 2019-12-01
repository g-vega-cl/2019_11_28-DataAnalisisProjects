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
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
from sklearn import linear_model
from sklearn.model_selection import cross_val_score
from sklearn.tree import DecisionTreeRegressor

#read data from folder, could be taken from database or any other method as well
os.chdir(r'C:\\Users\gvega\OneDrive\Documentos\Code\Intelimetrica_exam\The_lapidarist_problem\diamonds')
diamonds_data  = pd.read_csv('diamonds_data_removedOutliersAndImpossibilities.csv')



#Checking data integrity
def checkDataIntegrity(dataset):
    print(dataset.describe()) #gives back simple statistical analysis of each column
    print(dataset.isnull().sum()) #checks if there are any NULL values in the columns
    matplotlib.pyplot.boxplot(diamonds_data['carat']) #Makes a boxplot of the carat of the diamonds
    
def descriptiveAndSummaryAnalysis(dataset):
    dataset.hist(figsize = (20,20),bins=20) #makes histograms of every column
    #This section builds the heatmap with the desired characteristics
    sns.set(context="notebook", palette="Spectral", style = 'darkgrid' ,font_scale = 1.5, color_codes=True)
    plt.figure(figsize=(20,20))
    sns.heatmap(dataset.corr(), cmap='RdYlGn',annot=True, square = True) 
    plt.show()
    #End of heatmap
    
    #builds a pairplot for the columns of the data
    sns.pairplot(diamonds_data)

#This pre-processes data to properly feed it to the model
def modelDataPreparation(dataset): #there is hardcoded data in this function
    
    #Encoding categorical data with one_hot_encoder
        #so as to be able to properly feed it to the model
    one_hot_encoders_dataset_data =  pd.get_dummies(dataset) #pd.get_dummies transforms categories into dummy/indicator variables
    cols = one_hot_encoders_dataset_data.columns #basically gets the name of the columns, which is the categorical data
    dataset_clean_data = pd.DataFrame(one_hot_encoders_dataset_data, columns = cols) #I think it is the same if we dont add the columns = cols.
    
    #Now comes the data preparation for the numerical data, which is a simple scaling
        #using sklearn StandardScaler
    scaler = StandardScaler() #https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html
    scaledNumericals = pd.DataFrame(scaler.fit_transform( #basically we tall the scaler which data to scale (we dont want to scale categorical data)
            dataset_clean_data[['carat','depth','x','y','z','table']] #NOTE: we only take the numberical data scalers
            ),columns=['carat','depth','x','y','z','table'],index=dataset_clean_data.index)
    
    dataset_clean_data_scaled = dataset_clean_data.copy(deep=True)  #https://www.geeksforgeeks.org/copy-python-deep-copy-shallow-copy/  honestly I still dont really understand this.
    dataset_clean_data_scaled[['carat','depth','x','y','z','table']] = scaledNumericals[['carat','depth','x','y','z','table']]
    
    pd.set_option('display.max_columns', None)
    print(dataset_clean_data_scaled.head()) #Show scaled data
    
    return(dataset_clean_data_scaled)

#It seems that linear regression 
def checkForNegativeValues(y_pred):
    negativeCount = 0
    for value in y_pred:
        if(value < 0):
            negativeCount -= 1
    print(negativeCount)

def buldingRegressionModel(dataset_clean_data_scaled):
    x = dataset_clean_data_scaled.drop(["price"],axis=1) #everything but the price
    y = dataset_clean_data_scaled.price #the price (what we want to forecast)
    #https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html
    train_x, test_x, train_y, test_y = train_test_split(x, y,random_state = 2,test_size=0.3) # 30% of the dataset was used to test accuracy
    #For some reason there are values with NaN, we will drop them.
    train_x = train_x.dropna()
    train_y = train_y.dropna()
    test_x = test_x.dropna()
    test_y = test_y.dropna()
    
    #Linear regression
    regr = linear_model.LinearRegression()
    regr.fit(train_x,train_y)
    y_pred = regr.predict(test_x)
    print("LINEAR REGRESSION")
    print("accuracy: "+ str(regr.score(test_x,test_y)*100) + "%")
    print("Mean absolute error: {}".format(mean_absolute_error(test_y,y_pred)))
    print("Mean squared error: {}".format(mean_squared_error(test_y,y_pred)))
    R2 = r2_score(test_y,y_pred)
    print('R Squared: {}'.format(R2))
    n=test_x.shape[0]
    p=test_x.shape[1] - 1
    adj_rsquared = 1 - (1 - R2) * ((n - 1)/(n-p-1))
    print('Adjusted R Squared: {}'.format(adj_rsquared))
    
    #Lasso Regression
    las_reg = linear_model.Lasso()
    las_reg.fit(train_x,train_y)
    y_pred = las_reg.predict(test_x)
    print("LASSO REGRESSION")
    print("accuracy: "+ str(las_reg.score(test_x,test_y)*100) + "%")
    print("Mean absolute error: {}".format(mean_absolute_error(test_y,y_pred)))
    print("Mean squared error: {}".format(mean_squared_error(test_y,y_pred)))
    R2 = r2_score(test_y,y_pred)
    print('R Squared: {}'.format(R2))
    n=test_x.shape[0]
    p=test_x.shape[1] - 1    
    adj_rsquared = 1 - (1 - R2) * ((n - 1)/(n-p-1))
    print('Adjusted R Squared: {}'.format(adj_rsquared))

    #Ridge Regression
    rig_reg = linear_model.Ridge()
    rig_reg.fit(train_x,train_y)
    y_pred = rig_reg.predict(test_x)
    print("RIDGE REGRESSION")
    print("accuracy: "+ str(rig_reg.score(test_x,test_y)*100) + "%")
    print("Mean absolute error: {}".format(mean_absolute_error(test_y,y_pred)))
    print("Mean squared error: {}".format(mean_squared_error(test_y,y_pred)))
    R2 = r2_score(test_y,y_pred)
    print('R Squared: {}'.format(R2))
    n=test_x.shape[0]
    p=test_x.shape[1] - 1
    adj_rsquared = 1 - (1 - R2) * ((n - 1)/(n-p-1))
    print('Adjusted R Squared: {}'.format(adj_rsquared))

    #DesisionTree Regressor 
    #https://scikit-learn.org/stable/auto_examples/ensemble/plot_adaboost_regression.html#sphx-glr-auto-examples-ensemble-plot-adaboost-regression-py
    #https://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeRegressor.html
    desisionTreeRegressor = DecisionTreeRegressor(random_state=0)
    desisionTreeRegressor.fit(train_x,train_y)
    y_pred = desisionTreeRegressor.predict(test_x)
    print("DecisionTreeRegressor")
    print("accuracy: "+ str(desisionTreeRegressor.score(test_x,test_y)*100) + "%")
    print("Mean absolute error: {}".format(mean_absolute_error(test_y,y_pred)))
    print("Mean squared error: {}".format(mean_squared_error(test_y,y_pred)))
    R2 = r2_score(test_y,y_pred)
    print('R Squared: {}'.format(R2))
    n=test_x.shape[0]
    p=test_x.shape[1] - 1
    adj_rsquared = 1 - (1 - R2) * ((n - 1)/(n-p-1))
    print('Adjusted R Squared: {}'.format(adj_rsquared))
    
    return(regr, las_reg, rig_reg, desisionTreeRegressor)
    
stolen_diamonds_values = pd.read_csv('stolen_diamonds_data_merged.csv')
#note, to add the dummy columns I just added some of the train data,
    #there is probably a better way, but for now this works
def getStolenDiamondsValues(stolen_diamonds_values, regr):
    stolen_diamonds_x_values = modelDataPreparation(stolen_diamonds_values)
    stolen_diamonds_x_values = stolen_diamonds_x_values[:10] #select the stolen values
    y_pred = regr.predict(stolen_diamonds_x_values)
    print(y_pred)
    pd.DataFrame(y_pred).to_csv("y_pred.csv")

def getPercentageVariance(test_x,test_y, regr):
    y_pred = regr.predict(test_x)
    acc = 0
    y_test = test_y.reset_index()
    for i in range(len(y_pred)):
        currentAcc = 1 - (abs(y_pred[i]-y_test['price'][i])/y_pred[i])
        acc += currentAcc
    acc = acc/len(y_pred)
    print(acc)
    
"""
some more citations:
http://www.cyzsoftware.com/files/diamond_price_predictor.pdf
https://www.scribd.com/document/272677658/Predicting-Diamond-Price-Using-Linear-Model
https://csce.ucmss.com/cr/books/2018/LFS/CSREA2018/ICD8070.pdf
https://www.kaggle.com/shivam2503/diamonds
https://en.wikipedia.org/wiki/Coefficient_of_determination
https://www.datasciencecentral.com/profiles/blogs/regression-analysis-how-do-i-interpret-r-squared-and-assess-the 
"""