import pandas as pd
import folium
import plotly.graph_objs as go
from pyodide.http import open_url
import js
import json


# Load data
zdf = pd.read_csv(open_url("https://raw.githubusercontent.com/Dravitar/LUISSDataVisProject/main/zdf.csv"))
zdf = zdf.rename(columns={'total_rate': 'Total Rate',
			  'state_rate': 'State Rate',
                          'county_rate': 'County Rate',
                          'city_rate': 'City Rate',
                          'additional_rate': 'Additional Rate'})

# Create the colors dictionary
colors = {'State Rate':'#A3333D', 'County Rate':'#FFFFFF', 'City Rate':'#1C1F33', 'Additional Rate':'#477998'}

# Calculate averages by state
states = zdf.groupby('Official State Name')['Total Rate', 'State Rate', 'County Rate', 'City Rate', 'Additional Rate'].mean()
states = pd.DataFrame(states).reset_index()

# Create a map centered on the United States
map_usa = folium.Map(location=[37.0902, -95.7129], zoom_start=4)

# Upload the file we used to get the information on the States borders
us_states=json.loads(open_url("https://raw.githubusercontent.com/Dravitar/LUISSDataVisProject/main/us-states.json").getvalue())

# Create a choropleth map using the Total Rate column
folium.Choropleth(
	geo_data=us_states,
	name='choropleth',
	data=states,
	columns=['Official State Name', 'Total Rate'],
	key_on='feature.properties.name',
	fill_color='RdBu',
	fill_opacity=0.7,
	line_opacity=0.2,
	legend_name='Total Sales Taxes (%)',
).add_to(map_usa)

folium.Marker(
    [32.806671,	-86.791130], popup="<iframe src='projectImages/Alabama.html'></iframe>", tooltip="Alabama"
).add_to(m)

# Display the map
#map_usa
def startMap():
	elem = Element("usa-map")
	elem.write(map_usa)
	
def pie_state(state_name):
	data = states[states["Official State Name"] == state_name].reset_index()
	ttl = ("Average Distribution of Sales Taxes in " + str(state_name))
	
	# getting the data ready for the pie chart
	tax_perc = data[['State Rate', 'County Rate', 'City Rate', 'Additional Rate']].div(data['Total Rate'], axis=0) * 100
	tax_perc = tax_perc.mean().sort_values(ascending=False)
	tax_perc = pd.DataFrame(tax_perc)
	
	
	# create a list of values for the chart
	values = list(tax_perc[0])
	# create a list of colors for the chart
	colors_list = [colors[idx] for idx in tax_perc.index]
	# create the pie chart
	data=[go.Pie(labels=tax_perc.index, values=values, marker_colors=colors_list,sort=False,
		     direction='clockwise',textposition='outside',hoverinfo='label+percent',marker={'line': {'color': 'black', 'width': 2}})]
	layout=go.Layout(title={'text': ttl,'x':0.5},font={'size': 20},paper_bgcolor='white',
			 legend={'bordercolor': 'black', 'borderwidth': 1, 'font': {'size': 16}, 'xanchor':'right', 'x':1.3})
	
	fig = go.Figure(data=data, layout=layout)
