import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style("white")
import plotly.graph_objs as go
import plotly.io as pio
import plotly.offline as pyo
from pyodide.http import open_url


# Load data
zdf = pd.read_csv(open_url("https://raw.githubusercontent.com/Dravitar/LUISSDataVisProject/main/zdf.csv"))
zdf = zdf.rename(columns={'total_rate': 'Total Rate',
                          'state_rate': 'State Rate',
                          'county_rate': 'County Rate',
                          'city_rate': 'City Rate',
                          'additional_rate': 'Additional Rate'})

# Calculate averages by state and by city
states = zdf.groupby('Official State Name')[['Total Rate', 'State Rate', 'County Rate', 'City Rate', 'Additional Rate']].mean()
cities = zdf.groupby(['Official State Name', 'Official USPS city name'])[['Total Rate', 'State Rate', 'County Rate', 'City Rate', 'Additional Rate']].mean()

# creating the colors dictionary
colors = {'State Rate':'#A3333D', 'County Rate':'#FFFFFF', 'City Rate':'#1C1F33', 'Additional Rate':'#477998'}


#==================================================================================

# GRAPH 1: Stacked bar charts for highest and lowest total taxes
## All States
# Set the default renderer to 'svg'
pio.renderers.default = 'svg'

## Sort the states in ascending order based on the total tax rate

data = states.sort_values('Total Rate', ascending=False).drop(columns='Total Rate')

# Create traces for each category and a layout for the graph
traces = []
for col in data.columns:
    trace = go.Bar(x=data.index,y=data[col],name=col,marker={'color': colors[col], 'line': {'color': 'black', 'width': 2}},hovertemplate='%{x}<br>%{y:.2f}<extra></extra>')
    traces.append(trace)

# Create a Figure object, add the traces, and show the plot
fig = go.Figure(data=traces)

# Update the layout to create a stacked bar plot
fig.update_layout(
    barmode='stack',title={'text':"Average Sales Tax Rate by State",'x': 0.5,
                           'xanchor': 'center','yanchor': 'top','font': {'size': 30, 'family': 'Arial Black'}},
    xaxis_title="States",yaxis_title="Tax Rate",
    plot_bgcolor='white', paper_bgcolor='white',bargap=0.1,
    width = 1100)
# Update the x-axis font size
fig.update_xaxes(tickfont=dict(size=13),tickangle=270,automargin=True)

fig.show()

# Save the picture in HD
pio.write_image(fig, file='Sales Tax Rates Avg.png', format='png', width=1920, height=1080)



## States with highest total taxes
data = states.sort_values('Total Rate', ascending=False).head(5).drop(columns='Total Rate')
# Create traces for each category and a layout for the graph
traces = []
for col in data.columns:
    trace = go.Bar(x=data.index, y=data[col], name=col, marker={'color': colors[col],'line': {'color': 'black', 'width': 2}})
    traces.append(trace)

layout = go.Layout(title={'text': 'Highest Total Sales Tax Rates','x': 0.5,'xanchor': 'center','yanchor': 'top','font': {'size': 30, 'family': 'Arial Black'}},
                   barmode='stack', xaxis={'title': 'State', 'title_font': {'size': 20}}, yaxis={'title': 'Sales Tax Rate', 'title_font': {'size': 20}, 'range':[0, 0.12]}, 
                   colorway=list(colors.values()), 
                   legend={'bordercolor': 'black', 'borderwidth': 1, 'font': {'size': 16}}, 
                   font={'size': 20}, plot_bgcolor='white', paper_bgcolor='white', 
                   margin={'l': 40, 'b': 40, 't': 80, 'r': 10}, 
                   bargap=0.15, bargroupgap=0.1)


# Create and display figure
fig = go.Figure(data=traces, layout=layout)

#fig.show()
# Save the picture in HD
#pio.write_image(fig, file='Highest Total Sales Tax Rates.png', format='png', width=1200, height=800)

## States with lowest total taxes (excluding states with no sales taxes)
data = states.sort_values('Total Rate', ascending=True).head(10).drop(columns='Total Rate')
data = data.iloc[5:, :]
# Create traces for each category and a layout for the graph
traces = []
for col in data.columns:
    trace = go.Bar(x=data.index, y=data[col], name=col, marker={'color': colors[col],'line': {'color': 'black', 'width': 2}})
    traces.append(trace)
layout = go.Layout(title={'text': 'Lowest Total Sales Tax Rates','x': 0.5,'xanchor': 'center','yanchor': 'top','font': {'size': 30, 'family': 'Arial Black'}}, barmode='stack', xaxis={'title': 'State', 'title_font': {'size': 20}}, yaxis={'title': 'Sales Tax Rate', 'title_font': {'size': 20}, 'range':[0, 0.12]}, 
                   colorway=list(colors.values()), 
                   legend={'bordercolor': 'black', 'borderwidth': 1, 'font': {'size': 16}}, 
                   font={'size': 20}, plot_bgcolor='white', paper_bgcolor='white', 
                   margin={'l': 40, 'b': 40, 't': 80, 'r': 10}, 
                   bargap=0.15, bargroupgap=0.1)
# Create and display figure
fig = go.Figure(data=traces, layout=layout)
#fig.show()
# Save the picture in HD
#pio.write_image(fig, file='Lowest Total Sales Tax Rates.png', format='png', width=1200, height=800)


