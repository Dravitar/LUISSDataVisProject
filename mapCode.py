import pandas as pd
from pyodide.http import open_url

stateAvs = pd.read_csv(open_url("https://raw.githubusercontent.com/Dravitar/LUISSDataVisProject/main/StateAverages.csv"))
state_geo = json.loads(requests.get("https://raw.githubusercontent.com/python-visualization/folium/main/examples/data/us-states.json").text)

m = folium.Map(location=[48, -102], zoom_start=3)

folium.Choropleth(
    geo_data=state_geo,
    name="choropleth",
    data=stateAvs,
    columns=["Official State Name", "Average Tax Rate"],
    key_on="feature.id",
    fill_color="YlGn",
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name="Average Tax Rate (%)",
).add_to(m)

folium.LayerControl().add_to(m)

def USAMap():
	elem2 = Element("usa-map")
	elem2.write(m)