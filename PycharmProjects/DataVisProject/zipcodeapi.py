
# First we import our required libraries
import pandas as pd
import requests

# Next we read the CSV file we downloaded containing a list of all ZIP codes in America.
# There is a lot of information in the file that we will use later on for our visualizations.
zdf = pd.read_csv("georef-united-states-of-america-zc-point@public.csv", sep=";")
apiKey = 'W0qJ9YsKzX1TIwCcsAa6Og==vaDy0zBbql2gJYp3'
# Here we simply grab the list of all zip codes from the CSV so we can send it to the API.
codes = zdf["Zip Code"].tolist()

# Here we define the list we will be collecting the API tax responses into.
responses = []

# Here is our code to call the API for sales tax information for each zip code.
# We are doing it this way instead of possibly downloading the database directly because the site
# we found for this database requires a paid account to download databases directly.
for zip_code in codes:
    # Here is where we call the specific API URL for each zip code
    api_url = 'https://api.api-ninjas.com/v1/salestax?zip_code={}'.format(zip_code)
    # Here we get the response from the API given the specific URL we crafted above, passing along
    # my API key to gain access to the data.

    # ONLY REMOVE COMMENT IF YOU ARE READY TO CALL
    ###################
    response = requests.get(api_url, headers={'X-Api-Key': apiKey})
    ###################

    # If the response is good, we append the response to our list of responses.
    if response.status_code == requests.codes.ok:
        responses.append(response.text)
    else:
        # Otherwise, there is an error with the data so we will add an N/A that we can filter out later.
        responses.append("N/A")

# Finally, we write the completed list to a text file so we don't have to call the database again,
# which would be pricey both in terms of computation time and network time, but also literally pricey.
# We only get 50,000 free API calls a month, and with more than 33,000 zip codes, we only get one shot
# before we have to pay.
with open("DataVisTaxList.txt", "w") as output:
    output.write(str(responses))