import pandas as pd
from pyodide.http import open_url

url = (
    "https://raw.githubusercontent.com/Dravitar/LUISSDataVisProject/main/zdf_with_new_england.csv"  
    )
zip_code_data = pd.read_csv(open_url(url))

def test():
    elem = Element("dataHeadSpace")
    elem.write(zip_code_data.head())
