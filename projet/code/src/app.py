
# -*- coding: utf-8 -*-

'''
    File name: app.py
    Author: Olivia Gélinas
    Course: INF8808
    Python Version: 3.8

    This file is the entry point for our dash app.
'''

import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
from dash.dependencies import Input, Output

import pandas as pd
import json

import preprocess
import map_vis
import template

app = dash.Dash(__name__)
app.title = 'Mitate Lab Project | INF8808'

#%% We open the data for the cloropleth map


# the geojson with the sites
with open('geojson/S_2022.geojson', 'r') as f:
    Solar2022_data = json.load(f)
with open('geojson/S_2023.geojson','r') as f:
    Solar2023_data = json.load(f)
with open('geojson/W_2022.geojson','r') as f:
    Waste2022_data = json.load(f)
with open('geojson/W_2023.geojson','r') as f:
    Waste2023_data = json.load(f)

##The geojson used to draw the maps 
with open('geojson/fukushima.geojson', 'r') as f:
    Fukushima_data = json.load(f)
    
##The geojson used to find in wich town a point (site or click) is
with open('geojson/municipality.geojson', 'r') as f:
    Prefecture_data = json.load(f)
    
Solar2022_df = preprocess.to_df(Solar2022_data,'solar2022')
Solar2023_df = preprocess.to_df(Solar2023_data,'solar2023')
Waste2022_df = preprocess.to_df(Waste2022_data,'waste2022')
Waste2023_df = preprocess.to_df(Waste2023_data,'waste2023')

#a dataframes of all the sites
Sites_map_df = pd.concat([Solar2022_df, Solar2023_df, Waste2022_df, Waste2023_df])
#a dataframe containing the total accross all the prefecture
Global_stat_df = preprocess.get_global_stat_data(Sites_map_df)
#a dataframes containing the total m² of each type of site per municipality 
Municipal_df = preprocess.get_map_df(Sites_map_df)

#%% We open the data for the scatter map

with open('geojson/Sremoved.geojson','r') as f:
    SRemoved_data = json.load(f)
with open('geojson/Snew.geojson','r') as f:
    SNew_data = json.load(f)
with open('geojson/Sstill.geojson','r') as f:
    SStill_data = json.load(f)

with open('geojson/Wremoved.geojson','r') as f:
    WRemoved_data = json.load(f)
with open('geojson/Wnew.geojson','r') as f:
    WNew_data = json.load(f)
with open('geojson/Wstill.geojson','r') as f:
    WStill_data = json.load(f)

Sremoved_df= preprocess.to_df(SRemoved_data,'solar_removed')
Snew_df = preprocess.to_df(SNew_data,'solar_new')
Sstill_df = preprocess.to_df(SStill_data,'solar_still')

Wremoved_df= preprocess.to_df(WRemoved_data,'waste_removed')
Wnew_df = preprocess.to_df(WNew_data,'waste_new')
Wstill_df = preprocess.to_df(WStill_data,'waste_still')

#a dataframes of all the sites
Sites_df = pd.concat([Sremoved_df,Snew_df,Sstill_df,Wremoved_df,Wnew_df,Wstill_df]).dropna()
    
#%%
town_name_example='Okuma Machi'
town_sites_example,center_example = preprocess.get_municipal_site_data(Sites_df,Prefecture_data,town_name_example)
town_stat_example = preprocess.get_municipal_stat_data(Sites_map_df, town_name_example)

template.create_custom_theme()
template.set_default_theme()

app.layout = html.Div(className='content', children=[
    html.Header(children=[
        html.H1('Reconstruction of the Fukushima Prefecture'),
        html.H2('In 2022 and 2023')
    ]),
    html.Main(className='viz-container', children=[
        dcc.Graph(
            id='bar_chart_global',
            className='graph',
            figure=map_vis.get_bar_chart_town(Global_stat_df,'the Fukushima Prefecture'),
            config=dict(
                scrollZoom=False,
                showTips=False,
                showAxisDragHandles=False,
                doubleClick=False,
                displayModeBar=False
            )
        ),
        dcc.Graph(
            id='heatmapsolar2022',
            className='graph',
            figure=map_vis.get_map(
                Municipal_df, 
                Fukushima_data, 
                px.colors.sequential.Greens,
                "solar2022",
                "Solar instalations per municipality in 2022 m²"),
            config=dict(
                scrollZoom=False,
                showTips=False,
                showAxisDragHandles=False,
                doubleClick=False,
                displayModeBar=False
            )
        ),
        dcc.Graph(
            id='heatmapsolar2023',
            className='graph',
            figure=map_vis.get_map(
                Municipal_df,
                Fukushima_data,
                px.colors.sequential.Greens,
                "solar2023",
                "Solar instalations per municipality in 2023 m²"),
            config=dict(
                scrollZoom=False,
                showTips=False,
                showAxisDragHandles=False,
                doubleClick=False,
                displayModeBar=False
            )
        ),
        dcc.Graph(
            id='heatmapwaste2022',
            className='graph',
            figure=map_vis.get_map(
                Municipal_df, 
                Fukushima_data, 
                px.colors.sequential.Oranges,
                "waste2022",
                "Waste disposal areas per municipality in 2022 m²"),
            config=dict(
                scrollZoom=False,
                showTips=False,
                showAxisDragHandles=False,
                doubleClick=False,
                displayModeBar=False
            )
        ),
        dcc.Graph(
            id='heatmapwaste2023',
            className='graph',
            figure=map_vis.get_map(
                Municipal_df, 
                Fukushima_data, 
                px.colors.sequential.Oranges,
                "waste2023",
                "Waste disposal areas per municipality in 2023 m²"),
            config=dict(
                scrollZoom=False,
                showTips=False,
                showAxisDragHandles=False,
                doubleClick=False,
                displayModeBar=False
            )
        ),
        dcc.Graph(
            id='site_scatter',
            className='graph',
            #figure=map_vis.get_empty_figure(),
            figure=map_vis.get_scatter_plot(town_sites_example,center_example,town_name_example,Fukushima_data),
            config=dict(
                scrollZoom=False,
                showTips=False,
                showAxisDragHandles=False,
                doubleClick=False,
                displayModeBar=False
            )
        ),
        dcc.Graph(
            id='bar_chart_local',
            className='graph',
            figure=map_vis.get_bar_chart_town(town_stat_example,town_name_example),
            config=dict(
                scrollZoom=False,
                showTips=False,
                showAxisDragHandles=False,
                doubleClick=False,
                displayModeBar=False
            )
        )
    ])
])


@app.callback(
    Output('site_scatter', 'figure'),
    [Input('heatmap', 'clickData')]
)
def heatmap_clicked(click_data):
    '''
        When a cell in the heatmap is clicked, updates the
        line chart to show the data for the corresponding
        neighborhood and year. If there is no data to show,
        displays a message.

        Args:
            The necessary inputs and states to update the
            line chart.
        Returns:
            The necessary output values to update the line
            chart.
    '''
    if click_data is None or click_data['points'][0]['z'] == 0:
        fig = map_vis.get_empty_figure()
        return fig

    lat = click_data['points'][0]['y']
    long = click_data['points'][0]['x']
    points= [[lat,long]] #ugly but it was in that way in the geojsons files
    town_name = preprocess.find_municipality(points,Prefecture_data)
    if town_name =='no town found':
        fig = map_vis.get_empty_figure()
        return fig
    else :
        town_sites,center = preprocess.get_municipal_data(Sites_df,Prefecture_data,town_name)
        town_fig=map_vis.get_scatter_plot(town_sites,center,town_name,Fukushima_data)
    return( town_fig)
