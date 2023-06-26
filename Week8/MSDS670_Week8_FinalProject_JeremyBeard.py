# MSDS670_Week8_FinalProject_JeremyBeard.py

'''
Title: MSDS670 Week 8 Final Project
Date: 25JUN2023
Author: Jeremy Beard
Purpose: This script is the final project for MSDS670 and details an analysis of Colorado County Data
Inputs: Colorado County Data (wikipedia + shapefile + geojson)
Outputs: Visualizations on population and population per area in Colorado counties
Thank you
'''

# hello world
print('Hello World')

# import libraries
import os
import pandas as pd
from shapely.geometry import Point
import geopandas as gpd
from geopandas import GeoDataFrame
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import json

#Set directories
project_dir = r'C:\\Users\\jerem\\OneDrive\\Documents\\School\\_REGIS\\2023-05_Summer\\MSDS670\\MSDS670\\Week8\\'
data_dir = project_dir + r'data\\'
output_dir = project_dir + r'output\\'

################################################
# the following section is just a test of a world population dataset
# this was eventually abandoned and colorado was focused on instead
countries = gpd.read_file(data_dir + 'ne_110m_admin_0_countries.shp')

print('Countries: ')
print(countries.head(15))
#for column in countries.columns:
#    print(column)
#print('Countries info :')
#countries.info()
#countries.describe()
plt.style.use('dark_background')
fig, ax = plt.subplots(figsize=(12,10), subplot_kw=dict(aspect='equal'))
ax.set(title='Countries by Population')
countries.plot(column='POP_EST', scheme='quantiles', k=5, cmap='Greens', legend=True, ax=ax, edgecolor='white')
plt.show()
############################################################



################################################################
# The FOLLOWING begins another effort directed at the Colorado counties data
# get colorado county geojson data
# This effort was ultimately deemed unsuccessful but the code is left here for reference and for co_cos_df usage later
co_counties = json.load(open(data_dir + 'Colorado_County_Boundaries.geojson', 'r'))
print(co_counties['features'][0])

# now need to get the tables from wikipedia on colorado counties
# https://en.wikipedia.org/wiki/List_of_counties_in_Colorado

# The process below has been commented out beacuse the data was saved to a csv file
#dfs = pd.read_html('https://en.wikipedia.org/wiki/List_of_counties_in_Colorado')
#print('\nLength of dataframes list: ')
#print(len(dfs))
#co_cos_df = dfs[2]
#dfs[2].to_csv(output_dir + 'Colorado_Counties_wiki.csv')
co_cos_df = pd.read_csv(output_dir + 'Colorado_Counties_wiki.csv')

# Some initial exploration
print('\nColorado Counties Dataframe: ')
print(co_cos_df['County'].unique())
print('\nColorado Counties Areas: ')
print(co_cos_df['Area[6]'][0])
co_cos_df.drop(columns=['County seat[6][7]', 'Est.[8]', 'Formed from[8]', 'Etymology[8]', 'Map', 'Unnamed: 0'], inplace=True)
print('\nColorado counties dataframe after dropping columns:')
print(co_cos_df.head(15))
print('\nColorado counties df columns:')
print(co_cos_df.columns)
print('\nColorado counties df info:')
print(co_cos_df.info())
print('\nColorado counties df describe:')
#print(co_cos_df.describe())


# Some cleaning
# rename Population[9] to Population
co_cos_df.rename(columns={'Population[9]': 'Population'}, inplace=True)
co_cos_df.rename(columns={'Area[6]': 'Area'}, inplace=True)
co_cos_df.rename(columns={'FIPS code[5][b]': 'FIPS'}, inplace=True)

# remove commas from population column
co_cos_df['Area'] = co_cos_df['Area'].apply(lambda x: float(x.replace(',', '').split()[0]))

# create a population per area column
co_cos_df['Population_per_area'] = co_cos_df['Population'] / co_cos_df['Area']

# create log_scales for each of the population and per_area columns in case a tighter scale is needed
co_cos_df['log_ppa'] = np.log10(co_cos_df['Population_per_area'])
co_cos_df['log_pop'] = np.log10(co_cos_df['Population'])
print('\nLog base 10 Population per area: ')
for ppa in co_cos_df['log_ppa']:
    print(ppa)

print('\nPrinting Population per area: ')
for ppa in co_cos_df['Population_per_area']:
    print(ppa)

print(co_counties['features'][0].keys())
# need to create id key in the geojson file for each feature
# that id key will be mapped to column in dataframe
# ultimately this key mapping was deemed unsuccessful and merging was used instead, but the code is left here for reference
co_fips_map = {}
print('\nPrinting co_counties features: ')
for feature in co_counties['features']:
    #print(feature)
    feature['id'] = feature['properties']['NUM_FIPS'] #hmmm
    co_fips_map[feature['properties']['FULL']] = feature['id'] #hmmm  


print('\nPrinting co_fips_map: ')
print(co_fips_map)
# print co_fips_map as pretty print
import pprint
print('\nPrinting co_fips_map as pretty print: ')
print(pprint.pprint(co_fips_map))

print('\nPrinting co_cos_df: ')
# first, rename 'City and County of Broomfield' to just 'Broomfield County'
co_cos_df['County'] = co_cos_df['County'].apply(lambda x: 'Broomfield County' if x == 'City and County of Broomfield' else x)
# do the same to Denver
co_cos_df['County'] = co_cos_df['County'].apply(lambda x: 'Denver County' if x == 'City and County of Denver' else x)
#print(co_cos_df.head(15))
#print(co_cos_df.info())
print(co_cos_df.to_string())

