To run this code you need a python3 environement and the following libraries installed

pandas 
numpy
json
matplotlib
geopandas
plotly
dash
dash_html_components
dash_core_components

server.py 	create a window and link it to localhost:8050 on your browser.

app.py 		create the windows and place all the figures.

map_vis.py 	use the data to create the visualisations.

preprocess.py 	preprocess and reformat the data so that it is easily used by map_vis.

template.py 	sets the template for all the visualisations

geojson.py 	takes the raw geojson and add properties to them,
		it will also be used to detect wich town is clicked on certain visualisations.

The geojson data are in the /geojson folder

