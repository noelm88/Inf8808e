'''
    Contains some functions to preprocess the data used in the visualisation.
'''
import pandas as pd
import numpy as np
from datetime import datetime
from datetime import timedelta
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


def summarize_yearly_counts(my_df):
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
    df = my_df.copy(deep = True)
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
    #We select the data from the arrond and the selected year
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
