import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.patches as mpatches

# Load data
zdf = pd.read_csv("C:/Users/Fatma/Documents/GitHub/LUISSDataVisProject/zdf.csv")
zdf = zdf.rename(columns={'total_rate': 'Total Rate',
                          'state_rate': 'State Rate',
                          'county_rate': 'County Rate',
                          'city_rate': 'City Rate',
                          'additional_rate': 'Additional Rate'})

# Calculate averages by state and by city
states = zdf.groupby('Official State Name')['Total Rate', 'State Rate', 'County Rate', 'City Rate', 'Additional Rate'].mean()
cities = zdf.groupby(['Official State Name', 'Official USPS city name'])['Total Rate', 'State Rate', 'County Rate', 'City Rate', 'Additional Rate'].mean()

# GRAPH 1: Stacked bar charts for highest and lowest total taxes
## States with highest total taxes
data = states.sort_values('Total Rate', ascending=False).head(5).drop(columns='Total Rate')
data.plot(kind='bar', stacked=True, color=['red', 'ghostwhite', 'darkblue', 'cornflowerblue'], edgecolor='black')
plt.xlabel('State')
plt.ylabel('Total Sales Tax Rates')
plt.ylim([0, 0.12])
plt.title('Highest Total Sales Tax Rates')
plt.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))

## States with lowest total taxes (excluding states with no sales taxes)
data = states.sort_values('Total Rate', ascending=True).head(10).drop(columns='Total Rate')
data = data.iloc[5:, :]
data.plot(kind='bar', stacked=True, color=['red', 'ghostwhite', 'darkblue', 'cornflowerblue'], edgecolor='black')
plt.xlabel('State')
plt.ylabel('Total Sales Tax Rates')
plt.ylim([0, 0.12])
plt.title('Lowest Total Sales Tax Rates')
plt.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))

# GRAPH 2: Pie chart for tax percentage by type
## Calculate tax percentage for state, county, city, and additional rate
tax_perc = states[['State Rate', 'County Rate', 'City Rate', 'Additional Rate']].div(states['Total Rate'], axis=0) * 100
tax_perc = tax_perc.mean().sort_values(ascending=False)

## Create pie chart
colors = ["#FE0303", "#F8F8FE", "#00008A", "#6394EC"]
pal = sns.color_palette(colors)
fig, ax = plt.subplots()
wedges, texts, autotexts = ax.pie(tax_perc, colors=pal, autopct='%1.1f%%', startangle=90, counterclock=False, wedgeprops={'edgecolor': 'black', 'linewidth': 1})
ax.set_title('Percentage of Taxes by Type')

## Create custom legend
handles = []
for i, tax_type in enumerate(tax_perc.index):
    handles.append(mpatches.Patch(color=pal[i], label=tax_type))
ax.legend(handles=handles, title="Tax Type", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))

plt.show()

# GRAPH 3: Box plot for comparison of tax rates by type
## Select columns for box plot
boxplot_data = states[['State Rate', 'County Rate', 'City Rate', 'Additional Rate']]

## Create box plot
colors = ["#FE0303", "#F8F8FE", "#00008A", "#6394EC"]
pal = sns.color_palette(colors)
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

# GRAPH 4: Scatter plot for density vs. total taxes by region
## Extract latitude from Geo Point column
zdf['Latitude'] = zdf['Geo Point'].str.split(',').str[0].astype(float)

# Define the region based on the latitude
def get_region(latitude):
    if latitude >= 35:
        return 'North'
    elif latitude >= 25:
        return 'Middle'
    else:
        return 'South'
    
zdf['Region'] = zdf['Latitude'].apply(get_region)

## Set the colors for the South, Middle, and North regions
colors = {'South': '#FE0303', 'Middle': '#6394EC', 'North': '#00008A'}

## Create the scatterplot
fig, ax = plt.subplots()
for region, group in zdf.groupby('Region'):
    ax.scatter(group['Density'], group['Total Rate'], c=colors[region], label=region, alpha=0.7)

## Set the title, labels, and legend
ax.set_title('Density vs. Total Taxes by Region')
ax.set_xlabel('Density')
ax.set_ylabel('Total Taxes')
ax.legend()

## Show the plot
plt.show()
