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

def to_town(df):
    # get the total size by municipality
    df['Area_m2'] = df.groupby(['Municipality'])['Area_m2'].transform('sum')
    df = df[['Municipality','Site_type', 'Area_m2']].drop_duplicates()
    return(df)

def convert_dates(df):
    '''
        Converts the dates in the dataframe to datetime objects.

        Args:
            dataframe: The dataframe to process
        Returns:
            The processed dataframe with datetime-formatted dates.
    '''
    #Put the date as datetime object
    df['Date_Plantation'] = pd.to_datetime(df['Date_Plantation'], format='%Y-%m-%d')
    return df


def filter_years(df, start, end):
    '''
        Filters the elements of the dataframe by date, making sure
        they fall in the desired range.

        Args:
            dataframe: The dataframe to process
            start: The starting year (inclusive)
            end: The ending year (inclusive)
        Returns:
            The dataframe filtered by date.
    '''
    # Filter by dates between the years start and end included
    startY = datetime(year = start, month=1, day=1)
    endY = datetime(year = end+1, month=1, day=1)
    df = df.loc[(df['Date_Plantation'] >= startY) & (df['Date_Plantation'] < endY)]
    return df


def summarize_yearly_counts(df):
    '''
        Groups the data by neighborhood and year,
        summing the number of trees planted in each neighborhood
        each year.

        Args:
            dataframe: The dataframe to process
        Returns:
            The processed dataframe with column 'Counts'
            containing the counts of planted
            trees for each neighborhood each year.
    '''
    
    # first we put all the date to the year they correspond to
    df['Date_Plantation'] = [datetime(x.year,12,31,0,0,0,0,None) for x in df['Date_Plantation']]
    # then we do a count by arrond and year of plantation
    df['Count'] = df.groupby(['Date_Plantation','Arrond'])['Date_Plantation'].transform('count')
    # we drop the data on long and latt and drop the duplicate
    df = df[['Arrond','Arrond_Nom','Date_Plantation','Count']].drop_duplicates()
    return df


def restructure_df(yearly_df):
    '''
        Restructures the dataframe into a format easier
        to be displayed as a heatmap.

        The resulting dataframe should have as index
        the names of the neighborhoods, while the columns
        should be each considered year. The values
        in each cell represent the number of trees
        planted by the given neighborhood the given year.

        Any empty cells are filled with zeros.

        Args:
            yearly_df: The dataframe to process
        Returns:
            The restructured dataframe
    '''
    #First we restructure the data Frame
    yearly_df = yearly_df.pivot(index='Arrond_Nom', columns ='Date_Plantation', values = 'Count')
    # Then we fill the NaN values with 0
    yearly_df = yearly_df.fillna(0)
    return yearly_df


def get_daily_info(dataframe, arrond, year):
    '''
        From the given dataframe, gets
        the daily amount of planted trees
        in the given neighborhood and year.

        Args:
            dataframe: The dataframe to process
            arrond: The desired neighborhood
            year: The desired year
        Returns:
            The daily tree count data for that
            neighborhood and year.
    '''
    year = int(year[:4])
    dataframe['Date_Plantation']
    start = datetime(year = year, month=1, day=1)
    end = datetime(year = year+1, month=1, day=1)
    df = dataframe.loc[(dataframe['Arrond_Nom']==arrond)]
    df = df.loc[(df['Date_Plantation'] >= start) & (df['Date_Plantation'] < end)]
    df = df[['Arrond_Nom','Date_Plantation']]
    #We add a count column
    df['Count'] = df.groupby(['Date_Plantation'])['Date_Plantation'].transform('count')
    df = df.drop_duplicates()[['Date_Plantation','Count']]
    df = df.sort_values(by = 'Date_Plantation',ascending = True)
    df = df.reset_index()
    r = pd.date_range(start=df['Date_Plantation'].min(), end=df['Date_Plantation'].max())
    df = df.set_index('Date_Plantation').reindex(r).fillna(0.0).rename_axis('Date_Plantation').reset_index()
    return (df)
