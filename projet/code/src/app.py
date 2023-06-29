
# -*- coding: utf-8 -*-

'''
    File name: app.py
    Author: Olivia Gélinas
    Course: INF8808
    Python Version: 3.8

    This file is the entry point for our dash app.
'''

import dash
from dash import html,dcc,Input,Output,callback
import plotly.express as px

from dash.exceptions import PreventUpdate

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
    html.Div(className='viz-container',
             style = {'display':'grid','font-family': "Arial"},
             children=[
        #first row
        html.Div(
            style={'display':'grid'},
            children=[
            dcc.Markdown('''
                ### Global evolution
                
                We can see an augmentation of the surface covered by solar pannels by 5.000.000 m²
                and a decrease in the total area used for waste disposal by 300.000 m²
                
                         ''',
                id='global_text',
                style={'display':'inline'}),
            dcc.Graph(
                id='bar_chart_global',
                className='graph',
                figure=map_vis.get_bar_chart_town(Global_stat_df,'the Fukushima Prefecture'),
                config=dict(
                scrollZoom=False,
                showTips=False,
                showAxisDragHandles=False,
                doubleClick=False,
                displayModeBar=False,
                style={'display':'inline'}
            ))]),        
        #second row
        html.Div(
                style = {'display':'block'},
                children=[
                #first column of second row
                html.Div(
                    style={'display':'inline'},
                    children=[
                         dcc.Graph(
                             id='map_solar2022',
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
                             id='map_solar2023',
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
                         ]),
                #second column of second row
                html.Div(
                    style={'display':'inline'},
                    children = [
                        dcc.Graph(
                            id='map_waste2022',
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
                            id='map_waste2023',
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
                            )
                        ]),
                ]),
        #third row
        html.Div(children=[
            html.Div([dcc.Dropdown(id='town_selector',
                         options=Sites_map_df['Municipality'].unique(),
                         value='Okuma Machi')]),
            dcc.Graph(
                id='site_scatter',
                #figure=map_vis.get_empty_figure(town_name_example),
                figure=map_vis.get_scatter_plot(town_sites_example,center_example,town_name_example,Fukushima_data),
                config=dict(
                    scrollZoom=True,
                    showTips=False,
                    showAxisDragHandles=False,
                    doubleClick=False,
                    displayModeBar=False
                    )
                ),
            dcc.Graph(
                id='bar_chart_local',
                figure=map_vis.get_bar_chart_town(town_stat_example,town_name_example),
                config=dict(
                    scrollZoom=False,
                    showTips=False,
                    showAxisDragHandles=False,
                    doubleClick=False,
                    displayModeBar=False
                    )
                ),
            ])
        ])
    ])


@callback(Output('site_scatter', 'figure'),
          Input('town_selector', 'value')
)
def update_scatterplot(town_name):
    '''
        When a cell in the heatmap is clicked, updates the
        bar chart and the scatter chart to show the data for 
        the corresponding municipality

    '''
    if town_name =='no town found':
        fig_scatter = map_vis.get_empty_figure(town_name)
        fig_bar = map_vis.get_empty_figure(town_name)
    else :
        town_sites,center = preprocess.get_municipal_data(Sites_df,Prefecture_data,town_name)
        town_stat = preprocess.get_municipal_stat_data(Sites_map_df, town_name)
        fig_scatter=map_vis.get_scatter_plot(town_sites,center,town_name,Fukushima_data)
        fig_bar = map_vis.get_bar_chart_town(town_stat,town_name)
    return(fig_scatter)
