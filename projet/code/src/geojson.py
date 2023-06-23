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

def find_municipality(latitude,longitude,towns_data):
    '''
    this function useb the position of the site and the geojson 
    of the muncipalities to determine in wich town is the site
    '''
    point = (longitude,latitude)
    municipality = 'no town found'
    for town in towns_data['features']:
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
        town = find_municipality(latitude,longitude,towns_data)
        feat['properties']['latitude']= latitude
        feat['properties']['longitude']= longitude
        feat['properties']['municipality']= town
        
    return (my_data)
