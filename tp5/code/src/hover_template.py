'''
    Provides the templates for the tooltips.
'''


def map_base_hover_template():
    '''
        Sets the template for the hover tooltips on the neighborhoods.

        The label is simply the name of the neighborhood in font 'Oswald'.

        Returns:
            The hover template.
    '''
    # TODO : Generate the hover template
    #name= geojson['properties.NOM']
    font = 'Oswald'
    str = '<span style = "font-family: {font} "> %{customdata[0]} </span><extra></extra>'
    return str


def map_marker_hover_template():
    '''
        Sets the template for the hover tooltips on the markers.

        The label is simply the name of the walking path in font 'Oswald'.

        Args:
            name: The name to display
        Returns:
            The hover template.
    '''
    # TODO : Generate the hover template
    font = 'Oswald'
    str = '<span style = "font-family: {font} "> %{customdata[0]} </span><extra></extra>'
    return str