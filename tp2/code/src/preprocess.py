'''
    Contains some functions to preprocess the data used in the visualisation.
'''
import numpy as np
import pandas as pd
from modes import MODE_TO_COLUMN


def summarize_lines(my_df):
    '''
        Sums each player's total of number of lines and  its
        corresponding percentage per act.

        The sum of lines per player per act is in a new
        column named 'PlayerLine'.

        The percentage of lines per player per act is
        in a new column named 'PlayerPercent'

        Args:
            my_df: The pandas dataframe containing the data from the .csv file
        Returns:
            The modified pandas dataframe containing the
            information denescribed above.
    '''
    my_df = my_df[['Act','Player']]
    
    my_df['Count'] = my_df.groupby(['Act','Player'])['Player'].transform('count')
    my_df['Total_act_lines'] = my_df.groupby(['Act'])['Player'].transform('count')
    my_df['Percentile'] = 100*my_df['Count']/my_df['Total_act_lines']
    my_df = my_df[['Act','Player','Count','Percentile']]
    my_df = my_df.drop_duplicates()
    # TODO : Modify the dataframe, removing the line content and replacing
    # it by line count and percent per player per act
    return my_df


def replace_others(my_df):
    '''
        For each act, keeps the 5 players with the most lines
        throughout the play and groups the other players
        together in a new line where :

        - The 'Act' column contains the act
        - The 'Player' column contains the value 'OTHER'
        - The 'LineCount' column contains the sum
            of the counts of lines in that act of
            all players who are not in the top
            5 players who have the most lines in
            the play
        - The 'PercentCount' column contains the sum
            of the percentages of lines in that
            act of all the players who are not in the
            top 5 players who have the most lines in
            the play

        Returns:
            The df with all players not in the top
            5 for the play grouped as 'OTHER'
    '''
    #We get the 5 actors with the most lines in the play
    df = my_df.copy(deep = True)
    df['Act'] = 0
    df['Count'] = my_df.groupby(['Player'])['Count'].transform('sum')
    df['Percentile'] = my_df.groupby(['Player'])['Percentile'].transform('sum')
    df = df.drop_duplicates()
    top5 = df.sort_values(by = ['Count'],ascending = False).head(5)
    list_actors = list(top5['Player'])

    #For every actor not in the top 5 we replace its name with other
    my_df['Player'] = [x if (x in list_actors) else 'OTHERS' for x in my_df.Player]

    #We groupby and sum up all the lines by 'Others' 
    my_df['Count'] = my_df.groupby(['Act','Player'])['Count'].transform('sum')
    my_df['Percentile'] = my_df.groupby(['Act','Player'])['Percentile'].transform('sum')
    my_df = my_df.drop_duplicates()
        
    return my_df


def clean_names(my_df):
    '''
        In the dataframe, formats the players'
        names so each word start with a capital letter.

        Returns:
            The df with formatted names
    '''
    # TODO : Clean the player names
    my_df['Player'] = [x.capitalize() for x in my_df.Player]
    my_df = my_df.reset_index(drop=True)
    # each name is already starting with a capital letter
    return my_df
