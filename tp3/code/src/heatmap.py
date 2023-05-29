'''
    Contains some functions related to the creation of the heatmap.
'''
import plotly.express as px
from hover_template import get_heatmap_hover_template

def get_figure(data):
    '''
        Generates the heatmap from the given dataset.

        Make sure to set the title of the color bar to 'Trees'
        and to display each year as an x-tick. The x and y axes should
        be titled "Year" and "Neighborhood". 

        Args:
            data: The data to display
        Returns:
            The figure to be displayed.
    '''
    print(data)
    fig = px.imshow(data, template = "plotly_white")
    fig.update_traces(hovertemplate= get_heatmap_hover_template())
    return fig
    # TODO : Create the heatmap. Make sure to set dragmode=False in
    # the layout. Also don't forget to include the hover template.
