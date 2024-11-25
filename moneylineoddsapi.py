# -*- coding: utf-8 -*-
"""MoneylineOddsAPI

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1zPmcstU-nrV0wS96GPowGP7gequfveWK
"""

pat = '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'
!git clone https://{pat}@github.com/Ayushi26Aggarwal/BetalyticsNBA.git

cd /content/BetalyticsNBA

import requests
import pandas as pd
import json
import re

# Define the URL for the API request
url = "https://api.the-odds-api.com/v4/sports/basketball_nba/odds/?apiKey=96e45b9af0dcb5961e81d736ca4d1b59&markets=h2h&regions=us"

# Send a GET request to the URL
response = requests.get(url)

# Get the content of the response as text
content = response.text

# Remove the non-JSON parts
content = re.sub(r"^angular.callbacks._\d+\(", "", content)
content = re.sub(r"\);$", "", content)

# Load the JSON data into a DataFrame
df = pd.read_json(content)

# Extract the bookmakers into a DataFrame
bookmakers_df = pd.json_normalize(df['bookmakers'])

# Create new DataFrame for the first 15 rows

new_df = df.iloc[:, :6].copy()
new_df['home_price'] = 0
new_df['away_price'] = 0

# Iterate over the rows to fill price and point columns
for i in range(len(df)):
  print(i)
  temp = df['bookmakers'][i]
  fanduel_market = next((market for market in temp if market['key'] == 'fanduel'), None)
  if fanduel_market is not None:
    outcomes = fanduel_market['markets'][0]['outcomes']
    under_outcome = next((outcome for outcome in outcomes if outcome['name'] == df['home_team'][i]), None)
    over_outcome = next((outcome for outcome in outcomes if outcome['name'] == df['away_team'][i]), None)
    if under_outcome is not None:
      new_df.at[i, 'home_price'] = under_outcome['price']
    if over_outcome is not None:
      new_df.at[i, 'away_price'] = over_outcome['price']

# Set the name columns
#new_df = df.iloc[:, :6].copy()  # Assuming you want the same as the original new_df

# Combine both DataFrames and set the names
#new_df['name'] = 'Over'
#combined_df = pd.concat([new_df.iloc[:15], new_df1.iloc[:15]], ignore_index=True)

# Write the combined DataFrame to a CSV file
#combined_df.to_csv('odds_api_totals.csv', index=False)

old_data = pd.read_csv('/content/BetalyticsNBA/MoneylineOddsAPI.csv')
write_data = pd.concat([old_data.iloc[:,1:],new_df], ignore_index=True)
write_data['commence_time'] = pd.to_datetime(write_data['commence_time'])
write_data = write_data.drop_duplicates(['id','home_team', 'away_team'])
write_data.to_csv('/content/BetalyticsNBA/MoneylineOddsAPI.csv')

#new_df.to_csv('/content/BetalyticsNBA/MoneylineOddsAPI.csv')

!git init






## Step 2: Set your account identity in this repository.
##########
!git config user.email "ayushi.aggarwal@brainiuminfotech.com"
!git config user.name "Ayushi26Aggarwal"






## Step 3: Make the first commit
##########
# git isn't aware of the file READ.md , stage it
!git add MoneylineOddsAPI.csv

# commit the staged changes with a message
!git commit -m "MoneyLineOddsAPI csv file"

!git push -u origin main