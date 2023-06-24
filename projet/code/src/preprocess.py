'''
    Contains some functions to preprocess the data used in the visualisation.
'''
import pandas as pd
import numpy as np
import json
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
        for point in points:
            if is_inside(point,town['geometry']['coordinates'][0]):
                municipality = town['properties']['ward_en']
    return(municipality)


def find_lat(polygon):
    return(np.mean(polygon[0][0],axis=0)[1])
def find_long(polygon):
    return(np.mean(polygon[0][0],axis=0)[0])

def to_df(geo_data, site_type):
    '''
    This function turns the geojson into a panda dataframe and 'clean it up'
    '''
    df = pd.DataFrame.from_dict(pd.json_normalize(geo_data['features']),orient='columns')
    df['Area_m2']=df['properties.area_m2']
    df['Municipality']=df['properties.municipality']
    df['Longitude']=df['properties.longitude']
    df['Latitude']=df['properties.latitude']
    df['Id']=df['properties.id']
    df['Site_type']=site_type
    df = df[['Id','Municipality','Site_type', 'Area_m2', 'Longitude','Latitude']].drop_duplicates()
    return(df)

def get_map_df(df):
    '''
    
    This function turns the site database in a database indexed on the municipalities
    with columns solar2022, solar2023, waste2022 and waste2023 representing the total
    surface of eaxch type of site in each municipality
    '''
    df['Area_m2'] = df.groupby(['Municipality','Site_type'])['Area_m2'].transform('sum')
    df = df[['Municipality','Site_type', 'Area_m2']].drop_duplicates()
    df = df.pivot(index='Municipality', columns ='Site_type', values = 'Area_m2')
    # Then we fill the NaN values with 0
    df = df.fillna(0)
    df=df.astype(int)
    return(df)

def get_municipal_site_data(sites_df,towns_geojson,town_name='Nishigo Mura'):
    '''
    this function select the sites belonging to a municipality 
    it also returns the center point of said town
    '''
    df = sites_df.loc[sites_df['Municipality']==town_name]
    geo_df = pd.DataFrame.from_dict(pd.json_normalize(towns_geojson['features']),orient='columns')
    geo_df = geo_df.loc[geo_df['properties.ward_en']==town_name]
    points = geo_df.iat[0,-1][0]
    centerpoint = np.mean(points,axis=0)
    center = {'lon':centerpoint[0],'lat':centerpoint[1]}
    

    return( df, center)

def get_municipal_stat_data(df, town_name):
    df=df.loc[df['Municipality']==town_name]
    df['Area_m2'] = df.groupby(['Site_type'])['Area_m2'].transform('sum')
    df = df[['Site_type', 'Area_m2']].drop_duplicates()
    year = {'solar2022':'2022','solar2023':'2023','waste2022':'2022', 'waste2023':'2023'}
    site_type = {'solar2022':'solar','solar2023':'solar','waste2022':'waste', 'waste2023':'waste'}
    df['Year']=[year[x] for x in df['Site_type']]
    df['Site_type']=[site_type[x] for x in df['Site_type']]
    return df

def get_global_stat_data(my_df):
    df = my_df.copy(deep=True)
    df['Area_m2'] = df.groupby(['Site_type'])['Area_m2'].transform('sum')
    df = df[['Site_type', 'Area_m2']].drop_duplicates()
    year = {'solar2022':'2022','solar2023':'2023','waste2022':'2022', 'waste2023':'2023'}
    site_type = {'solar2022':'solar','solar2023':'solar','waste2022':'waste', 'waste2023':'waste'}
    df['Year']=[year[x] for x in df['Site_type']]
    df['Site_type']=[site_type[x] for x in df['Site_type']]
    print(df)
    return df

     