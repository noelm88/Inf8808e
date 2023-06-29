'''
    Contains some functions related to the creation of the heatmap.
'''
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


def get_map(df,geojson_data,colorscale,type_site,title):
    '''
        Generates the heatmap of the site from the given dataset.
    '''
    fig = px.choropleth(df, 
                        geojson=geojson_data, 
                        locations= df.index, 
                        color= type_site,
                        featureidkey='properties.ward_en',
                        labels= df.index,
                        color_continuous_scale = colorscale,
                        hover_data = [type_site],
                        custom_data = [df.index,type_site],
                        hover_name= df.index,
                        title = title,
                        )

    #center the map
    fig.update_layout(coloraxis_colorbar_title_text = '<b>m²</b>',
                      height = 800,
                      width = 800)
    fig.update_layout(dragmode = False)
    fig.update_geos(fitbounds="locations",
                    visible=False)
    fig.update_traces(hovertemplate = "<b>%{customdata[0]}</b><br> %{customdata[1]} m²<extra></extra>")
    #We add a marker of the position of fukushima_daishi
    fig.add_trace(go.Scattergeo(showlegend=False,
                                lon=[141.0337],
                                lat=[37.4218],
                                marker_symbol='star-dot',
                                marker_color='black',
                                marker = {'size':10},
                                hovertemplate='Fukushima Daishi Power Plant<extra></extra>'
                                ))
    return fig

def get_empty_figure(name):
    '''
        Returns the figure to display when there is no data to show.

    '''
    text = name + " <br>No data to display. Select a municipality on the maps for more information."
    fig = px.line()
    fig.update_layout(dragmode = False)
    fig.add_annotation(dict(showarrow = False,text=text))
    fig.add_shape(
        type="rect",
        fillcolor="LightGray",
        height=  600,
        width = 900
    )
    return(fig)

def get_scatter_plot(sites_df,center,town_name,towns_data):
    #this is the custom colorscale for the sites
    my_colorscale = {'solar pannels installed since 07/2022':'#16FF32',
                     'solar pannels installed before 07/2022':'#479B55',
                     'solar pannels removed since 07/2022':'#325A9B',
                     'waste deposits installed since 07/2022':'#FD3216',
                     'waste deposits installed before 07/2022':'#FF9619',
                     'waste deposits removed since 07/2022':'#9D755D'}
    
    # We create a cloropleth map that highights the town we want to display
    Municipal_df = pd.DataFrame.from_dict(pd.json_normalize(towns_data['features']),orient='columns')
    Municipal_df['colors']=[0 if (x==town_name) else 1 for x in Municipal_df['properties.ward_en']]
    title = "Evolution of the solar and waste disposal sites <br> in " +town_name
    fig_town = px.choropleth(Municipal_df, 
                    geojson=towns_data, 
                    locations= 'properties.ward_en', 
                    color= 'colors',
                    featureidkey='properties.ward_en',
                    labels= 'properties.ward_en',
                    color_continuous_scale = 'greys',
                    hover_name= 'properties.ward_en',
                    title = title,
                    custom_data=['properties.ward_en']
                    )
    # We add a marker on the position of the fukushima daishi power plant/accident
    fig_town.add_trace(go.Scattergeo(name='Fukushima Daishi PLant',
                                showlegend=False,
                                lon=[141.0337],
                                lat=[37.4218],
                                marker_symbol='star-dot',
                                marker_color='black',
                                marker = {'size':25},
                                hovertemplate='Fukushima Daishi Power Plant<extra></extra>'))
    #we update the layout so that it is centered on town_name
    fig_town.update(layout_coloraxis_showscale=False)
    fig_town.update_layout(#dragmode = False,
                           height = 800,
                           width = 1800
                           )
    fig_town.update_traces(marker_opacity=0.2, selector=dict(type='choropleth'),
                           hovertemplate = "<b> %{customdata[0]} </b>")
    fig_town.update_geos(center=center,
                         projection= {'scale':400},
                         visible=False)
    #We add a geographical scatter plot of the differents sites
    fig_sites = px.scatter_geo(sites_df,
                              lat='Latitude',
                              lon='Longitude',
                              color = 'Description',
                              size = 'Area_m2',
                              hover_data = ['Description','Area_m2'],
                              custom_data = ['Description','Area_m2'],
                              color_discrete_map = my_colorscale)
    
    fig_sites.update_traces(marker={'sizemin':5},
                            hovertemplate = "<b>%{customdata[0]}</b><br>size of the site : %{customdata[1]} m² <extra></extra>")
    # We add the scatterplot data to the cloropleth map
    for i in range(len(fig_sites.data)):
        fig_town.add_trace(fig_sites.data[i])
    # We update the layout to properly display the legend
    fig_town.update_layout(legend=dict(font={'size':15},
                                       orientation="v",
                                       yanchor="middle",
                                       y=0.5,
                                       xanchor="right",
                                       x=1.5,
                                       bordercolor = 'black',
                                       borderwidth = 2
                                       ))
    return fig_town

def get_bar_chart_town(df,town_name):
    title = "Evolution of solar pannels instalations and waste disposal areas <br> in "+town_name
    fig = px.bar(df,
                 x='Year',
                 y='Area_m2',
                 color='Site_type',
                 color_discrete_map={'solar pannels':'#479B55','waste disposal areas':'#FF9619'},
                 labels={'Site_type':''},
                 barmode='group',
                 title=title,
                 text = "Area_m2",
                 custom_data=['Area_m2','Site_type','Year'])
    fig.update_layout(
        yaxis=go.layout.YAxis(title = 'Total area covered by sites (m²)'),
        height = 600,
        width = 600
        )
    fig.update_traces(
        hovertemplate = "there is %{customdata[0]} m² <br>of %{customdata[1]} <br>in %{customdata[2]} <extra></extra>")
    return fig