'''
    This file contains the code for the bubble plot.
'''

import plotly.express as px
import plotly.graph_objects as go
from hover_template import get_bubble_hover_template


def get_plot(df, gdp_range, co2_range):
    '''
        Generates the bubble plot.

        The x and y axes are log scaled, and there is
        an animation between the data for years 2000 and 2015.

        The discrete color scale (sequence) to use is Set1 (see : https://plotly.com/python/discrete-color/)

        The markers' maximum size is 30 and their minimum
        size is 6.

        Args:
            my_df: The dataframe to display
            gdp_range: The range for the x axis
            co2_range: The range for the y axis
        Returns:
            The generated figure
    '''
    # TODO : Define figure with animation
    #df=my_df.copy(deep=True)
    #min_pop = df.min()['Population']
    #max_pop = df.max()['Population']
    #df['Size'] = (((df['Population']-min_pop)/(max_pop-min_pop))*24)+6"
    fig  = px.scatter(df,
                      x=df['GDP'],
                      y=df['CO2'],
                      animation_frame=df['Year'],
                      log_x = True,
                      log_y = True, 
                      range_x=gdp_range,
                      range_y=co2_range,
                      color=df['Continent'],
                      size =df['Population'],
                      size_max = 30,
                      color_discrete_sequence=px.colors.qualitative.Set1,
                      #hover_name = df['Country Name'],
                      hover_data = ['Country Name','Population','GDP','CO2'],
                      custom_data = ['Country Name','Population','GDP','CO2'],
                      )
    fig.update_traces(marker_sizemin = 6)
    return fig


def update_animation_hover_template(fig):
    '''
        Sets the hover template of the figure,
        as well as the hover template of each
        trace of each animation frame of the figure

        Args:
            fig: The figure to update
        Returns:
            The updated figure
    '''
    
    # Set the hover template
    fig.update_traces(hovertemplate = get_bubble_hover_template())
    return fig

def update_animation_menu(fig):
    '''
        Updates the animation menu to show the current year, and to remove
        the unnecessary 'Stop' button.

        Args:
            fig: The figure containing the menu to update
        Returns
            The updated figure
    '''
    # TODO : Update animation menu

    return fig


def update_axes_labels(fig):
    '''
        Updates the axes labels with their corresponding titles.

        Args:
            fig: The figure to be updated
        Returns:
            The updated figure
    '''
    # TODO : Update labels
    fig.update_layout(
        xaxis_title="GDP per capita ($ USD)",
        yaxis_title="CO2 emissions per capita (metric tonnes)"
        )
    return fig


def update_template(fig):
    '''
        Updates the layout of the figure, setting
        its template to 'simple_white'

        Args:
            fig: The figure to update
        Returns
            The updated figure
    '''
    # TODO : Update template
    fig.update_layout(
        template = 'simple_white'
        )
    return fig


def update_legend(fig):
    '''
        Updated the legend title

        Args:
            fig: The figure to be updated
        Returns:
            The updated figure
    '''
    fig.update_layout(
        legend_title = 'Legend'
        )
    # TODO : Update legend
    return fig
