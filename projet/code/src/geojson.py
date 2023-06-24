# -*- coding: utf-8 -*-
"""
Created on Fri Jun 23 14:19:56 2023

@author: galau
"""

import json
import pandas as pd
import numpy as np
import matplotlib.path as mplPath




def is_inside(point,polygon):
    '''
    This function check wether or not a point is inside a polygon using Path
    '''
    bbPath = mplPath.Path(polygon)
    return(bbPath.contains_point(point))

def find_municipality(points,towns_data):
    '''
    this function useb the position of the site and the geojson 
    of the muncipalities to determine in wich town is the site
    '''
    municipality = 'no town found'
    for town in towns_data['features']:
        for point in points[0][0]:
            if is_inside(point,town['geometry']['coordinates'][0]):
                municipality = town['properties']['ward_en']
    return(municipality)

def find_lat(polygon):
    return(np.mean(polygon[0][0],axis=0)[1])
def find_long(polygon):
    return(np.mean(polygon[0][0],axis=0)[0])


def add_geojson_properties(my_data,towns_data):
    '''
    add all necessary properties to the geojson
    mean latitude and longitude of the site
    the municipality where the site can be found
    '''
    count = 0
    for feat in my_data['features']:
        feat['properties']['id']= count
        count+=1
        latitude = find_lat(feat['geometry']['coordinates'])
        longitude = find_long(feat['geometry']['coordinates'])
        town = find_municipality(feat['geometry']['coordinates'],towns_data)
        feat['properties']['latitude']= latitude
        feat['properties']['longitude']= longitude
        feat['properties']['municipality']= town
        
    return (my_data)


#%% The folowing geojson are used for the cloropleth map
with open('geojson/solar_pannels_2022.geojson', 'r') as f:
    Solar2022_data = json.load(f)
with open('geojson/solar_pannels_2023.geojson','r') as f:
    Solar2023_data = json.load(f)
with open('geojson/waste_2022.geojson','r') as f:
    Waste2022_data = json.load(f)
with open('geojson/waste_2023.geojson','r') as f:
    Waste2023_data = json.load(f)
    
##The geojson used to add properties modified because some towns are in several polygons!! 
with open('geojson/municipality.geojson', 'r') as f:
    Prefecture_data = json.load(f)

Solar2022_data = add_geojson_properties(Solar2022_data, Prefecture_data)
Solar2023_data = add_geojson_properties(Solar2023_data, Prefecture_data)
Waste2022_data = add_geojson_properties(Waste2022_data, Prefecture_data)
Waste2023_data = add_geojson_properties(Waste2023_data, Prefecture_data)





with open('geojson/S_2022.geojson', 'w') as f:
    json.dump(Solar2022_data, f)
with open('geojson/S_2023.geojson', 'w') as f:
    json.dump(Solar2023_data, f)
with open('geojson/W_2022.geojson', 'w') as f:
    json.dump(Waste2022_data, f)
with open('geojson/W_2023.geojson', 'w') as f:
    json.dump(Waste2023_data, f)
    
#%% Thos are used for the scatter bubble chart
with open('geojson/solarRemoved.geojson','r') as f:
    SRemoved = json.load(f)
with open('geojson/solarNew.geojson','r') as f:
    SNew = json.load(f)
with open('geojson/intersection_solar.geojson','r') as f:
    SStill = json.load(f)

with open('geojson/wasteRemoved.geojson','r') as f:
    WRemoved = json.load(f)
with open('geojson/wasteNew.geojson','r') as f:
    WNew = json.load(f)
with open('geojson/intersection_waste.geojson','r') as f:
    WStill = json.load(f)
    
##The geojson used to add properties modified because some towns are in several polygons!! 
with open('geojson/municipality.geojson', 'r') as f:
    Prefecture_data = json.load(f) 
    
SRemoved = add_geojson_properties(SRemoved, Prefecture_data)
SNew= add_geojson_properties(SNew, Prefecture_data)
SStill = add_geojson_properties(SStill, Prefecture_data)

WRemoved = add_geojson_properties(WRemoved, Prefecture_data)
WNew= add_geojson_properties(WNew, Prefecture_data)
WStill = add_geojson_properties(WStill, Prefecture_data)

with open('geojson/Sremoved.geojson','w') as f:
    json.dump(SRemoved,f)
with open('geojson/Snew.geojson','w') as f:
    json.dump(SNew,f)
with open('geojson/Sstill.geojson','w') as f:
    json.dump(SStill,f)

with open('geojson/Wremoved.geojson','w') as f:
    json.dump(WRemoved,f)
with open('geojson/Wnew.geojson','w') as f:
    json.dump(WNew,f)
with open('geojson/Wstill.geojson','w') as f:
    json.dump(WStill,f)
    

