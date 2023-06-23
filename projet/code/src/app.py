
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
import heatmap
import line_chart
import template

app = dash.Dash(__name__)
app.title = 'Mitate Lab Project | INF8808'

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
##The geojson used to draw the maps 
with open('geojson/fukushima.geojson', 'r') as f:
    Fukushima_data = json.load(f)
    
    
Solar2022_data = preprocess.add_geojson_properties(Solar2022_data, Prefecture_data)
Solar2023_data = preprocess.add_geojson_properties(Solar2023_data, Prefecture_data)
Waste2022_data = preprocess.add_geojson_properties(Waste2022_data, Prefecture_data)
Waste2023_data = preprocess.add_geojson_properties(Waste2023_data, Prefecture_data)

Solar2022_df = preprocess.to_df(Solar2022_data,'solar2022')
Solar2023_df = preprocess.to_df(Solar2023_data,'solar2023')
Waste2022_df = preprocess.to_df(Waste2022_data,'waste2022')
Waste2023_df = preprocess.to_df(Waste2023_data,'waste2023')

MunicipalSolar2022_df = preprocess.to_town(Solar2022_df)
MunicipalSolar2023_df = preprocess.to_town(Solar2023_df)
MunicipalWaste2022_df = preprocess.to_town(Waste2022_df)
MunicipalWaste2023_df = preprocess.to_town(Waste2023_df)



template.create_custom_theme()
template.set_default_theme()

app.layout = html.Div(className='content', children=[
    html.Header(children=[
        html.H1('Reconstruction of the Fukushima Prefecture'),
        html.H2('In 2022 and 2023')
    ]),
    html.Main(className='viz-container', children=[
        dcc.Graph(
            id='heatmapsolar2022',
            className='graph',
            figure=heatmap.get_map(
                MunicipalSolar2022_df, 
                Fukushima_data, 
                px.colors.sequential.Greens,
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
            figure=heatmap.get_map(
                MunicipalSolar2023_df,
                Fukushima_data,
                px.colors.sequential.Greens,
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
            figure=heatmap.get_map(
                MunicipalWaste2022_df, 
                Fukushima_data, 
                px.colors.sequential.Oranges,
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
            figure=heatmap.get_map(
                MunicipalWaste2023_df, 
                Fukushima_data, 
                px.colors.sequential.Oranges,
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
            id='line-chart',
            className='graph',
            figure=line_chart.get_empty_figure(),
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
    Output('line-chart', 'figure'),
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
        fig = line_chart.get_empty_figure()
        line_chart.add_rectangle_shape(fig)
        return fig

    arrond = click_data['points'][0]['y']
    year = click_data['points'][0]['x']

    line_data = preprocess.get_daily_info(
        dataframe,
        arrond,
        year)
    line_fig = line_chart.get_figure(line_data, arrond, year)

    return line_fig