#print('\nprinting the mapping process tests: ') 
#print(co_fips_map['Adams County'])
#print(co_fips_map['Alamosa County'])
#print(co_cos_df['County'][0])
co_cos_df['id'] = co_cos_df['County'].apply(lambda x: co_fips_map[x])
co_cos_df['id'] = co_cos_df['id'].apply(lambda x: str(x))
# again, none of this key/id stuff above was used for anything really

print('\nPrinting co_cos_df: ')
print(co_cos_df.head())
print(co_cos_df.info())

# a quick aside while i try to create a chart via a different approach, using geopandas
# this is to test a quick theory
geo_df = gpd.read_file(data_dir + 'Colorado_County_Boundaries.geojson')
print('\ngeo_df info:   ')
print(geo_df.info())
print('\ngeo_df head:   ')
print(geo_df.to_string())

#############################################################################################
# new approach with shapefile instead of geojson as used below. trying now with shapefile
# we will recycle our work on the co_cos_df dataframe and merge it with a new shapefile
# the 2 visualizations created below were used in the final report
counties = gpd.read_file(data_dir + 'Colorado_County_Boundaries.shp')

co_cos_df['County'] = co_cos_df['County'].str.replace(' County', '')
counties['FULL'] = counties['FULL'].str.replace(' County', '')

# save co_cos_df to csv now that we're done processing it
co_cos_df.to_csv(output_dir + 'co_cos_df.csv', index=False)

# more initial exploration of new shapefile
print('\nCounties: ')
print(counties.head(15))  
print('\nCounties info: ')
print(counties.info())
for col in counties.columns:
    print(col)

print('\nPrinting co_cos_df: ')
print(co_cos_df.head())

# merge the 2 dataframes based on the County column, then create a geodataframe from the merged df
merged_df = pd.merge(co_cos_df, counties, left_on='County', right_on='FULL')
merged_gdf = gpd.GeoDataFrame(merged_df)
print('\nPrinting merged_gdf: ')
print(merged_gdf.head())
print('\nPrinting merged_gdf info: ')
print(merged_gdf.info())

# create static choropleth map with geopandas for a initial look at population data
# this static plot below was used in the final report!
fig, ax = plt.subplots(figsize=(12,10), subplot_kw=dict(aspect='equal'))
merged_gdf.plot(column='Population', scheme='quantiles', k=5, cmap='Blues', legend=True, legend_kwds=dict(loc='lower right', fmt='{:.0f}', interval=True), edgecolor='white', ax=ax)
ax.set_title('Colorado Population by County', fontdict={'fontsize': '25', 'fontweight' : '3'})
plt.show()


# Now let's create a plotly interactive Scattergeo graph object (go) map!
fig = go.Figure(data=go.Scattergeo(
    lat = merged_df['CENT_LAT'],
    lon = merged_df['CENT_LONG'],    
    text = merged_df['County'].astype(str) + ' County: ' + 'Population: ' + merged_df['Population'].astype(str) + ', Population/sq. mi.: ' + merged_df['Population_per_area'].apply(lambda x: "{:.0f}".format(x)) ,
    marker = dict(
        color = merged_df['Population'],
        colorscale = 'Blues',
        reversescale = False,
        opacity = 0.7,
        size = merged_df['log_pop'],
        sizemode="diameter",
        sizeref=0.1,
        colorbar = dict(
            titleside = "right",
            outlinecolor = "rgba(68, 68, 68, 0)",
            ticks = "outside",
            tickvals=[0, 100000, 200000, 300000, 400000, 500000, 600000, 700000],
            ticktext=['0', '100,000', '200,000', '300,000', '400,000', '500,000', '600,000', '700,000'],
            thickness = 30,
            showticksuffix = "last",
            dtick = 0.1
        )
    )
))
fig.update_geos(fitbounds="geojson", visible=True)
fig.update_layout(
    geo = dict(
        scope = 'north america',
        showland = True,
        #landcolor = "rgb(212, 212, 212)",
        landcolor = "rgb(25, 25, 25)",
        subunitcolor = "rgb(255, 255, 255)",
        countrycolor = "rgb(255, 255, 255)",
        showlakes = True,
        lakecolor = "rgb(255, 255, 255)",
        showsubunits = True,
        showcountries = True,
        resolution = 50,
        projection = dict(
            type = 'conic conformal',
            rotation_lon = -100
        ),
        lonaxis = dict(
            showgrid = True,
            gridwidth = 0.5,
            range= [ -140.0, -55.0 ],
            dtick = 5
        ),
        lataxis = dict (
            showgrid = True,
            gridwidth = 0.5,
            range= [ 20.0, 60.0 ],
            dtick = 5
        )
    ),
    title=dict(
        text='Colorado Population by County<br>Source: <a href="https://en.wikipedia.org/wiki/List_of_counties_in_Colorado/">Wiki</a>',
        font=dict(
            family="Arial, sans-serif",
            size=22,
            color="black"
        ),
        x=0.5,
        #y=0.2,
        xanchor="center",
        yanchor="top"
    )
)
fig.show()
fig.write_html(output_dir + 'co_counties.px.html')


# now create some accessory horizontal bar charts to supplement the interactive and static choropleth maps
# this eventually was moved to an Excel effort but was left here for reference
df_sortedpop = merged_df.sort_values(by='Population', ascending=False)
fig, ax = plt.subplots(figsize=(12,15))
ax.barh(df_sortedpop['County'], df_sortedpop['Population'], color='blue')
ax.set(title='Colorado County Population', xlabel='Population', ylabel='County')
plt.show()

print('Done')