
# -*- coding: utf-8 -*-

'''
    File name: app.py
    Author: Olivia Gélinas
    Course: INF8808
    Python Version: 3.8

    This file contains the source code for TP5.
'''
import json

import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State

import plotly.graph_objects as go

import preprocess as preproc
import map_viz
import helper
import callback

app = dash.Dash(__name__)
app.title = 'TP5 | INF8808'

with open('./assets/data/montreal.json', encoding='utf-8') as data_file:
    montreal_data = json.load(data_file)

with open('./assets/data/projetpietonnisation2017.geojson',
          encoding='utf-8') as data_file:
    street_data = json.load(data_file)

street_df = preproc.to_df(street_data)
street_df = preproc.update_titles(street_df)
street_df = preproc.sort_df(street_df)

locations = preproc.get_neighborhoods(montreal_data)
z = len(montreal_data['features']) * [1]

fig = go.Figure()

colorscale = ['#CDD1C4', '#CDD1C4']

fig = map_viz.add_choro_trace(fig, montreal_data, locations, z, colorscale)
fig = map_viz.add_scatter_traces(fig, street_df, )

fig = helper.adjust_map_style(fig)
fig = helper.adjust_map_sizing(fig)
fig = helper.adjust_map_info(fig)

app.layout = html.Div(
    className='row',
    children=[
        dcc.Graph(figure=fig, id='graph',
                  config=dict(
                      showTips=False,
                      showAxisDragHandles=False,
                      displayModeBar=False)),
        html.Div(
            className='panel-div',
            style={
                'justifyContent': 'center',
                'alignItems': 'center'},
            children=[
                html.Div(id='panel', style={
                    'visibility': 'hidden',
                    'border': '1px solid black',
                    'padding': '10px'},
                         children=[
                             html.Div(id='marker-title', style={
                                 'fontSize': '24px'}),
                             html.Div(id='mode', style={
                                 'fontSize': '16px'}),
                             html.Div(id='theme', style={
                                 'fontSize': '16px'})])])])


@app.callback([Output('marker-title', 'children'),
               Output('mode', 'children'),
               Output('theme', 'children'),
               Output('panel', 'style')],
              [Input('graph', 'clickData')],
              [State('graph', 'figure'),
               State('marker-title', 'children'),
               State('mode', 'children'),
               State('theme', 'children'),
               State('panel', 'style')])
def display(clicks_fig, figure, title, mode, theme, style): # noqa : E501 pylint: disable=unused-argument too-many-arguments line-too-long
    '''
        This function handles clicks on the map. When a
        marker is clicked, more information is displayed
        in the panel on the right of the map.

        Args:
            clicks_fig: The clickData associated with the map
            figure: The figure containing the map
            title: The current display title
            mode: The current display title
            theme: The current display theme
            style: The current display style for the panel
        Returns:
            title: The updated display title
            mode: The updated display title
            theme: The updated display theme
            style: The updated display style for the panel
    '''
    ctx = dash.callback_context

    if not ctx.triggered:
        return callback.no_clicks(style)
    if ctx.triggered[0]['prop_id'].split('.')[0] == 'graph':
        curve = ctx.triggered[0]['value']['points'][0]['curveNumber']
        point = ctx.triggered[0]['value']['points'][0]['pointNumber']

        if curve == 0:
            return callback.map_base_clicked(title, mode, theme, style)
        return callback.map_marker_clicked(figure,
                                           curve,
                                           point,
                                           title,
                                           mode,
                                           theme,
                                           style)
    return None, None, None, None
