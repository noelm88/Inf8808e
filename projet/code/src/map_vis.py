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
                        title = title
                        )

    #center the map
    fig.update_layout(coloraxis_colorbar_title_text = '<b>m²</b>')
    fig.update_layout(dragmode = False)
    fig.update_geos(fitbounds="locations",
                    visible=False)
    fig.update_traces(hovertemplate = "<b>%{customdata[0]}</b><br> %{customdata[1]} m²")
    return fig

def get_empty_figure():
    '''
        Returns the figure to display when there is no data to show.

    '''
    fig = px.line()
    fig.update_layout(dragmode = False)
    fig.add_annotation(dict(showarrow = False,text="No data to display. Select a cell in the heatmap for more information."))
    fig.add_shape(
        type="rect",
        fillcolor="LightGray",
    )
    return(fig)

def get_scatter_plot(sites_df,center,town_name,towns_data):
    my_colorscale = {'solar_new':'#16FF32','solar_still':'#479B55',
                     'solar_removed':'#325A9B','waste_new':'#FD3216',
                     'waste_still':'#FF9619','waste_removed':'#9D755D'}
    Municipal_df = pd.DataFrame.from_dict(pd.json_normalize(towns_data['features']),orient='columns')
    Municipal_df['colors']=[0 if (x==town_name) else 1 for x in Municipal_df['properties.ward_en']]
    title = "Evolution of the solar and waste disposal sites in " +town_name
    fig_town = px.choropleth(Municipal_df, 
                    geojson=towns_data, 
                    locations= 'properties.ward_en', 
                    color= 'colors',
                    featureidkey='properties.ward_en',
                    labels= 'properties.ward_en',
                    color_continuous_scale = 'greys',
                    hover_name= 'properties.ward_en',
                    title = title
                    )
    #we update the layout so that it is centered on town_name
    fig_town.update(layout_coloraxis_showscale=False)
    fig_town.update_layout(dragmode = False)
    fig_town.update_traces(marker_opacity=0.2, selector=dict(type='choropleth'))
    fig_town.update_geos(center=center,
                         projection= {'scale':400},
                         visible=False)
    fig_sites = px.scatter_geo(sites_df,
                              lat='Latitude',
                              lon='Longitude',
                              color = 'Site_type',
                              size = 'Area_m2',
                              hover_data = ['Id','Site_type','Area_m2'],
                              custom_data = ['Id','Site_type','Area_m2'],
                              color_discrete_map = my_colorscale)
    for i in range(len(fig_sites.data)):
        fig_town.add_trace(fig_sites.data[i])    
    return fig_town

def get_bar_chart_town(df,town_name):
    title = "Evolution of solar pannels instalations and waste disposal areas in "+town_name
    fig = px.bar(df,
                 x='Year',
                 y='Area_m2',
                 color='Site_type',
                 barmode='group',
                 title=title,
                 text = "Area_m2")
    fig.update_layout(
        yaxis=go.layout.YAxis(title = 'Total area covered by sites (m²)'
            )
        )
    return fig