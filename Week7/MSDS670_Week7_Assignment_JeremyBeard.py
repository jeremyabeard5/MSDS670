# MSDS670_Week7_Assignment_JeremyBeard.py

'''
Title: MSDS670 Week 7 Assignment
Date: 18JUN2023
Author: Jeremy Beard
Purpose: Process traffic accident data and create chloropleth map
Inputs: Denver Traffic Accident Dataset: https://www.kaggle.com/datasets/hrokrin/denver-traffic-accidents
Outputs: Chloropleth map of denver fatal car accidents
Thank you
'''

print('Hello World')

import os

import pandas as pd
from shapely.geometry import Point
import geopandas as gpd
from geopandas import GeoDataFrame
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px

#Set directories
project_dir = r'C:\\Users\\jerem\\OneDrive\\Documents\\School\\_REGIS\\2023-05_Summer\\MSDS670\\MSDS670\\Week7\\'
data_dir = project_dir + r'data\\'
output_dir = project_dir + r'output\\'

#Read csv file into dataframe
#df_filename = 'realtor-data.csv'
df_filename = 'traffic_accidents.csv'
df = pd.read_csv(data_dir + df_filename)

#Get some info on the data
print('LOADED DATA: ')
print(df.head(20))
print('LOADED DATA INFO: ')
print(df.info())
print('LOADED DATA SHAPE: ')
print(df.shape)

# drop Object_Id, Incident_Id, Offense_Id, Offense_Code_Extension columns
df.drop(['Object_Id', 'Incident_Id', 'Offense_Id', 'Offense_Code_Extension'], axis=1, inplace=True)


# examine Traffic Offenses category
print('\nTraffic Offenses value_counts (before): ')
print(df['Top_Traffic_Accident_Offense'].value_counts(ascending=True))  

# drop any rows with Top_Training_Offense = 'Pending Investigation and/or Court Hearing'
print('\nDropping rows with Top_Traffic_Accident_Offense = Pending Investigation and/or Court Hearing')
df = df[df['Top_Traffic_Accident_Offense'] != 'Pending Investigation and/or Court Hearing']

print('\nTraffic Offenses value_counts (after): ')
print(df['Top_Traffic_Accident_Offense'].value_counts(ascending=True))  

# examine Fatalities category
print('\nFatalities value_counts (before): ')
print(df['Fatalities'].value_counts(ascending=True))

# drop any rows which are not fatalities, including rows which are merely under investigation
print('\nDropping rows with Fatalities = 0')
df = df[df['Fatalities'] != '0.0']
df = df[df['Fatalities'] != '0.0 ']
df = df[df['Fatalities'] != 0.0]
df = df[df['Fatalities'] != 'Under Investigation']

# examine Fatalities category
print('\nFatalities value_counts (after): ')
print(df['Fatalities'].value_counts(ascending=True))

print('Road Location value_counts: ')
print(df['Road_Location'].value_counts(ascending=True))  

print('\nTraffic Offenses value_counts (afterrrr): ')
print(df['Top_Traffic_Accident_Offense'].value_counts(ascending=True))  

df_filename2 = 'colorado-counties.geojson'
data = gpd.read_file(data_dir + df_filename2)
data.plot()

categories = df['Top_Traffic_Accident_Offense']
unique_categories = df['Top_Traffic_Accident_Offense'].unique()
print('\nCategories: ')
print(unique_categories)

colors = {'Traf - Accident - Fatal': 'red', 'Traf - Accident - Hit & Run': 'yellow', 'Traf - Accident - Police': 'blue', 'Traf - Accident - SBI': 'green', 'Traf - Accident - DUI/DUID': 'orange', 'Traf - Accident': 'purple'}
plt.scatter(x=df['Geo_Lon'], y=df['Geo_Lat'], s=15, alpha=0.1, c='yellow')#, c=df['Top_Traffic_Accident_Offense'].map(colors), alpha=0.3)
plt.xlim([-105.5, -104.5])
plt.ylim([39.5, 40])
plt.title('CO Fatal Accidents, 2012-Present')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.show()

print('Done')