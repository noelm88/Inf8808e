'''
    Provides the templates for the tooltips.
'''


def get_heatmap_hover_template():
    '''
        Sets the template for the hover tooltips in the heatmap.

        Contains three labels, followed by their corresponding
        value, separated by a colon : neighborhood, year and
        trees planted.

        The labels are font 'Roboto Slab' and bold. The values
        are font 'Roboto' and regular weight.
    '''
    '''
    template = " <b>Neighborhood: </b>%{y}<br>Year: %{x}<br>Trees Planted :%{z}<extra></extra>"
    title = '<span style = "font-family: 'Grenze Gotisch';\
        color: black;font-size: 24px">'+ name +'</span><br><br>'
    neighborhood_label = '<b style="font-family: 'Roboto Slab'; color: black; font-size: 24px">'+ %{y} +'</b><br><br>'
    neighborhood_value = '<span style="font-family: 'Roboto'">'+ y + '</span> <br>'''
    font = 'Roboto'
    font_bold = 'Roboto Slab'
    
    neighborhood_label = '<b style="font-family: {font_bold}; color: black">'+ 'Neighborhood: ' +'</b>'
    neighborhood_value = '<span style="font-family: {font}; color: black">'+ '%{y}' + '</span> <br>'
    
    year_label = '<b style="font-family: {font_bold}; color: black">'+ 'Year: ' +'</b>'
    year_value = '<span style="font-family: {font}; color: black">'+ '%{x|%Y}' + '</span> <br>'
    
    trees_label = '<b style="font-family: {font_bold}; color: black">'+ 'Trees planted: ' +'</b>'
    trees_value = '<span style="font-family: {font}; color: black">'+ '%{z}' + '</span> <br>'
    
    extra = '<extra></extra>'
    
    return (neighborhood_label + neighborhood_value + year_label + year_value + trees_label + trees_value + extra)




def get_linechart_hover_template():
    '''
        Sets the template for the hover tooltips in the heatmap.

        Contains two labels, followed by their corresponding
        value, separated by a colon : date and trees planted.

        The labels are font 'Roboto Slab' and bold. The values
        are font 'Roboto' and regular weight.
    '''
    # TODO : Define and return the hover template
    
    font = 'Roboto'
    font_bold = 'Roboto Slab'
    
    date_label = '<b style="font-family: {font_bold}; color: black">'+ 'Date: ' +'</b>'
    date_value = '<span style="font-family: {font}; color: black">'+ '%{x|%d %b}' + '</span> <br>'
    
    trees_label = '<b style="font-family: {font_bold}; color: black">'+ 'Trees: ' +'</b>'
    trees_value = '<span style="font-family: {font}; color: black">'+ '%{y}' + '</span> <br>'
    
    return (date_label+date_value+trees_label+trees_value)

