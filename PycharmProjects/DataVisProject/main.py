
# First we import our required libraries
import pandas as pd
import json

database = []

with open("DataVisTaxList.txt", "r") as file:
    database = file.read()

dataTypes = {
    "zip_code": [],
    "total_rate": [],
    "state_rate": [],
    "city_rate": [],
    "county_rate": [],
    "additional_rate": []
}
dataframe = pd.DataFrame(dataTypes)

listOfStateStrings = database[2:][:-2].split("', '")
for stateString in listOfStateStrings:
    if stateString != "N/A":
        data = stateString[2:][:-2].split(", ")
        first = True
        zipcode = ""
        values = {"zip_code": 0,
                  "total_rate": 0,
                  "state_rate": 0,
                  "city_rate": 0,
                  "county_rate": 0,
                  "additional_rate": 0}
        for item in data:
            if first:
                values[item.split(": ")[0][1:][:-1]] = item.split(": ")[1][1:][:-1]
            else:
                values[item.split(": ")[0][1:][:-1]] = float(item.split(": ")[1][1:][:-1])
            first = False
        row_to_add = pd.Series(values)
        dataframe = dataframe.append(row_to_add, ignore_index=True)
        #dataframe = dataframe(row_to_add)

print(dataframe)