# GRAPH 2: Pie chart for tax percentage by type
## Calculate tax percentage for state, county, city, and additional rate
tax_perc = states[['State Rate', 'County Rate', 'City Rate', 'Additional Rate']].div(states['Total Rate'], axis=0) * 100
tax_perc = pd.DataFrame(tax_perc.mean().sort_values(ascending=False))
# create a list of values for the chart
values = list(tax_perc[0])
# create a list of colors for the chart
colors_list = [colors[idx] for idx in tax_perc.index]
# create the pie chart
data=[go.Pie(labels=tax_perc.index, values=values, marker_colors=colors_list,sort=False,
             direction='clockwise',textposition='outside',hoverinfo='label+percent',marker={'line': {'color': 'black', 'width': 2}})]
layout=go.Layout(title='Tax Rates by Type',font={'size': 20, 'family': 'Arial Black'},paper_bgcolor='white',
                 legend={'bordercolor': 'black', 'borderwidth': 1, 'font': {'size': 16}, 'xanchor':'right', 'x':1.3})

fig = go.Figure(data=data, layout=layout)
# display the chart
#fig.show()
# Save the picture in HD
#pio.write_image(fig, file='Tax Rates by Type.png', format='png', width=1200, height=800)



# GRAPH 3: Box plot for comparison of tax rates by type
## Select columns for box plot
boxplot_data = states[['State Rate', 'County Rate', 'City Rate', 'Additional Rate']]

## Create box plot
c = ["#A3333D", "#FFFFFF", "#1C1F33", "#477998"]
pal = sns.color_palette(c)
fig, ax = plt.subplots()
bp = ax.boxplot(boxplot_data, patch_artist=True, labels=['State Rate', 'County Rate', 'City Rate', 'Additional Rate'], sym='k.')

## Set colors and borders for boxes and whiskers
for i, box in enumerate(bp['boxes']):
    box.set(facecolor=pal[i], linewidth=2)
    box.set(edgecolor='black', linewidth=2)
for whisker in bp['whiskers']:
    whisker.set(color='black', linewidth=2)
for cap in bp['caps']:
    cap.set(color='black', linewidth=2)
for median in bp['medians']:
    median.set(color='black', linewidth=2)

ax.set_title('Comparison of Tax Rates by Type')
ax.set_ylabel('Tax Rate')

plt.show()
plt.savefig("Boxplot.png", dpi=300)



## Extract latitude from Geo Point column
zdf['Latitude'] = zdf['Geo Point'].str.split(',').str[0].astype(float)
# Define the region based on the latitude
def get_region(latitude):
    if latitude >= 39:
        return 'North'
    else:
        return 'South'
zdf['Region'] = zdf['Latitude'].apply(get_region)

## Set the colors for the South and North region
cb = {'South': '#A3333D', 'North': '#477998'}

# GRAPH 4: bubble plot
bb = zdf.groupby(['Density', 'Total Rate', 'Region']).count()
bb = pd.DataFrame(bb['Zip Code']).reset_index()
bb = bb.rename(columns={'Zip Code': 'Number of Cities'})
bb = bb[(bb["Density"] != 0) & (bb["Total Rate"] != 0)]

fig, ax = plt.subplots()
ax.set_title('Density vs Total Taxes by Region')
sns.scatterplot(bb,x="Density",y="Total Rate",size="Number of Cities",hue='Region',
                palette=cb,alpha=0.5,sizes=(20, 700))
sns.move_legend(ax, "upper left", bbox_to_anchor=(1, 1))
plt.subplots_adjust(right=0.7)
plt.savefig("bb.png", dpi=300)

## bubble chart for south only
sb = bb[bb['Region'] == 'South']
fig, ax = plt.subplots()
ax.set_title('Density vs Total Taxes by Region - Southern Region')
sns.scatterplot(sb,x="Density",y="Total Rate",c='#A3333D',size="Number of Cities",
                palette=cb,alpha=0.5,sizes=(20, 700))
sns.move_legend(ax, "upper left", bbox_to_anchor=(1, 1))
plt.subplots_adjust(right=0.7)
plt.savefig("sb.png", dpi=300)

## bubble chart for north only
nb = bb[bb['Region'] == 'North']
fig, ax = plt.subplots()
ax.set_title('Density vs Total Taxes by Region - Northern Region')
sns.scatterplot(nb,x="Density",y="Total Rate",c='#477998',size="Number of Cities",
                palette=cb,alpha=0.5,sizes=(20, 700))
sns.move_legend(ax, "upper left", bbox_to_anchor=(1, 1))
plt.subplots_adjust(right=0.7)
plt.savefig("nb.png", dpi=300)


# =============================================================================
### INTERACTIVE GRAPHS
# GRAPH 1: given a zip code and a price, calculate the total after taxes and
# visualize its distribution

# first, let's calculate the total price from the inputs
def getZipCodeGraph(zipCode, price):
  z = int(zipCode)
  p = float(price)
  
  for i in range (0, len(zdf)):
      if zdf["Zip Code"][i] == z:
          tp = p * (1+zdf["Total Rate"][i])
          tp = round(tp,2)
  print ("Your price after sales taxes is: $" + str(tp))

  # now, let's do the visualization for the zip code given as input
  data = zdf[zdf["Zip Code"] == z].reset_index()
  ttl = ("Distribution of Sales Taxes in " + str(data["Official USPS city name"][0]) + ", " + str(data["Official State Name"][0]))

  # getting the data ready for the pie chart
  tax_perc = data[['State Rate', 'County Rate', 'City Rate', 'Additional Rate']].div(data['Total Rate'], axis=0) * 100
  tax_perc = tax_perc.mean().sort_values(ascending=False)
  tax_perc = pd.DataFrame(tax_perc)

  # drawing the pie
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
  

  elem = Element("image_container")
  #pyo.plot(fig, filename=f'distribution_of_sales_taxes_{zipCode}.html', auto_open=False)
  elem.write(fig)
  
  elem2 = Element("price_container")
  elem2.write(tp)
 
