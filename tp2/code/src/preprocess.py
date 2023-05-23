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
    df = df1 = pd.DataFrame()
    df = my_df.copy(deep = True)
    for i in range(1,6):
        act_i_df = df[df['Act']==i]
        top5= act_i_df.sort_values(by = ['Count'],ascending = False).head(5)
        list_actors = list(top5['Player'])
        act_i_df['Player'] = [x if x in list_actors else 'OTHERS' for x in act_i_df.Player]
        df = pd.concat([df,act_i_df])
    
    df['Count'] = df.groupby(['Act','Player'])['Count'].transform('sum')
    df['Percentile'] = df.groupby(['Act','Player'])['Percentile'].transform('sum')
    my_df = df.drop_duplicates()
    # TODO : Replace players in each act not in the top 5 by a
    # new player 'OTHER' which sums their line count and percentage
    
    #now to sum up all the lines from OTHERS we do the same as before
    
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
    # each name is already starting with a capital letter
    return my_df
