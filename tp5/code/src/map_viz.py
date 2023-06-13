'''
    Contains the functions to set up the map visualization.

'''

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd 
import hover_template as hover


def add_choro_trace(fig, montreal_data, locations, z_vals, colorscale):
    '''
        Adds the choropleth trace, representing Montreal's neighborhoods.

        Note: The z values and colorscale provided ensure every neighborhood
        will be grey in color. Although the trace is defined using Plotly's
        choropleth features, we are simply defining our base map.

        The opacity of the map background color should be 0.2.

        Args:
            fig: The figure to add the choropleth trace to
            montreal_data: The data used for the trace
            locations: The locations (neighborhoods) to show on the trace
            z_vals: The table to use for the choropleth's z values
            colorscale: The table to use for the choropleth's color scale
        Returns:
            fig: The updated figure with the choropleth trace

    '''
    # TODO : Draw the map base
    df = pd.DataFrame.from_dict(pd.json_normalize(montreal_data['features']),orient='columns')
    fig = px.choropleth(df, 
                        geojson=montreal_data, 
                        locations= 'properties.CODEID', 
                        color=z_vals,
                        color_continuous_scale=colorscale, 
                        featureidkey='properties.CODEID',
                        labels=  locations,
                        hover_data = ['properties.NOM'],
                        custom_data = ['properties.NOM'],
                    )
    fig.update_geos(fitbounds="locations")
    fig.update_traces(marker_opacity=0.2, selector=dict(type='choropleth'))
    fig.update_traces(hovertemplate = hover.map_base_hover_template())
    return fig


def add_scatter_traces(fig, street_df):
    '''
        Adds the scatter trace, representing Montreal's pedestrian paths.

        The marker size should be 20.

        Args:
            fig: The figure to add the scatter trace to
            street_df: The dataframe containing the information on the
                pedestrian paths to display
        Returns:
            The figure now containing the scatter trace

    '''
    #Add the scatter markers to the map base
    print(street_df['properties.TYPE_SITE_INTERVENTION'])
    print(street_df)
    fig1 = px.scatter_geo(
        street_df,
        lat=street_df['properties.LATITUDE'],
        lon=street_df['properties.LONGITUDE'],
        color = street_df['properties.TYPE_SITE_INTERVENTION'],
        hover_data = ['properties.TYPE_SITE_INTERVENTION'],
        custom_data = ['properties.TYPE_SITE_INTERVENTION'],
        )
    fig1.update_traces(hovertemplate = hover.map_marker_hover_template()) 
    for i in range(len(fig1.data)):
        fig.add_trace(fig1.data[i])
    return fig
