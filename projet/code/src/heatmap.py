'''
    Contains some functions related to the creation of the heatmap.
'''
import plotly.express as px
import plotly.graph_objects as go



def get_map(df,geojson_data,colorscale,title):
    '''
        Generates the heatmap of the site from the given dataset.
    '''
    fig = px.choropleth(df, 
                        geojson=geojson_data, 
                        locations= 'Municipality', 
                        color= 'Area_m2',
                        featureidkey='properties.ward_en',
                        labels= 'Municipality',
                        color_continuous_scale = colorscale,
                        hover_data = ['Area_m2'],
                        custom_data = ['Municipality','Area_m2'],
                        hover_name= "Municipality",
                        title = title
                        )

    #center the map
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_traces(hovertemplate = "<b>%{customdata[0]}</b><br> %{customdata[1]} m²")
    return fig
