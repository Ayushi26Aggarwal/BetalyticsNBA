# -*- coding: utf-8 -*-
"""PlayerBlocksOddsAPI

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1tTBO9i3pQZ4joZ4yIIcpsaeMdJk9gLx1
"""

pat = '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'
!git clone https://{pat}@github.com/Ayushi26Aggarwal/BetalyticsNBA.git

cd /content/BetalyticsNBA

import requests
import pandas as pd
import json
import re

# Define the URL for the API request
url = "https://api.the-odds-api.com/v4/sports/basketball_nba/events?apiKey=96e45b9af0dcb5961e81d736ca4d1b59&markets=player_blocks&regions=us"

# Send a GET request to the URL
response = requests.get(url)

# Get the content of the response as text
content = response.text

# Remove the non-JSON parts
content = re.sub(r"^angular.callbacks._\d+\(", "", content)
content = re.sub(r"\);$", "", content)

# Load the JSON data into a DataFrame
df = pd.read_json(content)

points = pd.DataFrame()

for i in range(len(df)):
  print(i)
  url = "https://api.the-odds-api.com/v4/sports/basketball_nba/events/"+df['id'][i]+"/odds?apiKey=96e45b9af0dcb5961e81d736ca4d1b59&markets=player_blocks&regions=us"
  # Send a GET request to the URL
  response = requests.get(url)

  # Get the content of the response as text
  content = response.text

  # Remove the non-JSON parts
  content = re.sub(r"^angular.callbacks._\d+\(", "", content)
  content = re.sub(r"\);$", "", content)

  # Load the JSON data into a DataFrame
  df1 = pd.read_json(content)
  # Extract the bookmakers into a DataFrame
  bookmakers_df = pd.json_normalize(df1['bookmakers'])
  fanduel = True
  j = 0
  while fanduel & len(bookmakers_df != 0):
    if bookmakers_df['key'][j] == 'fanduel':
      market = pd.DataFrame(bookmakers_df['markets'][j])
      market = pd.DataFrame(market['outcomes'][0])
      fanduel = False
    j += 1
  print(int(len(market)/2))
  for k in range(int(len(market)/2)):
    print(k)
    row = [[df['id'][i], df['commence_time'][i], df['home_team'][i], df['away_team'][i], market['description'][k*2], market['point'][k*2], market['price'][k*2], market['price'][((k+1)*2)-1]]]
    points = pd.concat([points,pd.DataFrame(row)], ignore_index=True)

points

points.columns=['id', 'commence_time', 'home_team', 'away_team', 'Player Name', 'point', 'over price', 'under price']

old_data = pd.read_csv('/content/drive/MyDrive/Colab Notebooks/MoneylineOddsAPI.csv')
write_data = pd.concat([old_data.iloc[:,1:],new_df], ignore_index=True)
write_data['commence_time'] = pd.to_datetime(write_data['commence_time'])
write_data = write_data.drop_duplicates(['id','home_team', 'away_team'])
write_data.to_csv('/content/drive/MyDrive/Colab Notebooks/MoneylineOddsAPI.csv')

points.to_csv('/content/BetalyticsNBA/PlayerBlocks.csv')

#new_df
!git init






## Step 2: Set your account identity in this repository.
##########
!git config user.email "ayushi.aggarwal@brainiuminfotech.com"
!git config user.name "Ayushi26Aggarwal"






## Step 3: Make the first commit
##########
# git isn't aware of the file READ.md , stage it
!git add .

# commit the staged changes with a message
!git commit -m "PlayerBlocks  .csv"

!git push origin main